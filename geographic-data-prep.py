
from gerryframe import Setup
import geopandas as gpd

blocks = gpd.read_file("./data/steps/step-4/")

setup = Setup(blocks)
setup.points().to_graph("./data/houston-blocks.json")

