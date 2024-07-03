#!/usr/bin/env python3
# Author: Marcel Schneider

import sqlite3
import inspect
import subprocess
from sys import stdin

def growtable(conn, table, newcolumns):
    c = conn.execute("SELECT * FROM %s LIMIT 1;" % table)
    columns = [d[0].lower() for d in c.description]
    for k, t in newcolumns.items():
        if k.lower() not in columns:
            q = "ALTER TABLE %s ADD COLUMN %s %s;" % (table, k, t.typename)
            print(q)
            conn.execute(q)
            
def initdb(dbfile):
    conn = sqlite3.connect(dbfile)
    load_sqlite_ext(conn)
    conn.execute("CREATE TABLE IF NOT EXISTS runs(runid INTEGER PRIMARY KEY AUTOINCREMENT, timestamp text, githash text, file text);")
    conn.execute("CREATE TABLE IF NOT EXISTS datapoints(runid INTEGER REFERENCES runs(runid));")
    conn.execute("CREATE INDEX IF NOT EXISTS runtodata ON datapoints(runid);")
    return conn

def load_sqlite_ext(conn):
    from pathlib import Path
    from os.path import realpath
    conn.enable_load_extension(True)
    module = Path(realpath(__file__)).parent / "percentile.so"
    if not module.exists():
        subprocess.call(['gcc', '-fPIC', '--shared', '-o', str(module), str(module.parent/'percentile.c')])
    conn.load_extension(str(module))
    module = Path(realpath(__file__)).parent / "extension-functions.so"
    if not module.exists():
        subprocess.call(['gcc', '-fPIC', '--shared', '-o', str(module), str(module.parent/'extension-functions.c')])
    conn.load_extension(str(module))

def make_commit():
    # fails if there is nothing to commit, which is fine.
    tempcommit = subprocess.call('git commit -a -m "Automatic commit for run on `date`" 1>&2', shell=True)
    res = subprocess.call('git tag -f test-`date "+%Y-%m-%d_%H_%M_%S"` 1>&2', shell=True)
    #assert res == 0, "Could not tag software in git"
    githash = subprocess.check_output(["git", "rev-parse", "HEAD"]).decode().strip()
    if tempcommit == 0: # success
        res = subprocess.call('git reset HEAD^ 1>&2', shell=True)
        assert res == 0, "Could not reset state in git"
    return githash

class Results:
    # unique markers for to-be-added columns
    # note that SQLite is always dynamically typed, and all columns can take any values
    # there will be some limited conversions when a type is given.
    class Type:
        def __init__(self, name, convert):
            self.typename = name;
            self.convert = convert
    Int = Type('INTEGER', int)
    Real = Type('REAL', float)
    Text = Type('TEXT', str)
    Any = Type('', lambda x: x)
    types = {Int, Real, Text, Any}
    
    def __init__(self, datafile = 'results.db', githash = None):
        self.conn = initdb(datafile)
        
        self.githash = githash #if githash else make_commit()
            
        # to make sure timestamp is fixed for this run
        self.timestamp = next(self.conn.execute("SELECT datetime('now');"))[0]
        
    def collector(self, **parameters):
        fixedparameters = {k: v for k, v in parameters.items() if v not in Results.types}
        fixedparameters['timestamp'] = self.timestamp
        fixedparameters['githash'] = self.githash
        fixedparameters['file'] = inspect.stack()[1].filename
        varparameters = {k: v for k, v in parameters.items() if v in Results.types}
        varparameters['runid'] = Results.Int

        keys = sorted(fixedparameters.keys())
        varkeys = sorted(varparameters.keys())
        varconvert = [varparameters[k].convert for k in varkeys]
        growtable(self.conn, 'runs', {k: Results.Any for k in fixedparameters})         
        growtable(self.conn, 'datapoints', varparameters)         
        
        self.conn.execute("INSERT INTO runs(%s) VALUES (%s);" 
                          % (", ".join(keys), ", ".join(["?"]*len(keys))),
                          [fixedparameters[k] for k in keys])
        
        runid = next(self.conn.execute("SELECT last_insert_rowid();"))[0]
        
        insert = ("INSERT INTO datapoints(%s) VALUES (%s);" 
                          % (", ".join(varkeys), ", ".join(["?"]*len(varkeys))))
        
        def collect(**kws):
            kws['runid'] = runid
            assert len(kws) == len(varkeys)
            values = [conv(kws[k]) for k, conv in zip(varkeys, varconvert)]
            self.conn.execute(insert, values)
        
        return collect;
    
    def close(self):
        self.conn.commit()
        self.conn.close()
        
    def commit(self):
        self.conn.commit()
        
def mergeresults(datafile, addedfile):
    assert datafile != addedfile
    conn = initdb(datafile)
    conn.execute("ATTACH DATABASE ? AS new;", (addedfile,))
    
    c = conn.execute("SELECT * FROM new.runs LIMIT 1;")
    columns =  {d[0].lower(): Results.Any for d in c.description}
    growtable(conn, "runs", columns)
    newruncols = ", ".join(k for k in columns if k != "runid")
    
    c = conn.execute("SELECT * FROM new.datapoints LIMIT 1;")
    columns =  {d[0].lower(): Results.Any for d in c.description}
    growtable(conn, "datapoints", columns)
    newdatacols = ", ".join(k for k in columns if k != "runid")
    
    c = conn.execute("SELECT * FROM runs LIMIT 1;")
    runcols = ", ".join(d[0].lower() for d in c.description if d[0] != "runid")
    
    print (addedfile)
    print (datafile)   
    print (newruncols)
        
    conn.execute("CREATE TEMP TABLE newids AS SELECT runid FROM new.runs WHERE (%s) NOT IN (SELECT DISTINCT %s FROM runs);" % (newruncols, newruncols))
    conn.execute("INSERT INTO runs(%s) SELECT %s FROM new.runs WHERE runid IN newids;" % (newruncols, newruncols))
    
    conn.execute("CREATE TEMP VIEW newruns(%s,  newid) AS SELECT %s,  rowid FROM runs;" % (runcols, runcols))
    conn.execute("CREATE TEMP VIEW idmap(oldid, newid) AS SELECT runid, newid FROM newruns NATURAL JOIN new.runs;")
    conn.execute("""INSERT INTO datapoints(runid,  %s) SELECT newid,  %s 
                    FROM new.datapoints INNER JOIN idmap ON runid = oldid 
                    WHERE runid in newids;""" % (newdatacols, newdatacols))
    conn.commit()
    conn.close()

def plotdata(datafile, sql = None, runsql = None, datasql = None, runwhere = None, where = None, select = "count(*)", group = False, ignore = None, plotType = None, **kwargs):
    conn = initdb(datafile)
    
    if not sql:
        if not runsql:
            c = conn.execute("SELECT * FROM runs LIMIT 1;")
            cols = ", ".join(d[0] for d in c.description if d[0] not in ["runid", "githash", "timestamp"])
            if runwhere:
                clause = "WHERE %s" % runwhere
            else:
                clause = ""
            runsql = "SELECT max(timestamp), * FROM runs %s GROUP BY %s" % (clause, cols)
            
        if not datasql:
            if group:
                c = conn.execute("SELECT * FROM runs LIMIT 1;")
                rcols = [d[0] for d in c.description if d[0]]
                c = conn.execute("SELECT * FROM datapoints LIMIT 1;")
                dcols = [d[0] for d in c.description if d[0]]
                if not ignore:
                    ignore = dcols + ["runid"]
                else:
                    ignore = ignore + ["runid"]
                cols = [c for c in dcols + rcols if c not in ignore]
                clause = "GROUP BY %s" % ", ".join(cols)
            else:
                clause = ""
                
            datasql = "SELECT %s FROM data %s" % (select, clause)
        
        if where != None:
            whereclause = "WHERE %s" % where
        else:
            whereclause = ""
            
        sql = """
            WITH current AS (
                %s
            ), data AS (
                SELECT * 
                FROM datapoints 
                INNER JOIN current ON current.runid = datapoints.runid
                %s
            )
            %s""" % (runsql, whereclause, datasql)
                 
    return conn, sql

def record(datafile, parameter, variable, githash):
        typemap = {"any": Results.Any, "int": Results.Int, "text": Results.Text, "real": Results.Real}
        args = {k: v for k,v in parameter}
        args.update({k: typemap[t.lower()] for k,t in variable})
        r = Results(datafile, githash)
        collector = r.collector(**args)
        for l in stdin.readlines():
            if l.isspace(): continue
            collector(**{k[0]:v for k, v in zip(variable, l.split())})
        r.close()
    
def execute(datafile):
    code = stdin.read()
    conn = sqlite3.connect(datafile)
    conn.executescript(code)
    
def show(explain=False, limit=0, **kwargs):
    conn, sql = plotdata(**kwargs)
    if limit > 0:
        sql = "%s LIMIT %i" % (sql, limit)
    print(sql)
    def prettyprint(c):
        if not c.description: print("No data."); return
        print("\t".join(d[0] for d in c.description))
        for row in c:
            print("\t".join(str(v) for v in row))
    if explain:
        prettyprint(conn.execute("EXPLAIN " + sql))
        prettyprint(conn.execute("EXPLAIN QUERY PLAN " + sql))
    else:
        prettyprint(conn.execute(sql))
    conn.close()
    
def listruns(**kwargs):
    show(datasql="SELECT * FROM runs", **kwargs)
    
def merge(datafile, addedfiles):
    for f in addedfiles:
        mergeresults(datafile, f)
        
def ggplot(**kwargs):
    from . import results_ggplot
    results_ggplot.ggplot(**kwargs)
    
def ggplot2(**kwargs):
    from . import results_ggplot2
    results_ggplot2.ggplot(**kwargs)

def pyplot(**kwargs):
    from . import results_pyplot
    results_pyplot.pyplot(**kwargs)

def commit(**kwargs):
    print(make_commit())
