import matplotlib.pyplot as plt
import csv
from os.path import exists

def read_data(filename):
	years = []
	powers = []
	with open(filename, newline = '') as csvfile:
		reader =csv.reader(csvfile, delimiter=',', quotechar = '"')
		for row in reader:
			years.append(round(float(row[0])))			
			powers.append(round(float(row[1])))			
	return (years, powers)


def create_plot():
	fig, ax = plt.subplots(1,1, figsize = (4,2))
	plt.subplots_adjust(left=0.15, right = 0.95, top = 0.95, bottom = 0.2)

	(years_io, powers_io) = read_data("power_io.csv")
	(years_total, powers_total) = read_data("power_total.csv")

	plt.scatter(years_total, powers_total, color = "#559955", marker = ".", label = "total power per package")
	plt.scatter(years_io, powers_io, color = "#995500", marker = "*", label = "power for off-chip I/O")

	plt.plot([1994,2030],[1,3566], "--", marker = "None", color = "#995500")
	plt.plot([1990,2020],[7.2,422], "--", marker = "None", color = "#559955")

	ax.set_yscale("log")
	ax.set_ylim(1,1000)
	ax.set_xlim(1990,2030)
	ax.set_ylabel("Power [W]")
	ax.set_xlabel("Year")
	ax.grid()
	ax.legend(loc = "lower right", bbox_to_anchor = (1,0), labelspacing = 0.2, handlelength = 1)

	plt.savefig("plots/plot_power.pdf")

		
create_plot()
