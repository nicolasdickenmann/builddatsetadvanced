from .Plotter import Plotter
from .common import make_topos, find_runs
from .EdgeDisjointPathAnalysis import EdgeDisjointPathAnalyis
from .results import Results, pyplot 


class EdgeDisjointPathPlotter(Plotter):

    def __init__(self):
        super(EdgeDisjointPathPlotter,self).__init__()

    def plot_edge_disjoint_path_count(self, topos : [str], c : int, maxlength : int, jellyfish : bool, outfile = "plot.pdf", size = None, density=False):
        
        networks = make_topos(topos,[c],jellyfish)

        ed_analysis = EdgeDisjointPathAnalyis()
        ed_analysis.analyse(networks,maxlength)
        self.plotted_topologies_info(outfile,networks)

        res = Results(ed_analysis.datafile)

        runids = find_runs(networks,res,"connectivity", maxlength)
        runids = "(" + ", ".join(str(x) for x in runids) + ")"

        runwhere = "runid in " + runids
        select = 'c_ab, "l="||len, case when topo like "JF-%" then substr(topo, 4) || "-JF" else topo end'
        where = 'len <=' + str(maxlength)

        if size is None:
            size = str((maxlength + 1) * 1.5) + "x" + str(1.25 * (len(networks)+1))

        pyplot(outfile=outfile, size=size, manual=False, datafile=ed_analysis.datafile, select=select, runwhere=runwhere, where=where, plotType='edge_disjoint_path_count', density=density, label="Diversity (count) of non-minimal paths $c_{i}(A,B)$ \n $N = " + str(c) + "$", maxlength=maxlength, sqlLength=3, jellyfish=jellyfish)

    def plot_low_connectivity(self, topos : [str], classes : [int], length : [int], factor=0.75, outfile = "plot.pdf", size = None, noEdges = False, detailedTicks  = False, normalizedScale = False):
        assert(factor > 0 and factor <= 1)

        for topo in topos:
            for c in classes:
                # rename if multiple plots are done
                if (len(topos) > 1 or len(classes) > 1):
                    outfile = "lowConnectivity_" + str(c) + "_" + topo + '_plot.pdf'

                networks = make_topos([topo],[c], False)

                ed_analysis = EdgeDisjointPathAnalyis("low_connectivity.db", all_combinations=True)
                ed_analysis.analyse(networks,max(length))
                self.plotted_topologies_info(outfile,networks)

                res = Results(ed_analysis.datafile)

                runids = find_runs(networks,res,"connectivity", max(length))
                runids = "(" + ", ".join(str(x) for x in runids) + ")"
               
                length.sort()

                if size is None:
                    size = "8x8"

                runwhere = "runid in " + runids

                for l in length:
                    where = '(len = ' + str(l) + ' and c_ab <= r*' + str(factor) +')'
                    select = "b, a as [X; s  \n \n l = " + str(l) + " and c_l({s},{t}) / r' <= " + str(int(factor * 100))+ "%], round(c_ab*100.0/r,1)||'%', topo || ' R=' || n_r || ' N=' || n_e || ' net-radix=' || r,case when len = 1 and c_ab > 0 then 'Edge' else 'Path' end"

                    label = "$l = " + str(l) + "$ and $\\frac{c_{l}(\{s\},\{t\})}{ r'} \leq " + str(int(factor * 100)) + "\%$"

                    if not noEdges:
                        where = where+"or (len=1 and c_ab > 0)"
                        label = label + "\nor ($len = 1$ and $c_{ab} > 0$)"

                    if len(length) > 1:
                        outfile = 'lowConnectivity_' + str(c) + '_' + topo + '_' + str(l) + '_plot.pdf'

                    pyplot(outfile=outfile, size=size, manual=False, datafile=ed_analysis.datafile, select=select, runwhere=runwhere, where=where, plotType='low_connectivity',density=False, detailedTicks=detailedTicks, normalizedScale=normalizedScale, label=label, maxlength=l, sqlLength=5, jellyfish=False) 
