# mfinancials
Simple module for downloading financial statements and estimates from financials.morningstar.com

## Setup

Install using pip:

```
pip install mfinancials
```
or install from source:

```
git clone https://github.com/tobigs/mfinancials.git
cd mfinancials
python setup.py install
```

## Usage

### Basic usage

```python
import mfinancials as mf

# Apple, Inc.
aapl = mf.Ticker("aapl")

# financials from http://financials.morningstar.com/ratios/r.html?t=aapl
aapl.financials

# key ratios from from http://financials.morningstar.com/ratios/r.html?t=aapl
aapl.keyRatios

# estimates from financials.morningstar.com/valuation/earnings-estimates.html?t=aapl
aapl.estimates

# display like morningstar website
aapl.financials.T
aapl.keyRatios.T
aapl.estimates.T

# get urls to view data on morningstar website
aapl.url_estimates
aapl.url_financials
```

### Non-US stocks

Stocks not listed in the USA require either country or [Market Identifier Code (MIC)](https://en.wikipedia.org/wiki/Market_Identifier_Code).<br/>
It is generally advised to use country, mic only for not supported countries.

```python
# LVMH Moët Hennessy – Louis Vuitton SE
lvmh = mf.Ticker("mc", mic="XPAR")

# Samsung Electronics Co., Ltd.
smsng = mf.Ticker("005930", country="South Korea")

# list supported countries
smsng.countries
```

Some estimate data is in a different currency than the financials currency. To convert estimates use:

```python
# Alibaba Group Holding Limited
baba = mf.Ticker("baba")
baba.financials
baba.estimates
baba.estimatesConv

# access currencies
baba.currency_estimates
baba.currency_financials
```
