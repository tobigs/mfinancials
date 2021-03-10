#%%
import mfinancials as mf

#%% Apple, Inc.
aapl = mf.Ticker("aapl")

#%% financials from http://financials.morningstar.com/ratios/r.html?t=aapl
aapl.financials

#%% key ratios from from http://financials.morningstar.com/ratios/r.html?t=aapl
aapl.keyRatios

#%% estimates from financials.morningstar.com/valuation/earnings-estimates.html?t=AAPL
aapl.estimates

#%% display like morningstar website
aapl.financials.T
aapl.keyRatios.T
aapl.estimates.T

#%% get urls to view data on morningstar website
aapl.url_estimates
aapl.url_financials

#%% LVMH Moët Hennessy – Louis Vuitton SE
lvmh = mf.Ticker("mc", mic="XPAR")

#%% Samsung Electronics Co., Ltd.
smsng = mf.Ticker("005930", country="South Korea")

#%% list supported countries
smsng.countries

#%% Alibaba Group Holding Limited
baba = mf.Ticker("baba")
baba.financials
baba.estimates
baba.estimatesConv


#%% access currencies
baba.currency_estimates
baba.currency_financials

# %%
