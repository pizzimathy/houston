
import matplotlib.pyplot as plt
from charting import plots, defaults
import numpy as np
import pandas as pd
from .fonts import fonts
from . import defaults as opts


def accepts(config, guidance):
	gf = "guidance" if guidance else "no-guidance"

	# Retrieve data.
	accepts = list(pd.read_csv(f"./data/results/{config}/{gf}/accept.csv")["accept"])
	steps = len(accepts)

	# Plot.
	fig, ax = plt.subplots()
	fonts()

	fontdict = {
		"usetex": True,
		"size": 10
	}

	# Use LaTeX.
	plt.suptitle(f"Proposal Acceptance Probability", fontsize=16)
	plt.title(
		f"Houston City Council, Configuration {config}, {gf.upper()} {format(steps, ',d')}-Map Ensemble",
		fontdict={"usetex": True}
	)
	plt.ylabel("Probability", fontdict=fontdict)
	plt.xlabel("Step", fontdict=fontdict)
	plt.yticks(np.arange(0,1.1,0.25), ["0", "25%", "50%", "75%", "100%"])
	plots.splot(ax, range(len(accepts)), accepts, s=2, alpha=1/10)

	# Set fonts.
	ax.set_xticklabels([int(x) for x in ax.get_xticks()], {"usetex": True})
	ax.set_yticklabels([round(y, 2) for y in ax.get_yticks()], {"usetex": True})

	plt.savefig(f"./figures/{config}/{gf}/acceptance.png", opts.stdsave)
