
import matplotlib.pyplot as plt
from charting import demographics, defaults
import pandas as pd
from .fonts import fonts


def boxes(config, guidance, members):
	gf = "guidance" if guidance else "no-guidance"
	results = pd.read_csv(f"./data/results/{config}/{gf}/hcvap%.csv")
	_max = max(results.max())

	# Set fonts.
	fonts()

	# Plot boxes.
	ax = demographics.boxes(
		results, chamber=gf, statistic="Hispanic CVAP, Percent", titles=False,
		state=f"Houston City Council, Configuration {config},", defaults=False
	)

	# Some text stuff.
	textprops = {
		"ha": "left",
		"va": "bottom",
		"color": "k",
		"alpha": 1/2,
		"zorder": 1
	}

	# Plot visual guidelines and text helpers.
	droops = [(i+1)/(members+1) for i in range(members) if (i+1)/(members+1) < _max]
	for i, d in enumerate(droops):
		# Plot visual guidelines.
		ax.axhline(d, ls=":", color="k", alpha=1/2, zorder=0)

		# Plot text helpers.
		loc = (0.55,d)
		ax.text(
			*loc,
			f"{i+1} seat{'s' if (i+1)>1 else ''}",
			**textprops
		)

	# Save figures.
	plt.savefig(f"./figures/{config}/{gf}/boxes.png", bbox_inches="tight", dpi=400)
