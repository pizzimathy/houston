
import geopandas as gpd
import tqdm


# Import data.
cc = gpd.read_file("./data/geometries/ccds/")
precincts = gpd.read_file("./data/steps/step-5/")

# Match CRSes.
cc = cc.to_crs(precincts.crs)

# Set geometries properly.
cc["geometry"] = cc["geometry"].buffer(0)
precincts["geometry"] = precincts["geometry"].buffer(0)

def isint(k):
    try: int(k)
    except: return False
    return True

# Change columns.
relabel = lambda g: int(g) if isint(g) else 0

for i, row in tqdm.tqdm(precincts.iterrows(), total=len(precincts)):
    precinct = row["geometry"]

    for plan, name in zip([cc], ["DISTRICT"]):
        maxintersection, districtlabel = 0, ""

        for _, district in plan.iterrows():
            _label = district[name]
            districtpoly = district["geometry"]
            intersection = precinct.intersection(districtpoly).area

            if intersection > maxintersection:
                maxintersection = intersection
                districtlabel = _label

        precincts.at[i, name] = districtlabel


assignment = precincts[["VTD", "DISTRICT"]]
assignment.to_csv("./data/district-assignments.csv", index=False)
precincts.to_file("./data/geometries/districts-adjoined/districts-adjoined.shp")
