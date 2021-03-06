# this is the "app/robo_advisor.py" file

# Import all the modules and third-party packages that contain the functionality we need:
# We want to allow users choose their own user names by creating a separate virtual environment

import csv
import os
import requests
import json
# from getpass import getpass

from dotenv import load_dotenv 
from datetime import datetime

def to_usd(my_price):
    return "${0:,.2f}".format(my_price)

#
# info inputs
#

today_date = datetime.now().strftime("%Y-%m-%d %I:%M %p")

load_dotenv() # read env var(API key) from the ".env" file (read README.md)
API_KEY = os.getenv("ALPHAVANTAGE_API_KEY") # uses the os module to read the specified environment variable and store it in a corresponding python variable


# preliminary input validation
while True:
    stock_symbol = input("Please input a stock or cryptocurrency symbol (e.g. MSFT, AAPL, etc.)")
    if 1 <= len(stock_symbol) <= 5 and stock_symbol.isdecimal() == False:
        request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={stock_symbol}&apikey={API_KEY}"
        response = requests.get(request_url)
        if response.status_code != 200 or "Error Message" in response.text:
            print("Sorry, couldn't find any trading data for that stock symbol. Please try again.")
        else:
            break
    else:
        print("Oh, expecting a properly-formed stock symbol like 'MSFT'. Please try again.")

#
# get data
#

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


csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", f"stockdata_{stock_symbol}.csv")

csv_headers = ("date", "open", "high", "low", "close", "volume")
with open(csv_file_path, "w") as csv_file: # "w" means "open the file for writing"
    writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
    writer.writeheader() # uses fieldnames set above

    # loop to write each row
    for date in dates:
        daily_data = tsd[date]
        writer.writerow({
            "date": date,
            "open": float(daily_data["1. open"]),
            "high": float(daily_data["2. high"]),
            "low": float(daily_data["3. low"]),
            "close": float(daily_data["4. close"]),
            "volume": float(daily_data["5. volume"])
            })



print("-------------------------")
print("SELECTED SYMBOL:", stock_symbol)
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print("REQUEST AT:", today_date)
print("-------------------------")
print("LATEST DAY:", last_refreshed)
print("LATEST CLOSE:", to_usd(float(lastest_close)))
print("RECENT HIGH:", to_usd(float(recent_high)))
print("RECENT LOW:", to_usd(float(recent_low)))
print("-------------------------")
print("RECOMMENDATION: BUY!")
print("RECOMMENDATION REASON: TODO")
print("-------------------------")
print("WRITING DATA TO CSV...", csv_file_path)
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")

