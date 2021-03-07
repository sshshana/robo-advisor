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

The stock data retrieved through Alpha Vantage will be stored as a CSV file under the subdirectory called "data". The CSV file will be named as, for example, "stockdata_AAPL.csv".

The application will calcaulte the annualized return based on the most recent 


Here are some important tips that will help you use this application effectively:
 
 + If you want to send a copy of the receipt to a customer's email, enter `y` after the checkout. Then input the customer's email address as the program prompts.


> NOTE: if you see an error like "ModuleNotFoundError: No module named '...'", it's because the given package isn't installed, so run the `pip` command above to ensure that package has been installed into the virtual environment
