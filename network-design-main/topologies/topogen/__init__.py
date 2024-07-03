from .HypercubeGenerator import HypercubeGenerator
from .TorusGenerator import TorusGenerator
from .FlatbutterflyGenerator import FlatbutterflyGenerator
from .MLFMGenerator import MLFMGenerator
from .OFTGenerator import OFTGenerator
from .JellyfishGenerator import JellyfishGenerator
from .HyperXGenerator import HyperXGenerator
from .DragonflyGenerator import DragonflyGenerator
from .FatTreeGenerator import FatTreeGenerator
from .XpanderGenerator import XpanderGenerator
from .SlimFlyGenerator import SlimFlyGenerator
from .DelormeGenerator import DelormeGenerator
from .BrownGenerator import BrownGenerator
from .BrownExtGenerator import BrownExtGenerator
from .BundleflyGenerator import BundleflyGenerator
from .KautzGenerator import KautzGenerator
from .ArrangementNetworkGenerator import ArrangementNetworkGenerator
from .ExtendedGeneralizedFatTreeGenerator import ExtendedGeneralizedFatTreeGenerator
from .KaryNGenerator import KaryNGenerator
from .MeshGenerator import MeshGenerator
from .TofuGenerator import TofuGenerator
from .CascadeDragonflyGenerator import CascadeDragonflyGenerator
from .SpectralflyGenerator import SpectralflyGenerator
from .MegaflyGenerator import MegaflyGenerator
from .PolarstarGenerator import PolarstarGenerator

from .Hypercube import Hypercube
from .Torus import Torus
from .Flatbutterfly import Flatbutterfly
from .MLFM import MLFM
from .OFT import OFT
from .Jellyfish import Jellyfish
from .HyperX import HyperX
from .Dragonfly import Dragonfly
from .FatTree import FatTree
from .FatTree import FatTree2x
from .Xpander import Xpander
from .SlimFly import SlimFly
from .Delorme import Delorme
from .Brown import Brown
from .BrownExt import BrownExt
from .Bundlefly import Bundlefly
from .Kautz import Kautz
from .ArrangementNetwork import ArrangementNetwork
from .ExtendedGeneralizedFatTree import ExtendedGeneralizedFatTree
from .KaryN import KaryN
from .Mesh import Mesh
from .Tofu import Tofu
from .CascadeDragonfly import CascadeDragonfly
from .Spectralfly import Spectralfly
from .Megafly import Megafly
from .Polarstar import Polarstar

toponames = {
    'HC' : lambda n = -1, N = -1: Hypercube(n,N),
    '3DTorus' : lambda k = -1, N = -1: Torus(3,k,N),
    '4DTorus' : lambda k = -1, N = -1: Torus(4,k,N),
    '5DTorus': lambda k = -1, N = -1: Torus(5,k,N),
    '6DTorus': lambda k = -1, N = -1: Torus(6,k,N),
    '1DFB' : lambda k = -1, N = -1: Flatbutterfly(2,k,N),
    '2DFB' : lambda k = -1, N = -1: Flatbutterfly(3,k,N),
    '3DFB' : lambda k = -1, N = -1: Flatbutterfly(4,k,N),
    '4DFB' : lambda k = -1, N = -1: Flatbutterfly(5,k,N),
    '5DFB' : lambda k = -1, N = -1: Flatbutterfly(6,k,N),
    '6DFB' : lambda k = -1, N = -1: Flatbutterfly(7,k,N),
    'MLFM': lambda h = -1, N = -1: MLFM(h,N),
    'OFT' : lambda k = -1, N = -1: OFT(k,N),
    'JF' : lambda nr, R, p: Jellyfish(nr,R,p),
    'HX2' : lambda s = -1, N = -1: HyperX(2,s,N),
    'HX3' : lambda s = -1, N = -1: HyperX(3,s,N),
    'DF' : lambda p = -1, N = -1: Dragonfly(p,N),
    'Xp' : lambda N = -1 : Xpander(N=N, lifting_strategy='simple'),
    'Xpp' : lambda N = -1 : Xpander(N=N, lifting_strategy='2-lifts'),
    'FT' : lambda k = -1, N = -1: FatTree(k,N),
    'FT2x' : lambda k = -1, N = -1: FatTree2x(k,N),
    'SF' : lambda q = -1, N = -1: SlimFly(q,N),
    'DEL': lambda q = -1, N = -1: Delorme(q,N),
    'BRO': lambda q = -1, N = -1: Brown(q,N),
    'BRO_EXT' : lambda q = -1, N =-1, r0 = -1, r1 = -1: BrownExt(q,r0,r1,N),
    'BUNDLE'  : lambda q = -1, N = -1 : Bundlefly(q, N),
    '2KAUTZ' : lambda n = -1, N = -1 : Kautz(2,n,N),
    '3KAUTZ' : lambda n = -1, N = -1 : Kautz(3,n,N),
    '4KAUTZ' : lambda n = -1, N = -1 : Kautz(4,n,N),
    '5KAUTZ' : lambda n = -1, N = -1 : Kautz(5,n,N),
    '6KAUTZ' : lambda n = -1, N = -1 : Kautz(6,n,N),
    '8KAUTZ' : lambda n = -1, N = -1 : Kautz(8,n,N),
    'KAUTZ': lambda b = -1, n = -1, N = -1 : Kautz(b,n,N),
    'AN' : lambda n = -1, k = -1, N = -1 : ArrangementNetwork(n,k,N),
    '2AN' : lambda n = -1, k = 2, N = -1 : ArrangementNetwork(n,k,N),
    '3AN' : lambda n = -1, k = 3, N = -1 : ArrangementNetwork(n,k,N),
    '4AN' : lambda n = -1, k = 4, N = -1 : ArrangementNetwork(n,k,N),
    '5AN' : lambda n = -1, k = 5, N = -1 : ArrangementNetwork(n,k,N),
    '6AN' : lambda n = -1, k = 6, N = -1 : ArrangementNetwork(n,k,N),
    '8AN' : lambda n = -1, k = 8, N = -1 : ArrangementNetwork(n,k,N),
    '16AN' : lambda n = -1, k = 16, N = -1 : ArrangementNetwork(n,k,N),
    'XGFT4' : lambda h = -1, N = -1, inputs=None, variant = -1: ExtendedGeneralizedFatTree(h,inputs,N, '4'),
    'XGFT8' : lambda h = -1, N = -1, inputs=None, variant = -1: ExtendedGeneralizedFatTree(h,inputs,N,'8'),
    'XGFT8S' : lambda h = -1, N = -1, inputs=None, variant = -1: ExtendedGeneralizedFatTree(h,inputs,N, '8S'),
    'XGFT' : lambda h = -1, N = -1, inputs=None, variant = -1: ExtendedGeneralizedFatTree(h,inputs,N, variant),
    'KARYN' : lambda k = -1, n = -1, N = -1 : KaryN(k,n,N),
    'KARY2' : lambda k = -1, n = -1, N = -1 : KaryN(k,2,N),
    'KARY3' : lambda k = -1, n = -1, N = -1 : KaryN(k,3,N),
    'KARY4' : lambda k = -1, n = -1, N = -1 : KaryN(k,4,N),
    'KARY5' : lambda k = -1, n = -1, N = -1 : KaryN(k,5,N),
    'KARY6' : lambda k = -1, n = -1, N = -1 : KaryN(k,6,N),
    'KARY7' : lambda k = -1, n = -1, N = -1 : KaryN(k,7,N),
    'KARY8' : lambda k = -1, n = -1, N = -1 : KaryN(8,n,N),
    'KARY16' : lambda k = -1, n = -1, N = -1 : KaryN(16,n,N),
    '8ARYN' : lambda k = -1, n = -1, N = -1 : KaryN(8,n,N),
    '16ARYN' : lambda k = -1, n = -1, N = -1 : KaryN(16,n,N),
    '2dMESH' : lambda n = 2, k = -1, g = 0, N =-1 : Mesh(n,k,g,N),
    '3dMESH' : lambda n = 3, k = -1, g = 0, N =-1 : Mesh(n,k,g,N),
    '4dMESH' : lambda n = 4, k = -1, g = 0, N =-1 : Mesh(n,k,g,N),
    '5dMESH' : lambda n = 5, k = -1, g = 0, N =-1 : Mesh(n,k,g,N),
    '6dMESH' : lambda n = 6, k = -1, g = 0, N =-1 : Mesh(n,k,g,N),
    '2dExpMESH2' : lambda n = 2, k = -1, g = 2, N =-1 : Mesh(n,k,g,N),
    '3dExpMESH2' : lambda n = 3, k = -1, g = 2, N =-1 : Mesh(n,k,g,N),
    '4dExpMESH2' : lambda n = 4, k = -1, g = 2, N =-1 : Mesh(n,k,g,N),
    '5dExpMESH2' : lambda n = 5, k = -1, g = 2, N =-1 : Mesh(n,k,g,N),
    '6dExpMESH2' : lambda n = 6, k = -1, g = 2, N =-1 : Mesh(n,k,g,N),
    '2dExpMESH3' : lambda n = 2, k = -1, g = 3, N =-1 : Mesh(n,k,g,N),
    '3dExpMESH3' : lambda n = 3, k = -1, g = 3, N =-1 : Mesh(n,k,g,N),
    '4dExpMESH3' : lambda n = 4, k = -1, g = 3, N =-1 : Mesh(n,k,g,N),
    '5dExpMESH3' : lambda n = 5, k = -1, g = 3, N =-1 : Mesh(n,k,g,N),
    '6dExpMESH3' : lambda n = 6, k = -1, g = 3, N =-1 : Mesh(n,k,g,N),
    '2dExpMESH4' : lambda n = 2, k = -1, g = 4, N =-1 : Mesh(n,k,g,N),
    '3dExpMESH4' : lambda n = 3, k = -1, g = 4, N =-1 : Mesh(n,k,g,N),
    '4dExpMESH4' : lambda n = 4, k = -1, g = 4, N =-1 : Mesh(n,k,g,N),
    '5dExpMESH4' : lambda n = 5, k = -1, g = 4, N =-1 : Mesh(n,k,g,N),
    '6dExpMESH4' : lambda n = 6, k = -1, g = 4, N =-1 : Mesh(n,k,g,N),
    'TOFU' : lambda n = -1, N = -1 : Tofu(n, N),
    'CASDF' : lambda g = -1, N = -1 : CascadeDragonfly(g, N),
    'SPECFLY' : lambda p = -1, q = -1, N = -1 : Spectralfly(p,q,N),
    'MEGAFLY2' : lambda d = -1, g = 2, N = -1 : Megafly(g,d,N),
    'MEGAFLY3' : lambda d = -1, g = 3, N = -1 : Megafly(g,d,N),
    'MEGAFLY4' : lambda d = -1, g = 4, N = -1 : Megafly(g,d,N),
    'MEGAFLY8' : lambda d = -1, g = 8, N = -1 : Megafly(g,d,N),
    'MEGAFLY16' : lambda d = -1, g = 16, N = -1 : Megafly(g,d,N),
    'MEGAFLY32' : lambda d = -1, g = 32, N = -1 : Megafly(g,d,N),
    'POLARSTARmax' : lambda d = -1, pfq = -1, jq = -1, sg = 'max', N = -1 : Polarstar(d,pfq,jq,sg,N),
    'POLARSTARbdf' : lambda d = -1, pfq = -1, jq = -1, sg = 'bdf', N = -1 : Polarstar(d,pfq,jq,sg,N),
    'POLARSTARpaley' : lambda d = -1, pfq = -1, jq = -1, sg = 'paley', N = -1 : Polarstar(d,pfq,jq,sg,N)
    }
