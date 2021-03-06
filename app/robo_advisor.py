# this is the "app/robo_advisor.py" file

# Import all the modules and third-party packages that contain the functionality we need:
# We want to allow users choose their own user names by creating a separate virtual environment

import os
import requests
import json
# from getpass import getpass

from datetime import datetime
from dotenv import load_dotenv 

load_dotenv() # read env var(API key) from the ".env" file (read README.md)
API_KEY = os.getenv("ALPHAVANTAGE_API_KEY", default="abc123") # uses the os module to read the specified environment variable and store it in a corresponding python variable

def to_usd(my_price):
    """
    Converts a numeric value to usd-formatted string, for printing and display purposes.

    Param: my_price (int or float) like 4000.444444

    Example: to_usd(4000.444444)

    Returns: $4,000.44
    """
    return "${0:,.2f}".format(my_price) #f"${my_price:,.2}" #> $12,000.71


#
# info inputs
#

current_time = datetime.now().strftime("%Y-%m-%d")

request_url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=TSLA&apikey={API_KEY}"
response = requests.get(request_url)
# print(type(response)) # <class 'requests.models.Response'>
# print(response.status_code) # 200
# print(response.text) # string output of the object

parsed_response = json.loads(response.text)

last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]

tsd = parsed_response["Time Series (Daily)"]
dates = list(tsd.keys()) # TODO: assumes first day is on top, but consider shorting to ensure latest day is first
latest_day = dates[0]
lastest_close = tsd[latest_day]["4. close"]

# get high & low price from each day
high_prices = []
low_prices = []
for date in dates:
    high_price = tsd[date]["2. high"]
    high_prices.append(float(high_price))
    low_price = tsd[date]["3. low"]
    low_prices.append(float(low_price))
# maximum of all high prices / minimum of all low prices
recent_high = max(high_prices)
recent_low = min(low_prices)



#
# info outputs
#

print("-------------------------")
print("SELECTED SYMBOL: XYZ")
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print("REQUEST AT:", current_time) # shopping cart project
print("-------------------------")
print("LATEST DAY:", last_refreshed)
print("LATEST CLOSE:", to_usd(float(lastest_close)))
print("RECENT HIGH:", to_usd(float(recent_high)))
print("RECENT LOW:", to_usd(float(recent_low)))
print("-------------------------")
print("RECOMMENDATION: BUY!")
print("RECOMMENDATION REASON: TODO")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")
