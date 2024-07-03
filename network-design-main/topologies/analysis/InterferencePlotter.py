from .Plotter import Plotter
from .common import make_topos, find_runs
from .InterferenceAnalyisis import InterferenceAnalysis
from .results import Results, pyplot

class InterferencePlotter(Plotter):

    def __init__(self):
        super(InterferencePlotter,self).__init__()

    def plot_interference(self, topos : [str], c : int, maxlength : int, jellyfish : bool, outfile = "plot.pdf", size = None, density = False):

        networks = make_topos(topos,[c],jellyfish)

        if_analysis = InterferenceAnalysis()
        if_analysis.analyse(networks,maxlength)
        self.plotted_topologies_info(outfile,networks)

        res = Results(if_analysis.datafile)

        runids = find_runs(networks,res,"interference", maxlength)
        runids = "(" + ", ".join(str(x) for x in runids) + ")"

        runwhere = "runid in " + runids
        select = 'x_abcd, "l="||len, case when topo like "JF-%" then substr(topo, 4) || "-JF" else topo end'
        where = 'len <=' + str(maxlength)
        label = "interference $I^{l}_{ab,cd}$ \n $N = " + str(c) + "$"

        if size is None:
            size = str((maxlength + 1) * 1.5) + "x" + str(1.25 * (len(networks)+1))
         

        pyplot(outfile=outfile, size=size, manual=False, datafile=if_analysis.datafile, select=select, runwhere=runwhere, where=where, plotType='interference', density=density, label=label, maxlength=maxlength, sqlLength=3, jellyfish=jellyfish, classes=[c])

    def plot_interference_detail(self, topos : [str], c : int, maxlength : int, jellyfish : bool, outfile = "plot.pdf", size = None, density=False):

        networks = make_topos(topos,[c],jellyfish)

        if_analysis = InterferenceAnalysis()
        if_analysis.analyse(networks,maxlength)
        self.plotted_topologies_info(outfile,networks)

        res = Results(if_analysis.datafile)

        runids = find_runs(networks,res,"interference", maxlength)
        runids = "(" + ", ".join(str(x) for x in runids) + ")"

        runwhere = "runid in " + runids
        select = 'c_acd+c_acb, c_abcd, "l="||len, case when topo like "JF-%" then substr(topo, 4) || "-JF" else topo end'
        where = 'len <= '+ str(maxlength)
        label = "$c_{l}(\{a,c\},\{b\}) + c_l(\{a,c\},\{d\})$ \n $N=" + str(c) + "$"
        if size is None:
            size = str((maxlength+1) * 1.5) + "x" + str((len(networks)+1) * 1.5) 

        pyplot(outfile=outfile, size=size, manual=False, datafile=if_analysis.datafile, select=select, runwhere=runwhere, where=where, plotType='interference_detail', density=density, label=label, maxlength=maxlength, sqlLength=4, jellyfish=jellyfish, classes=[c])
