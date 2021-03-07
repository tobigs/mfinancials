#!/usr/bin/env python

import params
import utils

import datetime
import re
import json

from bs4 import BeautifulSoup
from numpy import nan

import requests

import pandas as pd
import yfinance as yf

class TickerBase():
    def __init__(self, ticker, country="USA"):
        self.ticker = ticker.upper()
        self._url_base = 'http://financials.morningstar.com/finan/financials/'
        self._url_financialsBase = self._url_base + 'getFinancePart.html?&callback=xxx&t={}'
        self._url_keyRatiosBase = self._url_base + 'getKeyStatPart.html?&callback=xxx&t={}'
        self._url_estBase = 'http://financials.morningstar.com/valuate/annual-estimate-list.action?&t={}'

        self._currencies = params.currencies
        self._exchanges = params.exchanges

        self.countries = list(params.exchanges.keys())
        self.country = country

        self.mic = self._exchanges[self.country]
        self._ticker_full = f"{self.mic}:{self.ticker}"

        self._url_financials = self._url_financialsBase.format(self._ticker_full)
        self._url_keyRatios = self._url_keyRatiosBase.format(self._ticker_full)
        self._url_est =  self._url_estBase.format(self._ticker_full)

        self._financials = None
        self._keyRatios = None
        self._estimates = None

        self.currency_financials = None
        self.currency_estimates = None

    def _get_currency(self, df):
        """[summary]

        Args:
            df ([type]): [description]
        """    

        mylist = df.index.str.split().tolist()
        mylist = utils.flatten(mylist)

        currencies = [item for item in mylist if item in self._currencies]

        if len(set(currencies)) > 1:
            mode = pd.Series(currencies).mode()

            if mode.shape[0] > 1:
                currency = '+'.join(mode.tolist())

            else:
                currency = mode.mode()[0]

        else:
            currency = currencies[0]
            
        return currency
        

    def _get_annualData(self, dataType):
        """[summary]

        Args:
            ticker ([type]): [description]

        Returns:
            [type]: [description]
        """

        if dataType == "financials":
            if self._financials is not None:
                return
            url = self._url_financials
        else:
            if self._keyRatios is not None:
                return
            url = self._url_keyRatios


        # Credit to Andrej Kesely
        # https://stackoverflow.com/users/10035985/andrej-kesely
        # https://stackoverflow.com/questions/56691753/cant-find-table-using-beautiful-soup-on-morningstar

        soup = BeautifulSoup(json.loads(re.findall(
            r'xxx\((.*)\)', requests.get(url).text)[0])['componentData'], 'lxml'
        )

        table = utils.get_table(soup)
        df = pd.DataFrame(table[1:], columns=table[0])
        df = df.replace("—", nan)

        index_col = df.columns[0]
        df = df.set_index(index_col)

        if dataType == "financials":
            self.currency_financials = self._get_currency(df)
            df = df.rename_axis(index={"X": f"Financials {self.currency_financials}"})
            
        df = df.T

        if dataType == "financials":
            self._financials = df
        else:
            self._keyRatios = df
        


    def _get_estimateData(self):
        """[summary]

        Args:
            ticker ([type]): [description]

        Returns:
            [type]: [description]
        """

        df = pd.read_html(self._url_est)[0]

        df = df.dropna(how='all', axis=0)
        df = df.dropna(how='all', axis=1)
        df = df.replace("—", nan)
        df.iloc[0,:] = df.iloc[0,:].bfill()

        columns = df.pop(0).tolist()
        columns[:2] = ["Year", "Estimates"]

        df = df.T
        df.columns = columns
        df = df.set_index(["Year", "Estimates"])

        currency_est = df.index[0][1]
        df.rename_axis(index={"Estimates": f"Estimates {currency_est}"})
        df = df.astype(float, errors='ignore')
        df.loc[:,"Number of Estimates"] = df.loc[:,"Number of Estimates"].bfill()
        df.loc[:,"Number of Estimates"] = df.loc[:,"Number of Estimates"].astype(pd.Int64Dtype(), errors='ignore')
        
        # Inconsitent results
        # Either file bug report or find mistake
        # df.index = df.index.set_levels(
        #     levels=[f"Earnings Per Share {currency_est}", 'Growth %'],
        #     level="Estimates"
        # )

        df.index = utils.rename_MultiIndex(df.index, currency_est)

        self._estimates = df


    def _conv_currency(self):

        if self.currency_financials is None:
            print("Can't convert estimate currency, please get finacials data first.")
            return
        
        elif self.currency_estimates is None:
            print("Can't convert estimate currency, please get estimate data first.")
            return

        currency_from = self.currency_estimates
        currency_to = self.currency_financials

        if self._estimates is not None:
            return
        
        df = self._estimates

        columns = df.columns[:-1]
        rows = ~df.index.get_level_values(1).str.contains("%")
        df.loc[rows,columns]

        start = datetime.date.today() - datetime.timedelta(days=7)
        end = datetime.date.today()

        forex = yf.download(
            str(currency_from) + str(currency_to) + "=X",
            start=start, end=end,
        )

        # most recent close
        df.loc[rows,columns] = df.loc[rows,columns] * forex["Close"][-1]

        # Inconsitent results
        # Either file bug report or find mistake(sortorder?)
        # df.index =  df.index.set_levels(
        #     levels=[f"Earnings Per Share {currency_to}", 'Growth %'],
        #     level="Estimates",
        # )

        df.index = utils.rename_MultiIndex(df.index, currency_to)

        return df

    def get_financials(self):
        self._get_annualData("financials")
        return self._financials

    def get_keyRatios(self):
        self._get_annualData("keyRatios")
        return self._keyRatios

    def get_estimates(self):
        self._get_estimateData()
        return self._estimates

if __name__ == "__main__":
    aapl = TickerBase("AAPL")
    aapl.get_keyRatios()


