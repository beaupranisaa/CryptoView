#!/usr/local/bin/python3

import numpy as np
import pandas as pd

# Number of options
n = 8
options = ["cci", 'rsi', 'k_avg', 'sma', 'ema', 'macd', 'awesome', 'ultimate']

# Creating default matrix of ones
A = np.ones([n,n])
# Running a for loop to take input from user and populate the upper triangular elements
for i in range(0,n):
    for j in range(0,n):
         if i<j:
             aij = input('How important is {} over {} ?: '.format(options[i],options[j]))
             A[i,j] = float(aij) #Upper triangular elements
             A[j,i] = 1/float(aij) #Lower triangular elements

print('='*60)
print("Preference Matrix")
print(A)

print('='*60)

e = np.linalg.eig(A)[1][:,0]
p = np.abs(e/e.sum())

print("Weights")
print(p)

print('='*60)
print("Consistency Ratio (Should be less than 10%)")
print((np.mean(np.sum(A*p.T,axis=1)/p) - n)/(n-1)/1.41)
