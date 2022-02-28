import warnings
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

plt.rcParams.update({'font.size': 10})

def logistic_fit(t, a, b, c):
    # function to perform logistic fit
    return a / (1 + b * np.exp(-c * t))

beta = 0.9  # Effective contact rate [1/min]
gamma = 0.4  # Recovery(+Mortality) rate[1/min]
N = 1000  # the total population 𝑁=𝑆+𝐼+𝑅
t_end = 30 # time

R = [0]  # Recovered or Fatal (= Recovered + Fatal)
t = [0]  # The elapsed time from the start date
I = [10]  # Infected (=Confirmed - Recovered - Fatal)
S = [N - I[0]]  # Susceptible (= Population - Confirmed)
CI = [0] # Cumulative Infected Population

j = 0 # counter to track the time

# variable to store the colors
colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']

while I[j] > 0 and t[j] < t_end: # code to generate the CI and t data.
    a = beta * S[j] * I[j] / N
    b = gamma * I[j]

    p_i = a / (a + b) # probability of infection
    p_r = b / (a + b) # probability of recovery
    
    # random number to determine if infected
    u1 = np.random.uniform(0, 1) 
    # random number to determine time
    u2 = np.random.uniform(0, 1) 

    if 0 < u1 <= p_i:
        S.append(S[j] - 1) # updates the susceptible population
        I.append(I[j] + 1) # updates the infected population
        CI.append(R[j] + I[j]) # updates the cumulative infected population
        R.append(R[j]) # updates the recovered population
    elif p_i < u1 < 1:
        S.append(S[j]) # updates the susceptible population
        I.append(I[j] - 1) # updates the infected population
        CI.append(R[j] + I[j]) # updates the cumulative infected population
        R.append(R[j] + 1) # updates the recovered population
        
    t.append(t[j] - np.log(u2) / (a + b))
    j += 1

print(len(CI))
    
