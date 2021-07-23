
import pandas as pd
import json
from tqdm import tqdm
from enum import Enum


"""
This script prepares the data in the 2018 ACS CVAP data file, where each row
corresponds to a racial or ethnic category, and groups of rows correspond to
individual block groups. This data will be prorated down to blocks (from the
block group level).
"""


class linenumber(Enum):
    """
    Maps names of columns to their positions in each transposed row.
    """
    _TOTAL = 0
    NHCVAP = 1
    AICVAP = 2
    ASIANCVAP = 3
    BCVAP = 4
    NHPICVAP = 5
    WCVAP = 6
    AIWCVAP = 7
    ASIANWCVAP = 8
    BWCVAP = 9
    AIBCVAP = 10
    OCVAP = 11
    HISPCVAP = 12


# Set years and create a codebook for columns.
years = [2018]
descriptions = [
    "Total CVAP",
    "American Indian or Alaska Native Alone",
    "Asian Alone",
    "Black or African American Alone",
    "Native Hawaiian or Other Pacific Islander Alone",
    "White Alone",
    "American Indian or Alaska Native and White",
    "Asian and White",
    "Black or African American and White",
    "American Indian or Alaska Native and Black or African American",
    "Remainder of Two or More Race Responses",
    "Hispanic or Latino"
]
book = {}

for year in years:
    all_cvaps = pd.read_csv(f"./data/demographics/acs-cvap-{year}/BlockGr.csv", encoding="ISO-8859-1")

    # Now, we have to throw out all the rows which aren't in Texas. The naming
    # scheme for each of the block group IDs is 15000USsscccttttttb, where
    #
    #                           ss      > state FIPS
    #                           cc      > county FIPS
    #                           tttttt  > tract FIPS
    #                           b       > block FIPS
    #
    # Based on this schema, we need to throw out every row that does not match
    #
    #                           15000US48cccttttttb.
    #
    # Throw out the rows.
    all_cvaps = all_cvaps.rename(columns={column: column.lower() for column in list(all_cvaps)})
    all_cvaps = all_cvaps.drop(["geoname", "lntitle"], axis=1)
    cvaps = all_cvaps[all_cvaps["geoid"].str.contains("15000US48")]

    # Reformat the dataframe (essentially transposition with some mapping), and
    # update the codebook.
    lines = [f"1-{year}"] + [f"{line}-{year}" for line in range(3,14)]
    book.update({year: {column: description for column, description in zip(lines, descriptions)}})
    cols = ["geoid"] + lines
    cvapst = pd.DataFrame(columns=cols)
    i = 0

    rows = []


    def mapcvap(row):
        """
        Properly maps CVAP columns to the specified categories.
        :param row: Dataframe row.
        :return: Modified dataframe row.
        """
        # Find the sum of the actual entries in the row.
        _total = sum(row[linenumber.AICVAP.value:])
        _TOTAL = row[linenumber._TOTAL.value]
        rrow = []

        # If the sum of the entries is more than the reported total, then we have
        # a problem: we need to normalize the data.
        if _total != _TOTAL and _total != 0:
            rrow = [sum(row[linenumber.AICVAP.value:])]
        else:
            rrow = [_TOTAL]

        return rrow + row[linenumber.AICVAP.value:]


    # Go through each row of the dataframe, assigning values to the appropriate
    # column (in chunks of 13 rows).
    pbar = tqdm(total=len(cvaps))
    while i < len(cvaps):
        geoid = cvaps.iloc[i]["geoid"].split("15000US")[1]
        county = geoid.split("48")[1][:3]

        row = []
        for line in range(0, 13):
            rrow = cvaps.iloc[i+line]
            cvap = rrow["adu_est"]
            row += [cvap]

        m = [geoid] + mapcvap(row)
        if county in ["157", "201", "339"]: rows += [m]
        i += 13
        pbar.update(13)

    cvapst = pd.concat([cvapst, pd.DataFrame(rows, columns=cols)])

    # Write the cvap data to file so we don't lose it!
    cvapst.to_csv(f"./data/demographics/acs-cvap-transposed/tx-bg-cvaps-t-{year}.csv", index=False)

# Write the codebook to a file.
with open("data/demographics/cvap-codebook.json", "w") as f:
    json.dump(book, f, indent=2)
