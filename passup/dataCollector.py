import pandas
from sodapy import Socrata

PASS_UP_DATA_ID = "mer2-irmb"               # used in API request to connect to pass-up data set
PASS_UP_MAX_ROWS = 170000                   # pass up data set contains around 160k rows
PASS_UP_TYPE_FULL = "Full Bus Pass-Up"      # we only want the rows with full bus pass-up type

# Unauthenticated client only works with public data sets. Note 'None'
# in place of application token, and no username or password:
# EXAMPLE: client = Socrata("data.winnipeg.ca", None)

# authenticated client (less throttling when sending requests):
client = Socrata(domain="data.winnipeg.ca",
                 app_token="VF3YwehWPH23DdQjpIcvm5YS1",
                 username="coopera@myumanitoba.ca",
                 password="Comp4710!")

# retrieve data from database via API request; get only Full Bus Pass-Up data (ignore wheelchair passups)
def getPassupData() -> pandas.DataFrame:
    queryStr = f"pass_up_type = '{PASS_UP_TYPE_FULL}'"      # only get rows with full pass-up type
    results = client.get(PASS_UP_DATA_ID, limit=PASS_UP_MAX_ROWS, where=queryStr)   # we get back JSON
    results_df = pandas.DataFrame.from_records(results)     # convert to data frame
    client.close()
    return results_df       # return a data frame