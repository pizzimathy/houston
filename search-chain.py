
from gerryframe import Plan, Chain, updaters

# Create a Plan object for the 11-member Houston city council.
cc = Plan(districts=11, chamber="City Council")
cc.load_graph("./data/houston-vtds.json")
