#!/usr/bin/env python

from .base import TickerBase

from . import params
from . import utils

import datetime
import re
import json

from bs4 import BeautifulSoup
from numpy import nan

import requests

import pandas as pd
import yfinance as yf

class Tickers():

    def __repr__(self):
        return 'mfinance.Tickers object <%s>' % ",".join(self.symbols)

    def __init__(self, tickers):
        tickers = tickers if isinstance(
            tickers, list) else tickers.replace(',', ' ').split()
        self.symbols = [ticker.upper() for ticker in tickers]
        ticker_objects = {}

        for ticker in self.symbols:
            ticker_objects[ticker] = Ticker(ticker)

        self.tickers = _namedtuple(
            "Tickers", ticker_objects.keys(), rename=True
        )(*ticker_objects.values())