# Author: Marcel Schneider
# Plot function using python ggplot.
import ggplot as gg
import pandas
from numpy import isreal, arange

from .results import plotdata

def ggplot(outfile, size, **kwargs):
    w, h = [float(x) for x in size.split("x", 1)]

    conn, sql = plotdata(**kwargs)
    header = sql + " LIMIT 0"
    c = conn.execute(header)
    cols  = [d[0] for d in c.description]
    paras = [c.split(';', 1) for c in cols]
    paras = [(c[0].split(' '), c[1] if len(c) > 1 else c[0], name) for c, name in zip(paras, cols)]
    
    data = pandas.read_sql(sql, conn)
    
    def find(s):
        try:
            return next(filter(lambda x: s in x[0], paras))
        except:
            return None, None, None
        
    kw = dict()
    xpar, xlbl, xname = find('X')
    assert xname, "Must have a X value"
    kw['x'] = xname
    ypar, ylbl, yname = find('Y')
    if yname:
        kw['y'] = yname
        
    cpar, clbl, cname = find('COLOR')
    if cname:
        if True: #isreal(data[cname][0]):
            data[clbl] = [str(x) for x in data[cname]]
            cname = clbl
        if 'HIST' in xpar and not 'LINE' in xpar:
            kw['fill'] = cname
        else:
            kw['color'] = cname
    spar, slbl, sname = find('SHAPE')
    if sname:
        data[slbl] = [str(x) for x in data[sname]]
        sname = slbl
        kw['shape'] = sname
        
    plot = gg.ggplot(data, gg.aes(**kw))
    
    kw = dict()
    none = True
    if 'HIST' in xpar:
        none = False
        if 'INT' in xpar:
            mini = min(data[xname])
            maxi = max(data[xname])
            kw['bins'] = arange(mini-0.5, maxi+1.5, 1)
            kw['xbins'] = arange(mini-0.5, maxi+1.5, 1)
        if cname:
            kw['alpha'] = 0.7
        if 'LINE' in xpar:
            kw['alpha'] = None
            kw['fill'] = (0,0,0,0) # rgba tuple
            kw['type'] = 'step'
            kw['size'] = 2
        if yname:
            assert 'HIST' in ypar, "No PROFILE yet, use HIST/HIST or BOX"
            if 'INT' in ypar:
                mini = min(data[yname])
                maxi = max(data[yname])
                kw['ybins'] = arange(mini-0.5, maxi+1.5, 1)
            kw['fill'] = 1
            # TODO: this is broken. Probably in ggplot.
            plot += gg.geom_tile(**kw)
        else:
            plot += gg.geom_histogram(**kw)
    if yname and 'BOX' in ypar:
        none = False
        plot += gg.geom_boxplot()
    if yname and 'BAR' in ypar:
        none = False
        plot += gg.geom_point(color='#000000', shape='_', size=100)
    if yname and 'LINE' in ypar:
        none = False
        plot += gg.geom_line()
    if yname and (none or 'POINT' in ypar):
        none = False
        plot += gg.geom_point()
    assert not none, "Need something to plot!"
    
    fpar, flbl, fname = find('FACET') 
    if fname:
        plot += gg.facet_wrap(fname)
    xfpar, xflbl, xfname = find('XFACET')
    yfpar, yflbl, yfname = find('YFACET')
    if xfname or yfname:
        assert fname == None, "Too many facets"
        plot += gg.facet_grid(yfname, xfname)
    
    plot += gg.xlab(xlbl)
    if ylbl:
        plot += gg.ylab(ylbl)
    if 'LOG' in xpar:
        plot += gg.scale_x_log()
    if ypar and 'LOG' in ypar or 'LOGY' in xpar:
        plot += gg.scale_y_log()
        if 'HIST' in xpar:
            plot += gg.ylim(low=1)
        else:
            mini = min(y for y in data[yname] if y > 0)
            plot += gg.ylim(low=mini/2.0)
    
    plot.save(outfile, width=w, height=h)
