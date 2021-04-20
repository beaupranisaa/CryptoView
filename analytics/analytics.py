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

def signal_indicator(close, values, macd_signal, ao_prev):
    if values[0] > 100 and values[0] < 150:
        signal_cci = 'SELL'
    elif values[0] < -100 and values[0] > -150:
        signal_cci = 'BUY'
    elif values[0] >= 150:
        signal_cci = 'STRONG SELL'
    elif values[0] <= -150:
        signal_cci = 'STRONG BUY'
    else: 
        signal_cci = 'NEUTRAL'

    if values[1] > 0 and values[1] < 20:
        signal_rsi = 'BUY'
    elif values[1] > 80 and values[1] < 100:
        signal_rsi = 'SELL'
    elif values[1] > 100:
        signal_rsi = 'STRONG SELL'
    elif values[1] < 0:
        signal_rsi = 'STRONG BUY'
    else:
        signal_rsi = 'NEUTRAL'

    if close > values[2]:
        signal_kama = 'BUY'
    else: 
        signal_kama = 'SELL'

    if values[3] or values[4] > close:
        signal_sma = 'BUY'
        signal_ema = 'BUY'
    elif values[3] == close and values[4] == close:
        signal_sma = 'NEUTRAL'
        signal_ema = 'NEUTRAL'
    else:
        signal_sma = 'SELL'
        signal_ema = 'SELL'
    
    if values[5] > macd_signal:
        signal_macd = 'BUY'
    elif values[5] < macd_signal:
        signal_macd = 'SELL'
    else:
        signal_macd = 'NEUTRAL'

    if ao_prev < values[6]: 
        signal_awesome = 'BUY'
    elif ao_prev > values[6]: 
        signal_awesome = 'SELL'
    else:
        signal_awesome = 'NEUTRAL'

    if values[7] >= 0 and values[7] <= 30:
        signal_ultimate = 'BUY'
    elif values[7] < 0:
        signal_ultimate = 'STRONG BUY'
    elif values[7] >= 70 and values[7] < 100:
        signal_ultimate = 'SELL'
    elif values[7] >= 100:
        signal_ultimate = 'STRONG SELL'
    else:
        signal_ultimate = 'NEUTRAL'
    signals = [signal_cci, signal_rsi, signal_kama, signal_sma, 
                        signal_ema, signal_macd, signal_awesome, signal_ultimate] 
    return signals