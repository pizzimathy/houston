
import matplotlib.pyplot as plt
from charting import plots, defaults
from charting import partisan, demographics
import pandas as pd
import numpy as np


# Plot results.
for root in ["guidance", "no-guidance"]:
	# Get dataframes.
	df_accepts = pd.read_csv(f"./data/{root}/accept.csv")
	df_distances = pd.read_csv(f"./data/{root}/distance.csv")

	# Get lists of values.
	accepts = list(df_accepts["accept"])
	distances = list(df_distances["distance"])

	# Plot.
	fig, ax = plt.subplots()
	defaults.style.format()

	# Use LaTeX.
	plt.suptitle(f"Proposal Acceptance Probability – {root.capitalize()}", fontsize=15)
	plt.ylabel(r"Probability", fontsize=10)
	plt.xlabel(r"Step", fontsize=10)
	plt.yticks(np.arange(0,1.1,0.25), ["0", "25%", "50%", "75%", "100%"])
	plots.splot(ax, range(len(accepts)), accepts, s=2, alpha=1/10)
	plt.savefig(f"./figures/acceptance-{root}.png", dpi=600, bbox_inches="tight")
	plt.close()

	# Plot.
	fig, ax = plt.subplots()
	defaults.style.format()

	# Use LaTeX.
	plt.suptitle(f"Normalized Permuted Euclidean Distance", fontsize=15)
	plt.xlabel("Step", fontsize=10)
	plt.ylabel(r"Normalized Permuted Euclidean Distance", fontsize=10)
	plots.splot(ax, range(len(distances)), distances, s=2, alpha=1/10)
	plt.savefig(f"./figures/distances-{root}.png", dpi=600, bbox_inches="tight")
	plt.clf()

	# Plots for seats.
	fig, ax = plt.subplots()
	defaults.style.format()
	demographics.boxes(
		pd.read_csv(f"./data/{root}/hcvap%.csv"),
		chamber="City Council",
		statistic="Hispanic Citizen Voting Age Population",
		state="Houston"
	)
	plt.savefig(f"./figures/hcvap%-{root}.png", dpi=600, bbox_inches="tight")
