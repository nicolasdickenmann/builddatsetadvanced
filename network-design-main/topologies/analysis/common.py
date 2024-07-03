# Author: Alessandro Maissen

from .results import Results
import topogen
from topogen import toponames


# creates list of topologies given classes and names
def make_topos(topos : [str], classes : [int], jellyfish : bool):

    networks = []
    for topo in topos:
        for c in classes:
            if jellyfish:
                network = toponames[topo](N=c)
                networks.append(network)
                networks.append(network.get_jellyfish_eq())
            else:
                networks.append(toponames[topo](N=c))
    return networks

def is_in_db(topo, results : Results, maxLength : int):
    
    if next(results.conn.execute("SELECT COUNT(*) from runs;"))[0]:
        # not empty database
        count = results.conn.execute("SELECT COUNT(*) FROM runs WHERE runs.topo LIKE '%s' AND n_r = %d AND runs.n_e = %d AND runs.r = %d AND runs.maxlen >= %d;" %(topo.name, topo.R, topo.N, topo.nr, maxLength))
        return next(count)[0]
    else:
        return 0

def find_runs(networks, results : Results, tag, maxlength):
    
    runids = []
    for network in networks:
        runid = results.conn.execute("SELECT runid FROM runs WHERE runs.topo LIKE '%s' AND n_r = %d AND runs.n_e = %d AND runs.r = %d AND runs.tag LIKE '%s' AND runs.maxlen >= %d ORDER BY runs.maxlen ASC;" %(network.name, network.R, network.N, network.nr, tag, maxlength))
        runids.append(next(runid)[0])

    return runids

def getinfo(topos : [str], classes : [int], jellyfish : bool):
    
    f=open("sizes.info","w+")
    f.write("name r p N R \n")
    for topo in topos:
        f.write(topo + " & ")
        for i in range(len(classes) - 1):
            net = make_topos([topo], [classes[i]], False)[0]
            f.write("%d & %d & %d & %d & " %(net.p, net.r, net.R, net.N))
        net = make_topos([topo], [classes[len(classes) - 1]], False)[0]
        f.write("%d & %d & %d & %d \\\\ \n" %(net.p, net.r, net.R, net.N))

        if jellyfish:
            f.write(topo + "-JF & ")
            for i in range(len(classes) - 1):
                net = make_topos([topo], [classes[i]], True)[1]
                f.write("%d & %d & %d & %d & " %(net.p, net.r, net.R, net.N))
            net = make_topos([topo], [classes[len(classes) - 1]], False)[0]
            f.write("%d & %d & %d & %d \\\\ \n" %(net.p, net.r, net.R, net.N))