
import matplotlib.pyplot as plt
from charting import scores
import pandas as pd
from .fonts import fonts
from .defaults import *


def distances(config, guidance):
	gf = "guidance" if guidance else "no-guidance"

	# Read in data.
	edges = list(pd.read_csv(f"./data/results/{config}/{gf}/cutedges.csv")["cutedges"])
	steps = len(edges)

	# Set fonts and plot.
	fonts()

	# Plot boxes.
	scores.cutedges(
		edges, 2397, defaults=False, title=False, *stdopts
	)
	plt.savefig(f"./figures/{config}/{gf}/distances.png", **stdsave)
