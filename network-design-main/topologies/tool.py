# Author: Alessandro Maissen

import topogen as tg
import analysis as an
from topogen import validate_hypercube as vhc
from topogen import validate_torus as vto
from topogen import validate_flatbutterfly as vfbf
from topogen import validate_mlfm as vmlfm
from topogen import validate_oft as voft
from topogen import validate_jellyfish as vjf
from topogen import validate_hyperx as vhx
from topogen import validate_dragonfly as vdf
from topogen import validate_xpander as vxp
from topogen import validate_fattree as vft
from topogen import validate_slimfly as vsf
from topogen import validate_delorme as vdl
from topogen import validate_brown as vbr
from topogen import validate_brown_ext as vbe
from topogen import validate_kautz as vka
from topogen import validate_arrangementNetwork as van
from topogen import validate_extendedGeneralizedFatTree as vxgft
from topogen import validate_karyn as vkaryn
from topogen import validate_mesh as vmesh
from topogen import validate_tofu as vtofu
from topogen import validate_cascadeDragonfly as vcdf
from topogen.common import clean_topologies
from analysis.results import ggplot, ggplot2, show
from analysis.analyse import analyse


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(prog='tool.py')
    subparser = parser.add_subparsers(help="type of operation", dest='type' ,required=True)

    # Topology Generator 
    parser_generate = subparser.add_parser("generate", help="generates a topology") 
    parser_generate_subparser = parser_generate.add_subparsers(help='type of topology', dest='type', required=True)

    topology_generator_parsers = []

    # Hypercube
    parser_generate_hypercube = parser_generate_subparser.add_parser("hypercube", help='generates a n-dimensional Hypercube topology')
    parser_generate_hypercube.add_argument('n', type=int, help='specifies number of dimensions')
    parser_generate_hypercube.set_defaults(func=tg.HypercubeGenerator().generate)
    topology_generator_parsers.append(parser_generate_hypercube)

    # Torus
    parser_generate_torus = parser_generate_subparser.add_parser("torus", help='generates a k-ary n-Torus topology')
    parser_generate_torus.add_argument('n', type=int, help='specifies number of dimensions')
    parser_generate_torus.add_argument('k', type=int, help='specifies number nodes per "edge"')
    parser_generate_torus.set_defaults(func=tg.TorusGenerator().generate)
    topology_generator_parsers.append(parser_generate_torus)

    # Flattened Butterfly
    parser_generate_flatbutterfly = parser_generate_subparser.add_parser("flatbutterfly", help='generates a k-ary n-flat (Flattened Butterfly)')
    parser_generate_flatbutterfly.add_argument('n', type=int, help='specifies number of dimensions')
    parser_generate_flatbutterfly.add_argument('k', type=int, help='specifies k')
    parser_generate_flatbutterfly.set_defaults(func=tg.FlatbutterflyGenerator().generate)
    topology_generator_parsers.append(parser_generate_flatbutterfly)

    # Multi-Layer Full-Mesh
    parser_generate_mlfm = parser_generate_subparser.add_parser("mlfm", help='generates a h-MLFM topology (Multi-Layer Full-Mesh)')
    parser_generate_mlfm.add_argument('h', type=int, help='specifies degree of local routers')
    parser_generate_mlfm.set_defaults(func=tg.MLFMGenerator().generate)
    topology_generator_parsers.append(parser_generate_mlfm)

    # Two-Level Orthogonal Fat-Tree
    parser_generate_oft = parser_generate_subparser.add_parser("oft", help='generates a k-OFT topology (Two-Level Orthogonal Fat-Tree)')
    parser_generate_oft.add_argument('k', type=int, help='specifies degree of routers in Layer 0 and Layer 2 (k:= q + 1 where q is prime)')
    parser_generate_oft.set_defaults(func=tg.OFTGenerator().generate)
    topology_generator_parsers.append(parser_generate_oft)

    # Jellyfish
    parser_generate_jellyfish = parser_generate_subparser.add_parser('jellyfish', help='generates a r-regular Jellyfish topology')
    parser_generate_jellyfish.add_argument('r', type=int, help='specifies network radix/degree of routers/nodes')
    parser_generate_jellyfish.add_argument('n', type=int, help='total number of routers/nodes')
    parser_generate_jellyfish.set_defaults(func=tg.JellyfishGenerator().generate)
    topology_generator_parsers.append(parser_generate_jellyfish)

    # HyperX
    parser_generate_hyperx = parser_generate_subparser.add_parser('hyperx', help='generates a regular HyperX topology')
    parser_generate_hyperx.add_argument('l', type=int, help='specifies number of dimensions')
    parser_generate_hyperx.add_argument('s', type=int, help='number of nodes per dimension')
    parser_generate_hyperx.set_defaults(func=tg.HyperXGenerator().generate)
    topology_generator_parsers.append(parser_generate_hyperx)

    # Dragonfly
    parser_generate_dragonfly = parser_generate_subparser.add_parser('dragonfly', help='generates a Dragonfly topology')
    parser_generate_dragonfly.add_argument('p', type=int, help='number of hosts per router')
    parser_generate_dragonfly.set_defaults(func=tg.DragonflyGenerator().generate)
    topology_generator_parsers.append(parser_generate_dragonfly)

    # FatTree
    parser_generate_fattree = parser_generate_subparser.add_parser('fattree', help='generates a FatTree topology')
    parser_generate_fattree.add_argument('k', type=int, help='network radix of routers (must be even)')
    parser_generate_fattree.set_defaults(func=tg.FatTreeGenerator().generate)
    topology_generator_parsers.append(parser_generate_fattree)

    # Xpander
    parser_generate_xpander = parser_generate_subparser.add_parser('xpander', help='generates a Xpander topology')
    parser_generate_xpander.add_argument('d', type=int, help='specifies the initial d-regular complete graph')
    parser_generate_xpander.add_argument('lifts', nargs='+', type=int, help='specifes the random lifts')
    parser_generate_xpander.set_defaults(func=tg.XpanderGenerator().generate)
    topology_generator_parsers.append(parser_generate_xpander)

    # SlimFly
    parser_generate_slimfly = parser_generate_subparser.add_parser('slimfly', help='generates a SlimFly topology')
    parser_generate_slimfly.add_argument('q', type=int, help='specifies the size of Gallois Field (q:=4w + delta where delta = -1 or 0 or 1 and q a prime power)')
    parser_generate_slimfly.set_defaults(func=tg.SlimFlyGenerator().generate)
    topology_generator_parsers.append(parser_generate_slimfly)

    # Delorme
    parser_generate_delorme = parser_generate_subparser.add_parser('delorme', help='generates a Delorme topology')
    parser_generate_delorme.add_argument('q', type=int, help='specifies the size of Gallois Field (q: size of Galois Field, q:= 2^(2*a-1), where a = 1,2,3,... and q an odd power of 2)')
    parser_generate_delorme.set_defaults(func=tg.DelormeGenerator().generate)
    topology_generator_parsers.append(parser_generate_delorme)

    # Brown
    parser_generate_brown = parser_generate_subparser.add_parser('brown', help='generates a Brown topology')
    parser_generate_brown.add_argument('q', type=int, help='specifies the size of Gallois Field (q: size of Galois Field, is a prime power')
    parser_generate_brown.set_defaults(func=tg.BrownGenerator().generate)
    topology_generator_parsers.append(parser_generate_brown)

    # Brown Extensions
    parser_generate_brown_ext = parser_generate_subparser.add_parser('brown_ext', help='generates incrmeental expansions of a Brown topology')
    parser_generate_brown_ext.add_argument('q', type=int, help='specifies the size of Gallois Field (q: size of Galois Field, is a prime power)')
    parser_generate_brown_ext.add_argument('r0', type=int, help='number of replications of cluster C0')
    parser_generate_brown_ext.add_argument('r1', type=int, help='round robin replication of a selected quadric and its neighbors(if r1>0, r0 is ignored)')
    parser_generate_brown_ext.set_defaults(func=tg.BrownExtGenerator().generate)
    topology_generator_parsers.append(parser_generate_brown_ext)

    # Bundlefly
    parser_generate_bundlefly   = parser_generate_subparser.add_parser('bundlefly', help='generates bundlefly')
    parser_generate_bundlefly.add_argument('q', type=int, help='degree')
    parser_generate_bundlefly.set_defaults(func=tg.BundleflyGenerator().generate)
    topology_generator_parsers.append(parser_generate_bundlefly)

    # Kautz
    parser_generate_kautz = parser_generate_subparser.add_parser('kautz', help='generates kautz')
    parser_generate_kautz.add_argument('b', type=int, help='base')
    parser_generate_kautz.add_argument('n', type=int, help='length')
    parser_generate_kautz.set_defaults(func=tg.KautzGenerator().generate)
    topology_generator_parsers.append(parser_generate_kautz)

    # Arrangement Network   
    parser_generate_arrnetwork = parser_generate_subparser.add_parser('arrnetwork', help='generates arrangement network')
    parser_generate_arrnetwork.add_argument('n', type=int, help='maximum integer')
    parser_generate_arrnetwork.add_argument('k', type=int, help='permutations')
    parser_generate_arrnetwork.set_defaults(func=tg.ArrangementNetworkGenerator().generate)
    topology_generator_parsers.append(parser_generate_arrnetwork)

    # Extended Generalized Fat Tree
    parser_generate_xgft = parser_generate_subparser.add_parser('xgft', help='generates extended generalized fat tree')
    parser_generate_xgft.add_argument('h', type=int, help='height')
    parser_generate_xgft.add_argument('inputs', nargs='+', type=int, help='specifes number of childs and parents per level. [c1,c2,...,ch,p1,p2,...,ph]')
    parser_generate_xgft.set_defaults(func=tg.ExtendedGeneralizedFatTreeGenerator().generate)
    topology_generator_parsers.append(parser_generate_xgft)

    # KaryN
    parser_generate_karyn = parser_generate_subparser.add_parser('karyn', help='generates k-ary-n Tree')
    parser_generate_karyn.add_argument('k', type=int, help='half the number of ports per switch')
    parser_generate_karyn.add_argument('n', type=int, help='numbers of levels in the tree')
    parser_generate_karyn.set_defaults(func=tg.KaryNGenerator().generate)
    topology_generator_parsers.append(parser_generate_karyn)

    # Mesh
    parser_generate_mesh = parser_generate_subparser.add_parser('mesh', help='generates Mesh k^n')
    parser_generate_mesh.add_argument('n', type=int, help='Number of dimensions')
    parser_generate_mesh.add_argument('k', type=int, help='Number of routers per edge')
    parser_generate_mesh.add_argument('g', type=int, default= 0, help='gap')
    parser_generate_mesh.set_defaults(func=tg.MeshGenerator().generate)
    topology_generator_parsers.append(parser_generate_mesh)

    # Tofu
    parser_generate_tofu = parser_generate_subparser.add_parser('tofu', help='generates Tofu 6D Tofu')
    parser_generate_tofu.add_argument('n', nargs='+', type=int, help='Array of dimension of mesh n1xn2x..xnN')
    parser_generate_tofu.set_defaults(func=tg.TofuGenerator().generate)
    topology_generator_parsers.append(parser_generate_tofu)

    # Cascade Dragonfly
    parser_generate_casdf = parser_generate_subparser.add_parser('casdf', help='generates Cascade Dragonfly (a=96,p=8,h=10) with g groups')
    parser_generate_casdf.add_argument('g', type=int, help='number of groups')
    parser_generate_casdf.set_defaults(func=tg.CascadeDragonflyGenerator().generate)
    topology_generator_parsers.append(parser_generate_casdf)

    # Spectralfly
    parser_generate_specfly = parser_generate_subparser.add_parser('specfly', help='construct lps graphs (spectralfly)')
    parser_generate_specfly.add_argument('p', type=int, help='parameter p, must be odd prime')
    parser_generate_specfly.add_argument('q', type=int, help='parameter q, must be odd prime distinct from p')
    parser_generate_specfly.set_defaults(func=tg.SpectralflyGenerator().generate)
    topology_generator_parsers.append(parser_generate_specfly)

    # Megafly
    parser_generate_megafly = parser_generate_subparser.add_parser('megafly', help='construct megafly')
    parser_generate_megafly.add_argument('g', type=int, help='total number of groups')
    parser_generate_megafly.add_argument('d', type=int, help='total radix, must be even')
    parser_generate_megafly.set_defaults(func=tg.MegaflyGenerator().generate)
    topology_generator_parsers.append(parser_generate_megafly)

    # Polarstar
    parser_generate_polarstar = parser_generate_subparser.add_parser('polarstar', help='construct polarstar')
    parser_generate_polarstar.add_argument('d', type=int, help='degree')
    parser_generate_polarstar.add_argument('pfq', type=int, help='Parameter for polarfly stucture graph')
    parser_generate_polarstar.add_argument('jq', type=int, help='Parameter for subgraph (bdf or paley)')
    parser_generate_polarstar.add_argument('sg', type=str, nargs = '?', choices=['bdf', 'paley', 'max'], default='max', help='subgraph')
    parser_generate_polarstar.set_defaults(func=tg.PolarstarGenerator().generate)
    topology_generator_parsers.append(parser_generate_polarstar)

    for sub in topology_generator_parsers:
        sub.add_argument('-v','--validate', action='store_true', help='validates the generated topology')
        sub.set_defaults(save=True)

    # end Topology Generator

    # Topology Validator
    parser_validate = subparser.add_parser("validate", help="validates a topology")
    parser_validate_subparser = parser_validate.add_subparsers(help='type of topology', dest='type', required=True)

    # Hypercube
    parser_validate_hypercube = parser_validate_subparser.add_parser("hypercube", help='validates random Hypercube topologies')
    parser_validate_hypercube.set_defaults(func=vhc.validate_hypercube)

    # Torus
    parser_validate_torus = parser_validate_subparser.add_parser("torus", help='validates random Torus topologies')
    parser_validate_torus.set_defaults(func=vto.validate_torus)

    # Flattened Butterfly
    parser_validate_flatbutterfly = parser_validate_subparser.add_parser("flatbutterfly", help='validates random Flattened Butterfly topologies')
    parser_validate_flatbutterfly.set_defaults(func=vfbf.validate_flatbutterfly)

    # Multi-Layer Full-Mesh
    parser_validate_mlfm = parser_validate_subparser.add_parser("mlfm", help='validates random MLFM topologies')
    parser_validate_mlfm.set_defaults(func=vmlfm.validate_mlfm)

    # Two-Level Orthogonal Fat-Tree
    parser_validate_oft = parser_validate_subparser.add_parser("oft", help='validates random OFT topologies')
    parser_validate_oft.set_defaults(func=voft.validate_oft)

    # Jellyfish
    parser_validate_jellfyfish = parser_validate_subparser.add_parser("jellyfish", help='validates random Jellyfish topologies')
    parser_validate_jellfyfish.set_defaults(func=vjf.validate_jellyfish)

    # HyperX
    parser_validate_hyperx = parser_validate_subparser.add_parser("hyperx", help='validates random HyperX topologies')
    parser_validate_hyperx.set_defaults(func=vhx.validate_hyperx)

    # Dragonfly
    parser_validate_dragonfly = parser_validate_subparser.add_parser("dragonfly", help='validates random Dragonfly topologies')
    parser_validate_dragonfly.set_defaults(func=vdf.validate_dragonfly)

    # Xpander
    parser_validate_xpander = parser_validate_subparser.add_parser("xpander", help='validates random Xpander topologies')
    parser_validate_xpander.set_defaults(func=vxp.validate_xpander)

    # Fat-Tree
    parser_validate_fattree = parser_validate_subparser.add_parser("fattree", help='validates random FatTree topologies')
    parser_validate_fattree.set_defaults(func=vft.validate_fattree)

    # SlimFly
    parser_validate_slimfly = parser_validate_subparser.add_parser("slimfly", help='validates random SlimFly topologies')
    parser_validate_slimfly.set_defaults(func=vsf.validate_slimfly)

    # Delorme
    parser_validate_slimfly = parser_validate_subparser.add_parser("delorme", help='validates Delorme topologies')
    parser_validate_slimfly.set_defaults(func=vdl.validate_delorme)

    # Brown
    parser_validate_slimfly = parser_validate_subparser.add_parser("brown", help='validates Brown topologies')
    parser_validate_slimfly.set_defaults(func=vbr.validate_brown)

    # Brown Extensions
    parser_validate_slimfly = parser_validate_subparser.add_parser("brown_ext", help='validates expanded Brown topologies')
    parser_validate_slimfly.set_defaults(func=vbe.validate_brown_ext)

    # end Topology Validator

    # Cleaning generated Toplogies 
    parser_clean = subparser.add_parser("clean", help='removes generated topologies')
    parser_clean.add_argument('-t', '--topos', type=str, nargs='+', default=[], help="all or topology folder e.g. hypercubes, tori,..")
    parser_clean.add_argument('-db', '--databases', type=str, nargs='+', default=[], choices=["all", "shortest_paths.db", "interference.db","edge_disjoint_paths.db", "low_connectivity.db"], help="all or databases")
    parser_clean.add_argument('-p', default=False, action='store_true', help="delete all the plotfiles (*_plot.pdf and *_plot.info)")
    parser_clean.add_argument('-a', default=False, action='store_true', help="delete all (topologies, databases and plots/plotinfos)")
    parser_clean.set_defaults(func=clean_topologies)

    # Topo information getter
    parser_info = subparser.add_parser("info", help="saves information about selected topologies")
    parser_info.add_argument('-t', '--topos', type=str, nargs='+', choices=[topo for topo in tg.toponames.keys() if topo != 'JF'], required=True, help="specifies the topologies")
    parser_info.add_argument('-c', '--classes', type=int, nargs='+', required=True, help="specifies the classes defining the number of host a topology have")
    parser_info.add_argument('-j', '--jellyfish', default=False, action='store_true', help="for each topology the jellyfish equivalent topology is also analysed")
    parser_info.set_defaults(func=an.common.getinfo)

    # Analysis
    parser_analyse = subparser.add_parser('analyse', help='analysing tool')
    parser_analyse_subparser = parser_analyse.add_subparsers(help='type of analysis', dest='type', required=True)
    
    parser_analyse_shortest_paths = parser_analyse_subparser.add_parser('shortestpaths' , help='analyses shortest paths')
    parser_analyse_shortest_paths.add_argument('-s', '--sparse', action='store_true', help='use sparse matrices')
    #parser_analyse_shortest_paths.add_argument('--lowmemory', action='store_true', help='memory efficient but slow')
    parser_analyse_shortest_paths.add_argument('--parallel', action='store_true', help='uses parallel matrix multiplication')
    parser_analyse_shortest_paths.set_defaults(analyse_function='shortestpaths')

    parser_analyse_disjoint_paths = parser_analyse_subparser.add_parser('disjointpaths' , help='analyses disjoint paths')
    parser_analyse_disjoint_paths.set_defaults(analyse_function='disjointpaths')
    parser_analyse_interference = parser_analyse_subparser.add_parser('interference' , help='analyses interference')
    #parser_analyse_interference.add_argument('-d', '--deterministic', action='store_true', help='use the deterministic algorithm to comupte interference')
    parser_analyse_interference.set_defaults(analyse_function='interference')

    for sub in [parser_analyse_shortest_paths, parser_analyse_disjoint_paths, parser_analyse_interference]:
        sub.add_argument('-t', '--topos', type=str, nargs='+', choices=[topo for topo in tg.toponames.keys() if topo != 'JF'], required=True, help="specifies the topologies")
        sub.add_argument('-c', '--classes', type=int, nargs='+', required=True, help="specifies the classes defining the number of host a topology have")
        sub.add_argument('-l', '--maxlength', type=int, default=5, help="specifies the maxiumum length of search space")
        sub.add_argument('-j', '--jellyfish', default=False, action='store_true', help="for each topology the jellyfish equivalent topology is also analysed")
        sub.set_defaults(func=analyse)


    # Analysis Plotter
    parser_plot = subparser.add_parser('plot', help='plotting tool')
    parser_plot_subparser = parser_plot.add_subparsers(help='type of plot', dest='type', required=True)

    # shorthest path plot & shorthest path multiplicity plot
    parser_plot_shortest_paths = parser_plot_subparser.add_parser('shortestpaths' , help='plots shortest paths')
    parser_plot_shortest_paths.set_defaults(func=an.ShortestPathPlotter().plot_shortestpath_length)

    parser_plot_shortest_paths_multiplicity = parser_plot_subparser.add_parser('multiplicity' , help='plots shortest paths multiplicity')
    parser_plot_shortest_paths_multiplicity.add_argument('-m', '--maxmultiplicity', type=int, default=5, help="bounds the x-axis of the plot")
    parser_plot_shortest_paths_multiplicity.set_defaults(func=an.ShortestPathPlotter().plot_shortestpath_multiplicity)

    for sub in [parser_plot_shortest_paths, parser_plot_shortest_paths_multiplicity]:
        sub.add_argument('-t', '--topos', type=str, nargs='+', choices=[topo for topo in tg.toponames.keys() if topo != 'JF'], required=True, help="specifies the topologies")
        sub.add_argument('-c', '--classes', type=int, nargs='+', required=True, help="specifies the classes defining the number of host a topology have")
        sub.add_argument('-l', '--maxlength', type=int, default=5, help="specifies the maxiumum length of search space")
        sub.add_argument('-j', '--jellyfish', default=False, action='store_true', help="for each topology the jellyfish equivalent topology is also analysed")
        sub.add_argument('-o', '--outfile', help='Output plot file name.', default="plot.pdf")
        sub.add_argument('--size', help='Plot size (e.g. 10x12, inches).', default=None)
        sub.add_argument('-d', '--density', default=False, action='store_true', help="Plots shoud show density instead of raw values")

    # disjoint paths & interference 
    parser_plot_disjoint_paths = parser_plot_subparser.add_parser('disjointpaths' , help='plots histogram of disjoint paths')
    parser_plot_disjoint_paths.set_defaults(func=an.EdgeDisjointPathPlotter().plot_edge_disjoint_path_count)

    parser_plot_interference = parser_plot_subparser.add_parser('interference' , help='plots histogram showing interference')
    parser_plot_interference.set_defaults(func=an.InterferencePlotter().plot_interference)

    parser_plot_interference_detail = parser_plot_subparser.add_parser('interferencedetail' , help='plots histogram showing interference')
    parser_plot_interference_detail.set_defaults(func=an.InterferencePlotter().plot_interference_detail)

    for sub in [parser_plot_disjoint_paths, parser_plot_interference, parser_plot_interference_detail]:
        sub.add_argument('-t', '--topos', type=str, nargs='+', choices=[topo for topo in tg.toponames.keys() if topo != 'JF'], required=True, help="specifies the topologies")
        sub.add_argument('-c', '--c', type=int, required=True, help="specifies the class defining the number of host a topology have")
        sub.add_argument('-l', '--maxlength', type=int, default=5, help="specifies the maxiumum length of search space")
        sub.add_argument('-j', '--jellyfish', default=False, action='store_true', help="for each topology the jellyfish equivalent topology is also analysed")
        sub.add_argument('-o', '--outfile', help='Output plot file name.', default="plot.pdf")
        sub.add_argument('--size', help='Plot size (e.g. 10x12, inches).', default=None)
        sub.add_argument('-d', '--density', default=False, action='store_true', help="Plots shoud show density instead of raw values")


    # low connectivity 
    parser_plot_low_connectivity = parser_plot_subparser.add_parser('lowconnectivity' , help='low connectivity plot')
    parser_plot_low_connectivity.add_argument('-t', '--topos', type=str , nargs='+', choices=[topo for topo in tg.toponames.keys() if topo != 'JF'], required=True, help="specifies the topologies")
    parser_plot_low_connectivity.add_argument('-c', '--classes', type=int, nargs='+', required=True, help="specifies the classes defining the number of host a topology have")
    parser_plot_low_connectivity.add_argument('-l', '--length', type=int, nargs='+', default=[5], help ="path lengths for plot")
    parser_plot_low_connectivity.add_argument('-f', '--factor', type=float, default=0.75, help="cut off for connection. Only plot connections <= cutOff")
    parser_plot_low_connectivity.add_argument('-o', '--outfile', help='Output plot file name.', default="plot.pdf")
    parser_plot_low_connectivity.add_argument('--size', help='Plot size (e.g. 10x12, inches).', default=None)
    parser_plot_low_connectivity.add_argument('-ne', '--noEdges', default=False, action='store_true', help='Do not show edges in Plots where l > 1.')
    parser_plot_low_connectivity.add_argument('-dt', '--detailedTicks', default=False, action='store_true', help='Shows number value of connectivity percentage on legend')
    parser_plot_low_connectivity.add_argument('-ns', '--normalizedScale', default=False, action='store_true', help='Normalize legend from 0.0 to 1.0 for plot')
    parser_plot_low_connectivity.set_defaults(func=an.EdgeDisjointPathPlotter().plot_low_connectivity)


    # Plotting and database
    parser_show = subparser.add_parser('show', help='Execute a SQL query and show the results.')
    parser_show.add_argument('--explain', help='Only show EXPLAIN output.', action='store_true')
    parser_show.add_argument('--limit', help='Limit to this number of results (0 for no limit).', type=int, default=100)
    parser_show.set_defaults(func=show)
    
    parser_ggplot = subparser.add_parser('ggplot', help='Execute a SQL query and plot results using python-ggplot. Uses matplotlib, pandas and the ggplot package.')
    parser_ggplot.set_defaults(func=ggplot)
    
    parser_ggplot2 = subparser.add_parser('ggplot2', help='Execute a SQL query and plot results using R ggplot2. Requires sqldf and ggplot2 for R.')
    parser_ggplot2.set_defaults(func=ggplot2)
    parser_ggplot2.add_argument('--manual', help='Do not run R, just generate script and data.', action='store_true')
    
    for sub in [parser_ggplot, parser_ggplot2]:
        sub.add_argument('-o', '--outfile', help='Output plot file name.', default="plot.pdf")
        sub.add_argument('--size', help='Plot size (e.g. 10x12, inches).', default="12x10")
    
    for sub in [parser_show, parser_ggplot, parser_ggplot2]:
        sub.add_argument('-f', '--datafile', help='SQLite file to operate on', default="results.db")
        sub.add_argument('--sql', help='Use this complete SQL query.', default=None)
        sub.add_argument('--runsql', help='Use this SQL SELECT to select runs.', default=None)
        sub.add_argument('--datasql', help='Use this SQL SELECT to select datapoints.', default=None)
        sub.add_argument('-r', '--runwhere', help='Use this SQL WHERE clause to select runs.', default=None)
        sub.add_argument('-w', '--where', help='Use this SQL WHERE clause to select datapoints.', default=None)
        sub.add_argument('-s', '--select', help='Output these columns.', default='*, count(*)')
        sub.add_argument('-g', '--group', help='Group the result by run.', action='store_true')
        sub.add_argument('-i', '--ignore', help='Group by all columns except this. Can be used multiple times.', action='append')
    


    # Parsing arguments and invoke function
    kwargs = parser.parse_args()
    func = kwargs.func
    del kwargs.func
    del kwargs.type # because dest
    func(**kwargs.__dict__)
