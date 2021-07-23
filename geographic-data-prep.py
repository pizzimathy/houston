
from gerryframe import Setup
import geopandas as gpd

blocks = gpd.read_file("./data/geometries/districts-adjoined/")

setup = Setup(blocks)
setup.points().to_graph("./data/houston-vtds.json")

