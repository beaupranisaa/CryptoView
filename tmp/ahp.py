#!/usr/local/bin/python3

import numpy as np
import pandas as pd

# Number of options
n = 3
# Creating default matrix of ones
A = np.ones([n,n])
# Running a for loop to take input from user and populate the upper triangular elements
for i in range(0,n):
    for j in range(0,n):
         if i<j:
             aij = input('How important is option{} over option{} ?: '.format(i,j))
             A[i,j] = float(aij) #Upper triangular elements
             A[j,i] = 1/float(aij) #Lower triangular elements

print(A)

e = np.linalg.eig(A)[1][:,0]
p = np.real(e/e.sum())

print(p)

print(A*p.T)

print(np.sum(A*p.T,axis=1))

print(np.sum(A*p.T,axis=1)/p)

print(np.mean(np.sum(A*p.T,axis=1)/p))

print((np.mean(np.sum(A*p.T,axis=1)/p) - n)/(n-1)/0.58)
