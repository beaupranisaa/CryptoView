# -*- coding: utf-8 -*-
"""
Created on Wed Feb 22 12:46:39 2021

@author: Romen Samuel Wabina
"""
import numpy as np
import pandas as pd
from ta import add_all_ta_features
from ta.utils import dropna
from sklearn import preprocessing

def normalize_indicator(data):
    scaler = preprocessing.MinMaxScaler()
    normalized_data = scaler.fit_transform(data)
    return normalized_data

def moving_averages(df):
    sma_fast = df['trend_sma_fast']
    sma_slow = df['trend_sma_slow']
    return sma_fast, sma_slow

def prices(df):
    timestamp = df.index
    open = df['open']
    high = df['high']
    close = df['close']
    low = df['low']
    return timestamp, open, high, close, low

def relative_strength(df):
    momentum_rsi = df['momentum_rsi']
    momentum_stoch_rsi = df['momentum_stoch_rsi']
    momentum_stoch_rsi_k = df['momentum_stoch_rsi_k']
    return momentum_rsi, momentum_stoch_rsi, momentum_stoch_rsi_k

def macd_signals(df):
    macd_line = df['trend_macd']
    signal_line = df['trend_macd_signal']
    return macd_line, signal_line

def commodity_channel(df):
    cci_signal = df['trend_cci']
    return cci_signal