
import geopandas as gpd
import pandas as pd

"""
Retrieves stats about the current districting plan.
"""
vtds = gpd.read_file("./data/geometries/districts-adjoined/")
districts = pd.DataFrame()

columns = [
	'1-2018', '3-2018', '4-2018', '5-2018', '6-2018', '7-2018', '8-2018',
	'9-2018', '10-2018', '11-2018', '12-2018', '13-2018', 'TOTPOP', '2010VAP',
	'PRES12R', 'PRES12D', 'SEN12R', 'SEN12D', 'TOTVR12', 'TOTTO12', 'SEN14R',
	'SEN14D', 'GOV14R', 'GOV14D', 'TOTVR14', 'TOTTO14', 'PRES16D', 'PRES16R',
	'TOTVR16', 'TOTTO16'
]

# First, we select rows based on their district. Then, we aggregate all the
# rows in the district.
for district in set(vtds["DISTRICT"]):
	row = vtds[vtds["DISTRICT"] == district][columns].aggregate("sum")
	row.name = district
	districts = districts.append(row)

districts = districts.applymap(lambda r: round(r, 2))

# Write the statistics to file.
districts.sort_values("13-2018", ascending=False).to_csv("./data/demographics/enacted.csv")
