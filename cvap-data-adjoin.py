
import geopandas as gpd
import pandas as pd
import tqdm
import json
import os

from geometry import retrieve, reformat, prorate, dissolve


"""
Prepares data for gerrychain runs. Rather than areally prorating population and
demographic data, we can simply obtain CVAP and other data from the 2018 ACS at
the Census block group level, disaggregate data down to blocks (based on 2010
Census VAP), then build precincts from those blocks. This process takes four
steps:

    1.  adjoin 2010 VAP data to blocks and block groups, and 2018 ACS CVAP data
        to block groups;
    2.  disaggregate 2018 ACS block group data down to blocks;
    3.  find blocks only within Houston's borders;
    4.  find the precinct to which each block belongs;
    5.  create "fractured precincts," which will be used in redistricting.
    
A shapefile (or other file) will be written to disk at the completion of each
step to ensure that, in the event of an error, the script re-starts on the step
after the last one completed.
"""

##########
# STEP 1 #
##########

# Do we want to restart the whole process?
restart = False

if not (os.path.exists("./data/steps/step-1/step-1-bgs.shp") or os.path.exists("./data/steps/step-1/step-1-blocks.shp")) or restart:
    # Load block group and block data.
    bgs = gpd.read_file("./data/geometries/tl_2016_48_bg/")
    blocks = gpd.read_file("./data/geometries/tl_2017_48_tabblock10/")

    # We only care about the blocks or block groups with a county identifier
    # matching Harris, Montgomery, or Fort Bend.
    blocks["COUNTYFP10"] = blocks["COUNTYFP10"].astype(int)
    bgs["COUNTYFP"] = bgs["COUNTYFP"].astype(int)

    blocks = blocks[
        (blocks["COUNTYFP10"] == 157) |
        (blocks["COUNTYFP10"] == 201) |
        (blocks["COUNTYFP10"] == 339)
    ]

    bgs = bgs[
        (bgs["COUNTYFP"] == 157) |
        (bgs["COUNTYFP"] == 201) |
        (bgs["COUNTYFP"] == 339)
    ]

    # Create initial dataframes; we will select data by county first.
    bgs_acs = pd.DataFrame()
    bgs_census = pd.DataFrame()
    blocks_census = pd.DataFrame()

    # For only the counties we want, get the data for all the available smallest
    # geometries.
    for county in ["157", "201", "339"]:
        # ACS 2018 data at the block group level.
        bgs_acs = bgs_acs.append(retrieve(
            48, 2018,
            geometry=[("county", county), ("tract", "*"), ("block group", "*")]
        ))

        # 2010 Census data at the block group level.
        bgs_census = bgs_census.append(retrieve(
            48,
            2010,
            dataset="sf1",
            geometry=[("county", county), ("tract", "*"), ("block group", "*")],
            cols=["GEO_ID", "P010001"]
        ))

        # 2010 Census data at the block level.
        blocks_census = blocks_census.append(retrieve(
            48,
            2010,
            dataset="sf1",
            geometry=[("county", county), ("tract", "*"), ("block", "*")],
            cols=["GEO_ID", "P010001"]
        ))

    # Reformat the dataframes so they have proper column identifiers and indices.
    # Then, adjoin that data to the block groups we found earlier.
    bgs_acs = reformat(bgs_acs)
    bgs_census = reformat(bgs_census, geo=("GEO_ID", "GEOID"), colmap={"P010001": "2010VAP"})
    bgs["GEOID"] = bgs["GEOID"].astype(int)
    bgs = bgs.merge(bgs_census, on="GEOID")
    bgs = bgs.merge(bgs_acs, on="GEOID")

    # Adjoin 2010 Census data and 2018 ACS data to blocks.
    blocks_census = reformat(blocks_census, geo=("GEO_ID", "GEOID"), colmap={"P010001": "2010VAP"})
    blocks["GEOID"] = blocks["GEOID10"].astype(int)
    blocks = blocks.merge(blocks_census, on="GEOID")

    # Load prepared 2018 CVAP data and join to block groups.
    bg_cvaps = pd.read_csv("./data/demographics/acs-cvap-transposed/tx-bg-cvaps-t-2018.csv")
    bg_cvaps["GEOID"] = bg_cvaps["geoid"].astype(int)
    del bg_cvaps["geoid"]
    bgs = bgs.merge(bg_cvaps, on="GEOID")

    # Write to file.
    bgs.to_file("./data/steps/step-1/step-1-bgs.shp")
    blocks.to_file("./data/steps/step-1/step-1-blocks.shp")

    print("Step 1 complete.")
else:
    print("Step 1 already completed; moving to Step 2.")


##########
# STEP 2 #
##########

if not os.path.exists("./data/steps/step-2/blocks.shp") or restart:
    # Load data.
    blocks = gpd.read_file("./data/steps/step-1/step-1-blocks.shp")
    bgs = gpd.read_file("./data/steps/step-1/step-1-bgs.shp")

    # Get column names from codebook file.
    with open("./data/demographics/cvap-codebook.json") as f: codebook = json.load(f)
    columns = list(codebook["2018"].keys()) + ["TOTPOP", "2010VAP"]

    # Prorate desired columns from block groups down to blocks.
    blocks = prorate(blocks, bgs, "2010VAP", "2010VAP", columns=columns)
    blocks.to_file("./data/steps/step-2/blocks.shp")
    print(blocks.head())
    print("Step 2 complete.")
else:
    print("Step 2 already completed; moving to Step 3.")


##########
# STEP 3 #
##########

if not os.path.exists("./data/steps/step-3/step-3.shp") or restart:
    # Load data.
    districts = gpd.read_file("./data/geometries/city-council-districts/")
    districts["geometry"] = districts["geometry"].buffer(0)
    blocks = gpd.read_file("./data/steps/step-2/blocks.shp")
    blocks["COUNTYFP10"] = blocks["COUNTYFP10"].astype(int)

    # Create a list to store blocks outside the city limits (i.e. blocks to
    # throw away) and a column on the blocks for district identification.
    outside = []
    blocks["district"] = ""

    # Assign blocks to districts based on which district most of their area lies
    # in.
    for index, brow in tqdm.tqdm(blocks.iterrows(), total=len(blocks)):
        block = brow["geometry"]
        largest = (0,"")
        for _, drow in districts.iterrows():
            district = drow["geometry"]

            # Find the area of the intersection between the block and the
            # district.
            intersection = block.intersection(district).area
            if intersection > largest[0]: largest = (intersection, drow["DISTRICT"])

        # If the largest area is zero, then the block isn't in any of the city
        # council districts, so we throw it out.
        if largest[0] == 0: outside.append(index); continue
        blocks.at[index, "district"] = largest[1]

    # Remove all the blocks not in Houston and write to file.
    hblocks = blocks.drop(outside)
    hblocks.to_file("./data/steps/step-3/step-3.shp")

    print("Step 3 complete.")
else:
    print("Step 3 already completed; moving to Step 4.")

##########
# STEP 4 #
##########

if not os.path.exists("./data/steps/step-4/step-4.shp") or restart:
    # Assign blocks to precincts.
    precincts = gpd.read_file("./data/geometries/all-precincts/")
    blocks = gpd.read_file("./data/steps/step-3/")
    blocks = blocks.to_crs(precincts.crs)

    blocks["precinct"] = 0

    for _, brow in tqdm.tqdm(blocks.iterrows(), total=len(blocks)):
        largest = (0, 0)
        for index, prow in precincts.iterrows():
            block, precinct = brow["geometry"], prow["geometry"]
            area = block.intersection(precinct).area

            if area > largest[0]: largest = (area, index)

        blocks.at[_, "precinct"] = largest[1]

    # Write to file.
    blocks.to_file("./data/steps/step-4/step-4.shp")
    print("Step 4 complete.")
else:
    print("Step 4 already completed; moving to Step 5.")

if not os.path.exists("./data/steps/step-5/fractured-precincts.shp") or restart:
    # Now, we just dissolve blocks based on their precinct membership.
    blocks = gpd.read_file("./data/steps/step-4/")

    # Get column names from codebook file.
    with open("./data/demographics/cvap-codebook.json") as f: codebook = json.load(f)
    columns = list(codebook["2018"].keys()) + ["TOTPOP", "2010VAP"]

    # Dissolve.
    fractured = dissolve(blocks, join="precinct", columns=columns)
    fractured.to_file("./data/steps/step-5/fractured-precincts.shp")
else:
    print("Step 5 already completed; set `restart = True` to re-do process.")

print("Complete.")
