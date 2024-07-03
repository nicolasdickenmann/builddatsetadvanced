# Author: Marcel Schneider
# Plot function using R ggplot2.
from .results import plotdata
import subprocess
from tempfile import NamedTemporaryFile

PRINTTHEME = True
histz = False

def ggplot(outfile, size, manual, **kwargs):
    w, h = [float(x) for x in size.split("x", 1)]

    conn, sql = plotdata(**kwargs)
    header = sql + " LIMIT 0"
    c = conn.execute(header)
    cols  = [d[0] for d in c.description]
    paras = [c.split(';', 1) for c in cols]
    paras = [(c[0].split(' '), c[1] if len(c) > 1 else c[0], name) for c, name in zip(paras, cols)]
    rname = {c : 'C%d' % i for i, c in enumerate(cols)}
    
    # DB name is added later, once we have the temp db. 
    rcode = ["library(sqldf)",
             "library(ggplot2)",
             "labels <- sqldf('SELECT * FROM labels', dbname='%s')",
             "data   <- sqldf('SELECT * FROM data', dbname='%s')",
             "plot   <- ("] # to allow arbitrary linebreaks
    
    aes = dict()
    labs = dict()
    
    def matchrule(key, action):
        for kw, lab, col in paras:
            if all(k in kw for k in key): action(kw, lab, col)
            
    def setcol(key):
        def setit(kw, lab, col):
            assert key not in aes, "Multiple values for %s (%s and %s)" % (key, aes[key], col)
            aes[key] = rname[col]
            labs[key] = "labels[1,'%s']" % rname[col]
            if lab == "": labs[key] = "''" # to hide the guide later
        return setit
    
    def hist(kw, lab, name):
        count = ("alpha" if "fill" in aes else "fill") if "y" in aes else "y"
        if "NORM" in kw: 
            aes[count] = "1e2*(..count..)/tapply(..count..,..PANEL..,sum)[..PANEL..]"
            labs[count] = "'fraction (%)'"
        else:
            aes[count] = "..count.."
            labs[count] = "'count'"
        args = "aes(%s), " % ", ".join(k + "=" + v for k,v in aes.items())
        if "INT" in kw: args += "binwidth=1, origin=-0.5, "
        if count == "y":   rcode.append("+ geom_histogram(%sposition='dodge', colour='black', size=0.1)" % args)
        else:            rcode.append("+ geom_bin2d(%s)" % args)
        if "LOGZ" in kw: 
            #rcode.append("+ scale_%s_continuous(trans='log', type = 'viridis')" % count)
            rcode.append("+ scale_%s_continuous(trans='log',  low='black', high='grey')" % count)
            global histz
            histz=True
            #labs[count] = "''" # hide LOGZ label, unreadable anyways.
    
    matchrule(["X"],     setcol("x"))
    matchrule(["COLOR"], setcol("colour"))
    matchrule(["SHAPE"], setcol("shape"))
    matchrule(["FILL"],  setcol("fill"))
    matchrule(["LABEL"], setcol("label"))
    matchrule(["Y", "HIST"], setcol("y")) # only for 2D HIST, where multiple y make no sense
    matchrule(["Y"], lambda _,__,col: "y" in labs or labs.update(y="labels[1,'%s']" % rname[col]))
    
    #if PRINTTHEME and "colour" in aes: del aes["colour"]
    rcode.append("ggplot(data, aes(%s))" % ", ".join(k + "=" + v for k,v in aes.items()))
    
    matchrule(["X", "HIST"], hist)
    
    rcode.append("+ labs(%s)"            % ", ".join(k + "=" + v for k,v in labs.items()))
            
    matchrule(["Y", "BAR"],   lambda _,__,y: rcode.append("+ geom_bar(aes(y=%s), stat='identity', position='identity')" % rname[y]))
    # legend for shape uses wrong draw_key here
    matchrule(["Y", "BOX"],   lambda _,__,y: rcode.append("+ geom_boxplot(aes(y=%s), outlier.shape=NULL)" % rname[y]))
    matchrule(["Y", "VIOLIN"],lambda _,__,y: rcode.append("+ geom_violin (aes(y=%s))" % rname[y]))
    matchrule(["Y", "LINE"],  lambda _,__,y: rcode.append("+ geom_line   (aes(y=%s))" % rname[y]))
    matchrule(["Y", "LINEDASH"],  lambda _,__,y: rcode.append("+ geom_line   (aes(y=%s), linetype='dotted')" % rname[y]))
    if PRINTTHEME: matchrule(["Y", "LINEDASH"],  lambda _,__,y: rcode.append("+ geom_point(aes(y=%s))" % rname[y]))
    matchrule(["Y", "JITTER"],lambda _,__,y: rcode.append("+ geom_jitter (aes(y=%s))" % rname[y]))
    matchrule(["Y", "POINT"], lambda _,__,y: rcode.append("+ geom_point  (aes(y=%s))" % rname[y]))
    matchrule(["Y", "POINTDODGE"], lambda _,__,y: rcode.append("+ geom_point  (aes(y=%s), position=position_dodge(width=0.3))" % rname[y]))
    matchrule(["Y", "TEXT"],  lambda _,__,y: rcode.append("+ geom_text   (aes(y=%s))" % rname[y]))
    
    matchrule(["FACET"],  lambda _,__,col: rcode.append("+ facet_wrap(~%s)"  % rname[col]))
    matchrule(["XFACET"], setcol("xf"))
    matchrule(["YFACET"], setcol("yf"))
    if "xf" in aes or "yf" in aes: rcode.append("+ facet_grid(%s~%s)" % 
        (aes["yf"] if "yf" in aes else ".", aes["xf"] if "xf" in aes else "."))
    
    matchrule(["Y", "LOG"], lambda _,__,___: rcode.append("+ scale_y_log10()"))
    matchrule(["X", "LOG"], lambda _,__,___: rcode.append("+ scale_x_log10()"))
    matchrule(["Y", "LOG2"], lambda _,__,___: rcode.append("+ scale_y_continuous(trans='log2')"))
    matchrule(["X", "LOG2"], lambda _,__,___: rcode.append("+ scale_x_continuous(trans='log2')"))
    matchrule(["Y", "FINE"], lambda _,__,___: rcode.append("+ scale_y_continuous(minor_breaks = seq(10, 1000, 10), breaks = seq(100, 1000, 100))"))
    matchrule(["X", "FINE"], lambda _,__,___: rcode.append("+ scale_x_continuous(minor_breaks = seq(10, 1000, 10), breaks = seq(100, 1000, 100))"))
    matchrule(["X", "LOGY"], lambda _,__,___: rcode.append("+ scale_y_log10()"))
    matchrule(["X", "ZERO"], lambda kw,__,___: rcode.append("+ expand_limits(x=%i)" % (1 if "LOG" in kw else 0)))
    matchrule(["Y", "ZERO"], lambda kw,__,___: rcode.append("+ expand_limits(y=%i)" % (1 if "LOG" in kw else 0)))
    matchrule(["X", "FLIP"], lambda _,__,___: rcode.append("+ coord_flip()"))
    matchrule(["X", "REVERSE"], lambda _,__,___: rcode.append("+ scale_x_reverse()"))
    matchrule(["Y", "REVERSE"], lambda _,__,___: rcode.append("+ scale_y_reverse()"))
    
    if PRINTTHEME:
        rcode.append("+ scale_colour_grey(start = 0, end = .7)")
        if not histz:
            rcode.append("+ scale_fill_grey(start = 0, end = .8)")

        rcode.append("""+ theme(panel.background = element_rect(fill='white', colour='black'),
                                plot.background = element_rect(colour = NA),
                                panel.grid.major = element_line(colour="black", size=0.1),
                                panel.grid.minor = element_line(colour="black", linetype='dotted', size=0.2))""")
        
    matchrule(["X", "VERT"], lambda _,__,___: rcode.append("+ theme(axis.text.x = element_text(angle = 90, hjust = 1, vjust = 0.5))"))
    
    rcode.append("+ scale_shape_manual(values=1:10)")
    rcode.append("+ theme(legend.position = 'bottom')")
    matchrule(["ONSIDE"], lambda _,__,___: rcode.append("+ theme(legend.position = 'right')"))
    
    if "''" in labs.values(): rcode.append("+ guides(%s)" % ", ".join('%s=FALSE' % k for k, v in labs.items() if v == "''"))
    rcode.append(")")
    rcode.append("ggsave(labels[1, 'outfilename'], plot, width=%f, height=%f)" % (w, h)) 
            
    with NamedTemporaryFile(delete=not manual) as t:
        conn.execute("ATTACH DATABASE ? AS forR;", (t.name,))
        conn.execute("CREATE TABLE forR.data(%s);" % 
                     ", ".join(rname[c] for c in cols))
        conn.execute("INSERT INTO forR.data %s" % sql)
        # avoid escape hell
        conn.execute("CREATE TABLE forR.labels(outfilename, %s);" % 
                     ", ".join(rname[c] for c in cols))
        conn.execute("INSERT INTO forR.labels VALUES(?,%s)" % ",".join(["?"]*len(cols)),
                     [outfile]+[lbl for _, lbl, _ in paras])
        conn.commit()
        r = "\n".join(r.replace("%s", t.name) for r in rcode).encode()
        #print(r.decode())
        if not manual:
            p = subprocess.Popen(["Rscript", "-"], stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)
            p.communicate(r)
