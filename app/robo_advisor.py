# this is the "app/robo_advisor.py" file

# Import all the modules and third-party packages that contain the functionality we need:
# We want to allow users choose their own user names by creating a separate virtual environment

import csv
import os
import requests
import json
from statistics import geometric_mean
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
    stock_symbols_st = input("""
        Please input a stock or cryptocurrency symbol.
        If you want to access multiple stocks at once,
        please give a space between symbols (e.g. AAPL MSFT TSLA)
        """)
    stock_symbols = list(stock_symbols_st.split(" "))

    if len(stock_symbols) > 5:
        print("The application can access only up to FIVE stocks at once. Please try again.")
    else:
        responses = []
        for stock_symbol in stock_symbols:
            if 1 <= len(stock_symbol) <= 5 and stock_symbol.isdecimal() == False:
                request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol={stock_symbol}&apikey={API_KEY}"
                response = requests.get(request_url)
                
                if response.status_code != 200 or "Error Message" in response.text:
                    print(f"Sorry, couldn't find any trading data for {stock_symbol}. Please try again.")
                    exit()
                else:
                    responses.append(response)

            else:
                print("Oh, expecting a properly-formed stock symbol like 'MSFT'. Please try again.")
                exit()
        break


#
# enter loop to get data from Alpha Vantage for all stocks of interest
#

for response in responses:
    parsed_response = json.loads(response.text)
    stock_name = parsed_response["Meta Data"]["2. Symbol"]
    last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]

    tsd = parsed_response["Weekly Time Series"]
    dates = list(tsd.keys())
    latest_day = dates[0]
    lastest_close = tsd[latest_day]["4. close"] # TODO: make sure the series is in a chronological order

    #
    # calculate 52-week high and 52-week low
    #

    # get high & low prices from weekly data
    high_prices = []
    low_prices = []
    i = 1 # to store weekly data of the recent 52 weeks
    for date in dates:
        if i > 52:
            break
        else:
            high_price = tsd[date]["2. high"]
            high_prices.append(float(high_price))
            low_price = tsd[date]["3. low"]
            low_prices.append(float(low_price))
            i += 1
    # maximum of all high prices & minimum of all low prices
    recent_high = max(high_prices)
    recent_low = min(low_prices)

    #
    # info outputs
    #

    csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", f"stockdata_{stock_name}.csv")

    csv_headers = ("date", "open", "high", "low", "close", "volume")
    with open(csv_file_path, "w") as csv_file: # "w" means "open the file for writing"
        writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
        writer.writeheader() # uses fieldnames set above

        # loop to write each row
        for date in dates:
            weekly_data = tsd[date]
            writer.writerow({
                "date": date,
                "open": float(weekly_data["1. open"]),
                "high": float(weekly_data["2. high"]),
                "low": float(weekly_data["3. low"]),
                "close": float(weekly_data["4. close"]),
                "volume": float(weekly_data["5. volume"])
                })


    # make a list of closed prices of the past 52 weeks
    closed_prices = []
    i = 1
    for date in dates:
        if i > 52:
            break
        else:
            closed_price = tsd[date]["4. close"]
            closed_prices.append(float(closed_price))
            i += 1

    # calculate weekly returns and make a list
    weekly_returns = []
    w = 0
    for w in range(len(closed_prices)-1):
        weekly_returns.append(closed_prices[50-w]/closed_prices[51-w]-1)

    # calcualte annualized return (using geometric average approach)

    weekly_returns_calc = [n+1 for n in weekly_returns]
    average_weekly_return = geometric_mean(weekly_returns_calc)-1 # geometric mean of weekly returns
    annualized_weekly_return = (average_weekly_return + 1)**51 - 1 # 52 weeks per year; 51 weekly returns per year
    formatted_return = "{}%".format(round(annualized_weekly_return*100, 2))

    # give recommendations based on the annualized return
    if annualized_weekly_return > 0.3:
        profitability = "HIGH"
        rec = "Buy the stock!"
        reason = f"""
        The stock's annualized return is {formatted_return},
        which is higher than 30% and, therefore, very promising!
        """
    elif annualized_weekly_return > 0.02: # assuming inflation rate is 2%
        profitability = "MEIDUM"
        rec = """
        It's up to you!
        It's not an ideal stock, but not a bad option as well.
        """
        reason = f"""
        The stock's annualized return is {formatted_return}.
        Neither super promising nor devastating.
        """
    else:
        profitability = "LOW"
        rec = "DO NOT buy the stock!"
        reason = f"""
        The stock's annualized return is {formatted_return},
        which is lower than the inflation rate.
        You'll be better off putting your money in your saving account.
        """

    # print the results
    print(f"""
    -------------------------
    RESULT PAGE: {responses.index(response)+1}/{len(responses)}
    SELECTED SYMBOL: {stock_name}
    -------------------------
    REQUESTING STOCK MARKET DATA...
    REQUEST AT: {today_date}
    -------------------------
    LATEST DAY: {last_refreshed}
    LATEST CLOSE: {to_usd(float(lastest_close))}
    52-WEEK HIGH: {to_usd(float(recent_high))}
    52-WEEK LOW: {to_usd(float(recent_low))}
    -------------------------
    STOCK'S EXPECTED RETURN: {profitability}
    RECOMMENDATION: {rec}
    RECOMMENDATION REASON: {reason}
    -------------------------
    WRITING DATA TO CSV... {csv_file_path}
    -------------------------
    HAPPY INVESTING!
    -------------------------
    """)





