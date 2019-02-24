# If you are unfamiliar with Jupyter Notebook

To fully leverage on StocksCafe API and this library, you would need to have some knowledge of Jupyter Notebook. No worries though, it is easy to learn and I highly recommend this easy to follow [lecture by Quantopian](https://www.quantopian.com/lectures/introduction-to-research) to start with.

<br/>

# Quick Start (to run this on the web)

### Step 1 - Run Binder

https://mybinder.org/v2/gh/StocksCafe/Quant/master

Binder allows you to create custom computing environments that can be shared and used by many remote users. It is an non-profit project funded with grants from the Moore Foundation and the Google Cloud Platform.

<br/>

### Step 2 - Change StocksCafe() usage

For all usages of StocksCafe() in Jupyter Notebook, change it to StocksCafe(apiUser='YOUR_USERNAME', apiUserKey='YOUR_API_KEY').

Explanation: When we use call StocksCafe(), we are actually reading api-key.txt file for your username and api key. Since Binder is running on a shared environment, we cannot upload these sensitive credentials there.

To find your API Key, goto https://stocks.cafe/user/profile (if your API Key is NULL, please click on the "Renew API Key" link).

Note: API keys are available only to Friends of StocksCafe.

<br/>

### Step 3 - Have fun!

I recommend to start with this notebook => "[evankoh] Plot Moving Average Chart.ipynb"

Note: The output would be sent to the output folder. Please goto into it and view the corresponding html file. Enjoy!

<br/>

# Quick Start (to install on your local drive)

### Step 1 - Install Git

https://git-scm.com/book/en/v2/Getting-Started-Installing-Git

<br/>

### Step 2 - Clone this repository

Command prompt: `git clone https://github.com/StocksCafe/Quant.git`

<br/>

### Step 3 - Install Jupyter Notebook

https://jupyter.org/install.html

<br/>

### Step 4 - Install additional required libraries

Command prompt: `pip install plotly` (or `pip3 install plotly` if pip fails)

<br/>

### Step 5 - Edit sample.api-key.txt and rename it to api-key.txt

1) Please rename sample.api-key.txt to api-key.txt (sample.api-key.txt is located where you clone the repository to in Step 2)

2) Replace the entire first line with your StocksCafe username, and the entire second line with your API key, which can be found on https://stocks.cafe/user/profile
(if your API Key is NULL, please click on the "Renew API Key" link).

Note: API keys are available only to Friends of StocksCafe.

<br/>

### Step 6 - Have fun!

Command prompt: `jupyter notebook`

I recommend to start with [this notebook](https://github.com/StocksCafe/Quant/blob/master/%5Bevankoh%5D%20Plot%20Moving%20Average%20Chart.ipynb)

<br/>

# (Optional) If you want to learn more about python

To be effective in using this library, you would need to have some knowledge of Python programming language. No worries though, it is one of the easiest programming language to learn. I recommend to read [this tutorial](https://thomas-cokelaer.info/tutorials/python/basics.html) to start with.



