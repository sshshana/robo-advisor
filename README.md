# robo-advisor

This application will be able to help you make wise investment decisions.

## Prerequisites

  + Anaconda 3.7+
  + Python 3.7+
  + Pip

## Installation

Clone or download [remote repository](https://github.com/sshshana/robo-advisory). Choose a familiar download location such as Desktop.

Then navigate into the project repository:

```sh
cd ~/Desktop/robo-advisor
```

Use Anaconda to create and activate a new virtual environment, perhaps called "robo-advisor-env":

```sh
conda create -n stocks-env python=3.8 
conda activate stocks-env
```
In your new virtual environment, install package dependencies:

```sh
pip install -r requirements.txt
```

> NOTE: if this command throws an error like "Could not open requirements file: [Errno 2] No such file or directory", make sure you are running it from the repository's root directory, where the requirements.txt file exists (see the initial `cd` step above)


## Setup
Before using this application, you need an API Key to issue requests to the [AlphaVantage API Key](https://www.alphavantage.co/). Please click the link and get your API Key. (e.g. "abc123")

Then, in your project repository, create an .env file and set a variable called `ALPHAADVANTAGE_API_KEY` and assign the value of your API key as a string. Please see the example below:

```sh
ALPHAVANTAGE_API_KEY="abc123"
```


## Usage
Run the application. The application is in the subdirectory called "app":

```py
python app/robo_advisor.py
```

Once launched, the application will ask you to enter the stock symbol of your interest. Please follow the insturctions the applicaiton prompts.

> NOTE: Free version of Alpha Vantage has a volume limit of requests: 5 API requests per minute; 500 API requests per day. The application will accept up to five stock inputs at once to prevent any error. In certain use cases that exceed the limit, consider getting [a premium plan](https://www.alphavantage.co/premium/#:~:text=Alpha%20Vantage%20Premium%20API%20Key,-Welcome%20to%20Premium&text=In%20certain%20use%20cases%20that,help%20you%20scale%20your%20application.) Alpha Vantage offers.

Once you enter the symbol, historical data of the past 20+ years will be retrieved, and the application will create a plot of the adjusted close stock prices. All stocks that you choose will be plotted on a single chart.

If you close the window that shows the chart, the application will give you more detailed information of selected stock(s), including latest adjusted close price, 52-week high, and 52-week low.

> NOTE: In order to mitigate the confusion caused by the stock split, this application regards the maximum and minimum of the stock's adjusted close prices as **52-week high and 52-week low**. 

The application also calculates the annualized return based on the data, following the steps below:
 1. Retrieve adjusted close stock prices of the past 52 weeks.
 2. Calculate wekly returns.
 3. Calcaulte geometric average of the weekly returns.
 4. Annualize the calculated geometric-average return.

Based on the annualized return, the application will tell you whether the expected return on the stock is **high** (return > 30%), **medium** (30% => return > 2%), or **low** (return <=2%). It will also provide you the reason for its evaluation.

The retrieved stock data will be stored as a CSV file under the subdirectory called "data". The CSV file will be named as, for example, "stockdata_AAPL.csv", "stockdata_MSFT.csv",  etc.

> NOTE: If you see an error like "ModuleNotFoundError: No module named '...'", it's because the given package isn't installed, so run the `pip` command above to ensure that package has been installed into the virtual environment
