
import matplotlib.pyplot as plt
import seaborn as sns
from charting import plots, defaults
import numpy as np
from scores import temperature
from math import e
from charts import fonts

def temp(config, guidance):
	gf = "guidance" if guidance else "no-guidance"
	# Plot the temperature function.
	N = 50000
	phi = 2/3
	L = 23000
	fig, ax = plt.subplots()

	# Set fonts.
	defaults.style.format(latex=True)

	# Get coordinates.
	x = np.arange(0,N,0.1)
	y = [-temperature(t, L, N, 1/3000, phi=phi) for t in x]
	plots.lines(ax, x, y, marker=None, lw=2)

	# Set tick label fonts.
	ax.set_xticklabels([int(x) for x in ax.get_xticks()], {"usetex": True})
	ax.set_yticklabels([round(y, 2) for y in ax.get_yticks()], {"usetex": True})

	# ticks.
	plt.yticks([0, -L/2, -L], [r"$0$", r"$-\frac{L}{2}$", "$-L$"], fontsize=30)
	plt.xticks([0, N*phi, N], [r"$0$", r"$\phi$" + "$N$", r"$N$"], fontsize=30)
	plt.axvline(N*phi, ls=":", color="k", alpha=1/2)
	plt.axhline(-L/2, ls=":", color="k",alpha=1/2)
	plt.text(N*phi + 1/100*N, -L/2, f"$k$", fontsize=30)
	plt.savefig(f"./figures/{config}/{gf}/temperature-function.png", dpi=600, bbox_inches="tight")
	sns.despine()
