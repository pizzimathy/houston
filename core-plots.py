
import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd
from ast import literal_eval as tup
from charting import defaults, scores, partisan

for root in ["guidance", "no-guidance"]:
	# Start plotting.
	cores = pd.read_csv(f"./data/{root}/centers.csv")
	votes = pd.read_csv(f"./data/{root}/2016pres.csv")

	# First, rename the columns.
	corecols = {str(d): f"cores-{d}" for d in range(len(list(cores)))}
	votecols = {str(d): f"votes-{d}" for d in range(len(list(votes)))}
	cores = cores.rename(columns=corecols)
	votes = votes.rename(columns=votecols)

	# Parse coordinates.
	cores = cores.applymap(tup)

	# Pivot the dataframe to match the requirements.
	dfdict = {"x": [], "y": [], "party": []}

	# Define a function for determining party designation.
	def party(g):
		if g > 0.55: return "D"
		elif g <= 0.55 and g >= 0.45: return "C"
		else: return "R"

	for district in range(len(list(cores))): dfdict["x"] += [t[0] for t in list(cores[f"cores-{district}"])]
	for district in range(len(list(cores))): dfdict["y"] += [t[1] for t in list(cores[f"cores-{district}"])]
	for district in range(len(list(votes))): dfdict["party"] += list(votes[f"votes-{district}"].apply(party))

	cores = pd.DataFrame.from_dict(dfdict)
	cores = cores.iloc[::2, :]

	# Plot.
	partisan.cores(
		gpd.read_file("./data/geometries/districts-adjoined/").to_crs("epsg:4326"),
		cores,
		chamber="City Council"
	)
	plt.savefig(f"./figures/{root}-cores.png", dpi=600, bbox_inches="tight")
	plt.clf()
