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
 
You will need an API Key to issue requests to the [AlphaVantage API](https://www.alphavantage.co/). Please visit the alphavantage.co thorugh the link and get your API Key.

Then, in your project repository, create an .env file and set a variable called `ALPHAADVANTAGE_API_KEY` and assign the value of your API key as a string. Please see the example below:

```sh
ALPHAVANTAGE_API_KEY="abc123"
```


> NOTE: If you don't update your API key, it will be set as abc123 by default.







## Setup

In your project repository, update sales_tax_rate variable in the ".env" file according to your city's sales tax rate. Please see the exmaple below (which assumes the tax rate is 8.75%):

```sh
sales_tax_rate=8.75
```
> NOTE: Do not include percentage sign (%) in the code
> NOTE: If you don't customize your tax rate, it will be use New York City's sales tax rate of 8.75%


## Usage
Run the program and follow the instructions the system prompts:

```py
python shopping-cart.py
```

Here are some important tips that will help you use this program effectively:

 + Please verify that you enter the correct identifier of the product you want to scan.

 + If the item is priced by pound, the program will ask you to enter the pound of the product. Please follow the instructions.

 + Enter `DONE` once you complete scanning all the products you have. Then the program will proceed to checkout.
 
 + If you want to send a copy of the receipt to a customer's email, enter `y` after the checkout. Then input the customer's email address as the program prompts.



> NOTE: if you see an error like "ModuleNotFoundError: No module named '...'", it's because the given package isn't installed, so run the `pip` command above to ensure that package has been installed into the virtual environment
