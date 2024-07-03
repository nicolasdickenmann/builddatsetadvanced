import matplotlib.pyplot as plt
import csv
from os.path import exists

def read_data(filename):
	pf_deg = []
	pf_perc = []
	sf_deg = []
	sf_perc = []
	hx_deg = []
	hx_perc = []
	pg_deg = []
	pg_perc = []
	sh_deg = []
	sh_perc = []

	with open(filename, newline = '') as csvfile:
		reader =csv.reader(csvfile, delimiter=',', quotechar = '"')
		next(reader)	#Header 1
		next(reader)	#Header 2
		for row in reader:
			if row[0] != "":
				pf_deg 	.append(float(row[0]))
				pf_perc .append(float(row[1]))
			if row[4] != "":
				sf_deg 	.append(float(row[4]))
				sf_perc .append(float(row[5]))
			if row[7] != "":
				hx_deg 	.append(float(row[7]))
				hx_perc .append(float(row[8]))
			if row[10] != "":
				pg_deg 	.append(float(row[10]))
				pg_perc .append(float(row[11]))
			if row[13] != "":
				sh_deg 	.append(float(row[13]))
				sh_perc .append(float(row[14]))
	return (pf_deg,pf_perc,sf_deg,sf_perc,hx_deg,hx_perc,pg_deg,pg_perc,sh_deg,sh_perc)


def create_plot():
	fig, ax = plt.subplots(1,1, figsize = (4.5,2.75))
	plt.subplots_adjust(left=0.15, right = 0.98, top = 0.75, bottom = 0.17)

	(pf_deg,pf_perc,sf_deg,sf_perc,hx_deg,hx_perc,pg_deg,pg_perc,sh_deg,sh_perc) = read_data("moore_bound_comparison.csv")

	ax.grid()

	plt.scatter(pf_deg, pf_perc, color = "#000099", marker = "o", label = "PolarFly", s = 2)
	plt.scatter(sf_deg, sf_perc, color = "#666666", marker = "*", label = "SlimFly", s = 2)
	plt.scatter(hx_deg, hx_perc, color = "#995500", marker = "d", label = "HyperX", s = 2)
	plt.scatter(pg_deg, pg_perc, color = "#999900", marker = "s", label = "Petersen Graph", s = 2)
	plt.scatter(sh_deg, sh_perc, color = "#009900", marker = "D", label = "Hoffman-Singleton Graph", s = 2)
	plt.scatter(pg_deg, pg_perc, color = "#999900", marker = "s", s = 12)
	plt.scatter(sh_deg, sh_perc, color = "#009900", marker = "D", s = 12)


	ax.set_ylim(0,105)
	ax.set_xlim(0,125)
	ax.set_title("Diameter 2 Moore Bound Comparison", y = 1.25)
	ax.set_ylabel("Percentage of Moore Bound")
	ax.set_xlabel("Degree")
	ax.legend(loc = "upper center", bbox_to_anchor = (0.5,1.3), labelspacing = 0.1, handlelength = 1, markerscale = 3, ncol = 3, fontsize = 9, columnspacing = 0.3, handletextpad = 0.25)
	ax.set_axisbelow(True)

	plt.savefig("plot_moore_bound.pdf")

		
create_plot()
