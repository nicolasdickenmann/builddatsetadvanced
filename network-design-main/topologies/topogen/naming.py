# Author: Alessandro Maissen

prefix = "data/"

topo_folders = {
    'HC' : "hypercubes/",
    'Torus' : "tori/",
    'FB' : "flatbutterflies/",
    'MLFM': "mlfms/",
    'OFT' : "ofts/",
    'JF' : "jellyfishes/",
    'HX' : "hyperxs/",
    'DF' : "dragonflies/",
    'Xpander' : "xpanders/",
    'FT' : 'fattrees/',
    'BUNDLE' : 'bundleflies/',
    'KAUTZ' : 'kautz/',
    'AN' : 'arrangementNetworks/',
    'XGFT' : 'extGenFatTrees/',
    'KARYN' : 'karynTrees/',
    'MESH' : 'meshes/',
    'EXPMESH' : 'meshes/',
    'TOFU' : 'tofu/',
    'CASDF' : 'casDragonflies/',
    'SPECFLY' : 'spectralflies/',
    'MEGAFLY' : 'mageflies/',
    'POLARFLY' : 'polarflies/'
}

topo_filenames = {
    'HC' : lambda n: str(n) + "DHypercube.adj.txt",
    'Torus' : lambda n,k: str(n) + "DTorus." + str(k) + ".adj.txt",
    'FB' : lambda n,k: str(n) + "DFlatButterfly." + str(k) + ".adj.txt",
    'MLFM': lambda h: "MLFM." + str(h) + ".adj.txt",
    'OFT' : lambda k: "OFT." + str(k) + ".adj.txt",
    'JF' : lambda nr, R: "Jellyfish." + str(nr) + "." + str(R) + ".adj.txt",
    'HX' : lambda l, s: "HyperX" + str(l) + "." + str(s) + ".adj.txt",
    'DF' : lambda p: "Dragonfly." + str(p) + ".adj.txt",
    'Xpander' : lambda d, lifts: "Xpander." + str(d) + ".lifts." + ".".join(str(lift) for lift in lifts) + ".adj.txt",
    'FT' : lambda k: "FatTree." + str(k) + ".adj.txt",
    'BUNDLE' : lambda q: "Bundlefly." + str(q) + ".adj.txt",
    'KAUTZ' : lambda b,n: str(b) + "Kautz." + str(n) + ".adj.txt",
    'AN' : lambda n,k: str(n) + "arrNetwork." + str(k) + ".adj.txt",
    'XGFT' : lambda h,inputs: str(h) + ".xgft.(" + ".".join(str(i) for i in inputs[:h]) + ")(" + ".".join(str(i) for i in inputs[h:]) + ").adj.txt",
    'KARYN' : lambda k, n : str(k) + "ary" + str(n) + ".adj.txt",
    'MESH' : lambda n,k : "Mesh" + str(n) + "." + str(k) + ".adj.txt",
    'EXPMESH' : lambda n,k,g,: "ExpMesh" + str(n) + "." + str(k) + "gap" + str(g) + ".adj.txt",
    'TOFU' : lambda d1,d2,d3 : "Tofu6D.(" + str(d1) + "," + str(d2) + "," + str(d3) + ",2,3,2).adj.txt",
    'CASDF' : lambda g : str(g) + ".casDF.adj.txt",
    'SPECFLY' : lambda p,q : "Spectralfly." + str(p) + "_"  + str(q) + ".adj.txt",
    'MEGAFLY' : lambda d,g : "Megafly." + str(d) + "_"  + str(g) + ".adj.txt",
    'POLARFLY' : lambda pfq, jq, sg : "Polarfly." + str(pfq) + "." + str(jq) + "." + sg + ".adj.txt"
}

topo_folderpath = lambda topo: prefix + str(topo_folders[topo])
