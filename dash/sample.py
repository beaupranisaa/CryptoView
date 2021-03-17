# -*- coding: utf-8 -*-
"""
Created on Tue Feb 23 09:25:37 2021

@author: Romen Samuel
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from IPython.display import clear_output
class SIRSI_MODEL():
    def __init__(self, beta0, beta1, h, Iw, T, transmission = 'Periodic'):
        self.beta0 = beta0
        self.beta1 = beta1
        self.h = h
        self.T = T
        self.M = T/h
        self.Iw = Iw
        self.k1 = 0.00005111486
        self.k2 = 0.00032621758
        self.a = 1
        self.time = np.array(range(0, T))
        self.transmission = str(transmission)
        self.gamma = 10 ** 7
        
        assert self.beta0 <= self.beta1
    
    def main(self):
        Sd, IHd, Rd = self.init_birds()
        S, I = self.init_humans()
        Sd, IHd, Rd, S, I = self.compartment_sirsi()
        #plot = self.plot_model(Sd, IHd, Rd, S, I)
        return Sd, IHd, Rd, S, I

    def compartment_sirsi(self):
        lambda_d, omega1, mu_d, nu_Hd, Lambda, beta, mu, nu = self.model_params()
        Sd, IHd, Rd = self.init_birds()
        S, I = self.init_humans()
        for i in range(self.T - 1):
            if self.transmission == 'Periodic':
                beta_w = self.beta0 + self.beta1 * np.cos(2 * np.pi/52 * self.a * self.time[i])
            
            else:
                beta_w = self.transmission_type()
            
            #Forward Euler
            Sd[i + 1] = Sd[i] + self.h * (lambda_d - beta_w * self.Iw * Sd[i] - mu_d * Sd[i])
            IHd[i + 1] = IHd[i] + self.h * (beta_w * self.Iw * Sd[i] - (mu_d + nu_Hd) * IHd[i])
            Rd[i + 1] = (mu_d + nu_Hd) * IHd[i]
            S[i + 1] = S[i] + self.h * (Lambda + beta * IHd[i] * S[i] - mu * S[i])
            I[i + 1] = I[i] + self.h * (beta * IHd[i] * S[i] - (mu + nu) * I[i])
        
        for compartment in [Sd, IHd, Rd, S, I]:
            assert compartment.shape[0] == self.T
        return Sd, IHd, Rd, S, I

    def transmission_type(self):
        if self.transmission == 'Periodic':
            beta_w = self.beta0 
        
        elif self.transmission == 'Non-Periodic':
            beta_w = self.beta0 + self.beta1 * -1 + np.random.uniform(0, 1) * 2
        
        elif self.transmission == 'Temperature-driven':
            #beta_w = pd.read_csv('Global Temperature NASA.csv')
            #beta_w = beta_w.to_numpy()
            TRAINING_SET = './data/train/*.csv'
            dataset = load_dataset()
            beta_w = dataset.readDataset(TRAINING_SET)
        return beta_w
    
    def model_params(self):
        lambda_d = 1020/365
        omega1 = 107.75
        mu_d = 1 / (2 * 365)
        nu_Hd = 0.3
        Lambda = 1000/365
        beta = 1.9e-11
        mu = 1 / (65*365)
        nu = 0.15
        return lambda_d, omega1, mu_d, nu_Hd, Lambda, beta, mu, nu
            
    def init_birds(self):
        Sd = np.zeros(self.T)
        IHd = np.zeros(self.T)
        Rd = np.zeros(self.T)
        Sd[1] = 1975.27
        IHd[1] = 1.77
        return Sd, IHd, Rd
    
    def init_humans(self):
        S = np.zeros(self.T)
        I = np.zeros(self.T)
        S[1] = 65000
        I[1] = 0.00047
        return S, I
     
    def plot_model(self, Sd, IHd, Rd, S, I):
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize = (12, 5))
        clear_output(wait=True)
        ax1.plot(self.time, IHd * self.gamma, 'b', label = 'Susceptible birds', lw = 3)
        ax1.plot(self.time, Sd * self.gamma, 'r', label = 'Infected birds', lw = 3)
        ax1.plot(self.time, Rd * self.gamma, 'orange', label = 'Recovered birds', lw = 3)
        ax1.set_xlabel('Weeks', size = 15)
        ax1.set_ylabel('Number of cases', size = 15)
        ax1.set_xlim(0, 500)
        ax1.set_title(f'{self.transmission} Transmission with \n {int(self.beta0 * 100)}% Baseline Transmission and {int(self.beta1 * 100)}% Virus deviation', size = 10)
        ax1.legend()

        ax2.plot(self.time, IHd * self.gamma, 'b', label = 'Susceptible birds', lw = 3)
        ax2.plot(self.time, Sd * self.gamma, 'r', label = 'Infected birds')
        ax2.plot(self.time, Rd * self.gamma, 'orange', label = 'Recovered birds')
        ax2.set_xscale('symlog')
        ax2.set_xlabel('Weeks', size = 15)
        ax2.set_ylabel('Number of cases', size = 15)
        ax2.set_xlim(0, 500)
        ax2.set_title(f'{self.transmission} Transmission with \n {int(self.beta0 * 100)}% Baseline Transmission and {int(self.beta1 * 100)}% Virus deviation', size = 10)
        ax2.legend()
        plt.tight_layout

avian = SIRSI_MODEL(beta0 = 1, beta1 = 1, h = 0.1, Iw = 5, T = 1655, transmission = 'Periodic')
avian.main()