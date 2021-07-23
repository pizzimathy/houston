
import matplotlib.pyplot as plt
from charting import plots, defaults
import pandas as pd


def distances(config, guidance):
	gf = "guidance" if guidance else "no-guidance"

	# Read in data.
	distances = list(pd.read_csv(f"./data/results/{config}/{gf}/distance.csv")["distance"])
	steps = len(distances)

	# Plot.
	fig, ax = plt.subplots()
	defaults.style.format(latex=True, serif=True)

	# Set fonts.
	fontprops = {
		"usetex": True,
		"size": 10
	}

	# Use LaTeX.
	plt.suptitle(f"Normalized Permuted Euclidean Distance", fontsize=16)
	plt.title(
		f"Houston City Council, Configuration {config}, {gf.upper()} {format(steps, ',d')}-Map Ensemble",
		fontdict={"usetex": True}
	)
	plt.xlabel("Step", fontdict=fontprops)
	plt.ylabel("Normalized Permuted Euclidean Distance", fontdict=fontprops)
	plots.splot(ax, range(len(distances)), distances, s=2, alpha=1/10)

	# Set tick label fonts.
	ax.set_xticklabels([int(x) for x in ax.get_xticks()], {"usetex": True})
	ax.set_yticklabels([round(y, 2) for y in ax.get_yticks()], {"usetex": True})

	plt.savefig(f"./figures/{config}/{gf}/distances.png", dpi=600, bbox_inches="tight")
