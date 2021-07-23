
import matplotlib.pyplot as plt
from charting import plots, demographics, partisan
import pandas as pd
import numpy as np
import os
from .fonts import fonts


def seats(config, guidance, election, districts, members):
	gf = "guidance" if guidance else "no-guidance"
	results = pd.read_csv(f"./data/results/{config}/{gf}/{election}.csv")

	# Calculate the number of seats based on the number of districts and the
	# number of members per district. Uses the droop quota.
	ts = districts*members
	lower = 1/(members+1)

	# Set fonts.
	fonts()

	# Create a dictionary of district IDs and empty lists.
	seatsdict = {
		district: []
		for district in list(results)
	}

	# Iterate over the districts and find out how many seats were won per
	# district in each district. Then, sum these together to determine the
	# overall number of seats won.
	for district in list(results):
		seatsdict[district] = np.array(results[district].apply(lambda g: int(g/lower)))

	totalseats = sum(seatsdict[district] for district in seatsdict)
	partisan.seats(
		totalseats, ts, chamber=gf, defaults=False,
		state=f"Houston City Council, Configuration {config},"
	)

	plt.savefig(f"./figures/{config}/{gf}/seats.png", bbox_inches="tight", dpi=400)
