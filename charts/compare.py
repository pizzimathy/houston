
import ast
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from charting import defaults, comparison
import pandas as pd
import numpy as np
from .fonts import fonts


def compare(config, guidance):
	gf = "guidance" if guidance else "no-guidance"
	hcvaps = pd.read_csv(f"./data/results/{config}/{gf}/hcvap%.csv")
	cutedges = pd.read_csv(f"./data/results/{config}/{gf}/cutedges.csv")

	# Re-set cutedges so it's a percentage.
	cutedges["cutedges"] = cutedges["cutedges"].apply(lambda k: k/2397)

	# Make lists.
	hcvapvar = list(hcvaps[list(hcvaps)].var(axis=1))
	edges = list(cutedges["cutedges"])

	# Do the plotting thing!
	fonts()
	comparison.joint(
		hcvapvar, edges, kind="hist", defaults=False, vline=np.median(hcvapvar),
		hline=np.median(edges)
	)
	plt.show()
