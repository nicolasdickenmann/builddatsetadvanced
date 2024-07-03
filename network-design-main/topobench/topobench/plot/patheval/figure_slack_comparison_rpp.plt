###  
###  Released under the MIT License (MIT) --- see ../LICENSE
###  Copyright (c) 2014 Ankit Singla, Sangeetha Abdu Jyothi, Chi-Yao Hong, Lucian Popa, P. Brighten Godfrey, Alexandra Kolla, Simon Kassing
###  

# Note you need gnuplot 4.4 for the pdfcairo terminal.
set terminal pdfcairo font "Gill Sans, 16" linewidth 1.8 rounded dashed

# Line style for axes
set style line 80 lt rgb "#808080" 

# Line style for grid
set style line 81 lt 0  # dashed
set style line 81 lt rgb "#808080"  # grey

set grid back linestyle 81
set border 3 back linestyle 80 # Remove border on top and right.  These
             # borders are useless and make it harder
	                  # to see plotted lines near the border.
			      # Also, put it in grey; no need for so much emphasis on a border.
			      set xtics nomirror
			      set ytics nomirror

#set log x
#set mxtics 10    # Makes logscale look good.

# Line styles: try to pick pleasing colors, rather
# than strictly primary colors or hard-to-see colors
# like gnuplot's default yellow.  Make the lines thick
# so they're easy to see in small plots in papers.
set style line 1 lt rgb "#5060D0" lw 1.5 pt 7 ps 0.5
set style line 2 lt rgb "#A00000" lw 2 pt 2 ps 0.8
set style line 3 lt rgb "#00A000" lw 1.3 pt 6 ps 0.8
set style line 4 lt rgb "#F25900" lw 1 pt 8
set style line 5 lt rgb "#996600" lw 1 pt 4
set style line 6 lt rgb "#4B0082" lw 1.5 pt 5 ps 0.8
set style line 7 lt rgb "#008b8b" lw 1.1 pt 9 ps 0.8

set output "figure_slack_comparison_rpp.pdf"
set xlabel "Fraction of servers with traffic demand"
set ylabel "Throughput per server"

set xrange [0.1:1]
set yrange [0:1]

#set key bottom left 
set key top right
#set key opaque

plot "../../results/patheval/slack_comparison_rpp.txt" using 9:((strcol(1) eq "SLACK") && $2==-1 ? (($10/$7) > 1 ? 1 : ($10/$7)) : 1/0) title "Slack Infinite"  w lp ls 2, \
     "../../results/patheval/slack_comparison_rpp.txt" using 9:((strcol(1) eq "SLACK") && $2==3 ? (($10/$7) > 1 ? 1 : ($10/$7)) : 1/0) title "Slack 3"  w lp ls 1, \
     "../../results/patheval/slack_comparison_rpp.txt" using 9:((strcol(1) eq "SLACK") && $2==2 ? (($10/$7) > 1 ? 1 : ($10/$7)) : 1/0) title "Slack 2"  w lp ls 3, \
     "../../results/patheval/slack_comparison_rpp.txt" using 9:((strcol(1) eq "NEIGH") ? (($10/$7) > 1 ? 1 : ($10/$7)) : 1/0) title "Neighbor"  w lp ls 4, \
     "../../results/patheval/slack_comparison_rpp.txt" using 9:((strcol(1) eq "SLACK") && $2==1 ? (($10/$7) > 1 ? 1 : ($10/$7)) : 1/0) title "Slack 1"  w lp ls 5, \
     "../../results/patheval/slack_comparison_rpp.txt" using 9:((strcol(1) eq "SLACK") && $2==0 ? (($10/$7) > 1 ? 1 : ($10/$7)) : 1/0) title "Slack 0"  w lp ls 7
     
	 
     
     