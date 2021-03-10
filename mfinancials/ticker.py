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

class Ticker(TickerBase):

    def __repr__(self):
        return 'mfinance.Ticker object <%s>' % self.ticker

    @property
    def financials(self):
        return self._get_financials()

    @property
    def estimates(self):
        return self._get_estimates()

    @property
    def keyRatios(self):
        return self._get_keyRatios()
    
    @property
    def estimatesConv(self):
        return self._get_estimatesConv()
