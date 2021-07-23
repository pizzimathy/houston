
from gerryframe import Plan, Chain, Accept, updaters
from scores import ideal, npd
import pandas as pd
import os

from configuration import configurations, ideals, run

for id in run["configurations"]:
	# Set the number of districts and the number of members.
	districts, members = configurations[id]

	# Create a Plan object for the 11-member Houston city council.
	cc = Plan(districts=districts, chamber="City Council")
	cc.load_graph("./data/houston-vtds.json")

	# Now, we create our chain object.
	chain = Chain(cc)
	chain.pop_column = "TOTPOP"

	# Next, we set up an ideal distribution, an acceptance function, and some
	# updaters. No acceptance function to guide the chain, so we get a good
	# control.
	pi = ideals[id]
	chain.steps = 50000
	acceptance = ideal(pi, "hcvap%", chain.steps, L=23000, k=1/3000, phi=2/3)
	# chain.accept = Accept.metropolis_hastings(acceptance)

	# Set updaters.
	chain.updaters = {
		"cvap": updaters.Tally("1-2018", "cvap"),
		"bcvap": updaters.Tally("5-2018", "bcvap"),
		"bcvap%": updaters.Percentage("bcvap", "cvap"),
		"hcvap": updaters.Tally("13-2018", "hcvap"),
		"hcvap%": updaters.Percentage("hcvap", "cvap"),
		"accept": lambda p: min(1, acceptance(p)/acceptance(p.parent)) if p.parent else 1,
		"distance": npd(pi, "hcvap%"),
		"2012sen": updaters.Election("2012 Senate", {"D": "SEN12D", "R": "SEN12R"}, alias="2012sen"),
		"2012pres": updaters.Election("2012 President", {"D": "PRES12D", "R": "PRES12R"}, alias="2012sen"),
		"2014sen": updaters.Election("2014 Senate", {"D": "SEN14D", "R": "SEN14R"}, alias="2014sen"),
		"2014gov": updaters.Election("2014 Governor", {"D": "GOV14D", "R": "GOV14R"}, alias="2014gov"),
		"2016pres": updaters.Election("2016 President", {"D": "PRES16D", "R": "PRES16R"}, alias="2016pres"),
		"centers": updaters.weightedcenters(weight=chain.pop_column)
	}

	# Set up some containers for election results..
	elections = ["2012sen", "2012pres", "2014sen", "2014gov", "2016pres"]
	electionresults = {election: {d: [] for d in range(districts)} for election in elections}

	for partition in chain.progress():
		# Collect statistical results.
		chain.collect(
			partition,
			updaters=[
				"hcvap%", "bcvap%", "distance", "accept",
			]
		)

		for election in elections:
			for i, result in enumerate(partition[election].percents("D")):
				electionresults[election][i].append(result)

	# Create filepaths for results.
	p = os.path
	ex = p.exists
	root = "./data/results/"
	if not ex(root): os.mkdir(root)
	if not ex(p.join(root, id)): os.mkdir(p.join(root, id))
	if not ex(p.join(root, id, "no-guidance")): os.mkdir(p.join(root, id, "no-guidance"))
	root = p.join(root, id, "no-guidance")

	# Write election results as separate spreadsheets.
	for election in electionresults:
		pd\
			.DataFrame.from_dict(electionresults[election]) \
			.to_csv(f"{root}/{election}.csv", index=False)

	chain.write(root)
