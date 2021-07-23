
from charts import *
import geopandas as gpd
import os
from configuration import run, ideals, configurations


def checkpath(config, guidance):
	p = os.path
	guideroot = "guidance" if guidance else "no-guidance"
	if not p.exists(f"./figures/{config}/"): os.mkdir(f"./figures/{config}/")
	if not p.exists(f"./figures/{config}/{guideroot}/"): os.mkdir(f"./figures/{config}/{guideroot}/")


for config in run["configurations"]:
	for guidance in [True, False]:
		ts, members = configurations[config]
		# checkpath(config, guidance)
		# seats(config, guidance, "hcvap%", ts, members)
		boxes(config, guidance, members)
		# cores(config, guidance, gpd.read_file("./data/geometries/districts-adjoined/").to_crs("epsg:4326"))
		# accepts(config, guidance)
		distances(config, guidance)
		# temp(config, guidance)
		# compare(config, guidance)
