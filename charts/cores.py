
import ast
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from charting import defaults, plots as plts
import pandas as pd
import numpy as np
from .fonts import fonts


def cores(config, guidance, shape):
	# First, plot the map.
	fig, ax = plt.subplots()
	fonts()
	plts.map(ax, shape, linewidth=0.1)

	# Now, prepare the data. This one might not be great, but we'll try.
	gf = "guidance" if guidance else "no-guidance"
	hcvaps = pd.read_csv(f"./data/results/{config}/{gf}/hcvap%.csv")
	steps = len(hcvaps)
	centers = pd.read_csv(
		f"./data/results/{config}/{gf}/centers.csv",
		converters={d: ast.literal_eval for d in range(len(hcvaps))}
	)

	# Rename columns, concat data, make bins.
	hcvaps = hcvaps.rename({str(d): f"hcvap-{d}" for d in list(hcvaps)}, axis=1)
	data = pd.concat([centers, hcvaps], axis=1)
	bins = [round((i*0.2), 1) for i in range(1, 6)]

	# Create a list of cores.
	cores = {
		f"{round(bin-0.2, 1)} – {bin}": list(np.concatenate([
			data[(data[f"hcvap-{d}"] > bin-1/5) & (data[f"hcvap-{d}"] <= bin)][str(d)]
			for d in range(len(list(hcvaps)))
		]))[::10]
		for bin in bins
	}

	# Get a color palette and plot points.
	palette = defaults.style.palette(len(cores))
	for i, bin in enumerate(cores):
		x, y = [pt[0] for pt in cores[bin]], [pt[1] for pt in cores[bin]]
		plts.splot(
			ax, x, y,
			s=1,
			markerfacecolor=palette[i],
			markeredgecolor="none",
			alpha=0.2
		)

	# Add things to legends.
	legendprops = {
		"marker": "o",
		"color": "w",
		"markeredgecolor": "none"
	}
	plots = [
		Line2D([0],[0], markerfacecolor=palette[i], label=bin, **legendprops)
		for i, bin in enumerate(cores)
	]

	# Remove all axes.
	plt.axis("off")

	# Titles, legends, and saving.
	plt.suptitle(f"Population-Weighted Centers – Ensemble Comparison", fontsize=16)
	plt.title(
		f"Houston City Council, Configuration {config}, {gf.upper()} {format(steps, ',d')}-Map Ensemble",
		fontdict={"usetex": True}
	)
	ax.legend(handles=plots, loc="lower right", prop={"size": 6})
	plt.savefig(f"./figures/{config}/{gf}/cores.png", bbox_inches="tight", dpi=400)
