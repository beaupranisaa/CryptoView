# -*- coding: utf-8 -*-
"""
Created on Wed Feb 22 12:46:39 2021

@author: Romen Samuel Wabina
"""
import numpy as np
import pandas as pd
from ta import add_all_ta_features #pip install ta
from ta.utils import dropna


df = pd.read_csv('BTCUSDT-1h-data.csv', sep = ',')
df = dropna(df)
df = add_all_ta_features(df, open="open", high = "high", low="low", close="close", 
                           volume="volume", fillna=True)

def moving_averages():
    sma_fast = df['trend_sma_fast']
    sma_slow = df['trend_sma_slow']
    return sma_fast, sma_slow

def prices():
    timestamp = df['timestamp']
    open = df['open']
    high = df['high']
    close = df['close']
    low = df['low']
    return timestamp, open, high, close, low

def relative_strength():
    momentum_rsi = df['momentum_rsi']
    momentum_stoch_rsi = df['momentum_stoch_rsi']
    momentum_stoch_rsi_k = df['momentum_stoch_rsi_k']
    return momentum_rsi, momentum_stoch_rsi, momentum_stoch_rsi_k

def macd_signals():
    macd_line = df['trend_macd']
    signal_line = df['trend_macd_signal']
    return macd_line, signal_line

def commodity_channel():
    cci_signal = df['trend_cci']
    print(cci_signal)
    return cci_signal

#print(df.columns)

    