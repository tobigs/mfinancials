#!/usr/bin/env python

from base import TickerBase

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

class Ticker(TickerBase):

    def __repr__(self):
        return 'mfinance.Ticker object <%s>' % self.ticker

    @property
    def financials(self):
        return self.get_financials()

    @property
    def estimates(self):
        return self.get_estimates()

    @property
    def keyRatios(self):
        return self.get_keyRatios()

if __name__ == "__main__":
    aapl = Ticker("AAPL")