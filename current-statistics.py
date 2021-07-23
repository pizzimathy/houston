
import geopandas as gpd
import pandas as pd

from geometry import dissolve


# Import data.
vtds = gpd.read_file("./data/geometries/districts-adjoined/")

# Get district names and create a new dataframe.
columns = [
	"TOTPOP", "1-2018", "5-2018", "13-2018", 'PRES12R', 'PRES12D', 'SEN12R',
	'SEN12D', 'TOTVR12', 'TOTTO12', 'SEN14R', 'SEN14D', 'GOV14R', 'GOV14D',
	'TOTVR14', 'TOTTO14', 'PRES16D', 'PRES16R', 'TOTVR16', 'TOTTO16'
]

# Dissolve on districts; ask if we want to save the file.
save = False
root = "./data/geometries/districts-statistics-adjoined/"
districts = dissolve(vtds, join="DISTRICT", columns=columns)
if save: districts.to_file(root + "districts-statistics-adjoined.shp")

# Write stats to file.
root = "./data/demographics/enacted/"
districtdata = pd.DataFrame(districts[columns])
districtdata["BCVAP%"] = districtdata["5-2018"]/districtdata["1-2018"]
districtdata["HCVAP%"] = districtdata["13-2018"]/districtdata["1-2018"]
districtdata.to_csv("./data/demographics/enacted/enacted.csv")
