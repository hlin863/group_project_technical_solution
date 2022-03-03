import warnings
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

plt.rcParams.update({'font.size': 10})

beta, gamma = 0.9, 0.4 # effective contact rate, recovery rate
N = 1000 # population
t_end = 30 # time

def logistic_fit(t, a, b, c): # function to perform logistic fit
    return a / (1 + b * np.exp(-c * t))

R = [0] # Recovered Population
t = [0] # Elapsed Time
I = [10] # Infected Population
S = [N - I[0]] # Susceptible Population
CI = [0] # Cumulative Infected Population

Ptis = [] # List to store polyfit time intervals
Ps = [] # List to store polyfit data
Pts = [] # List to store polyfit time interval data

j = 0 # counter to track the time

colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k'] # variable to store the colors

while I[j] > 0 and t[j] < t_end:
    a = beta * S[j] * I[j] / N # constant a
    b = gamma * I[j] # constant b

    p_i = a / (a + b) # probability of infection
    p_r = b / (a + b) # probability of recovery

    u1 = np.random.uniform(0, 1) # random number to determine if infected
    u2 = np.random.uniform(0, 1) # random number to determine time

    if 0 < u1 <= p_i: # if infected
        S.append(S[j] - 1) # updates the susceptible population
        I.append(I[j] + 1) # updates the infected population
        CI.append(R[j] + I[j]) # updates the cumulative infected population
        R.append(R[j]) # updates the recovered population
    elif p_i < u1 < 1: # if recovered
        S.append(S[j]) # updates the susceptible population
        I.append(I[j] - 1) # updates the infected population
        CI.append(R[j] + I[j]) # updates the cumulative infected population
        R.append(R[j] + 1) # updates the recovered population
        
    if S[j] + I[j] + R[j] != N: # checks whether the total population is correct
        print('Population: ' + str(S[j] + I[j] + R[j]))
        
    t.append(t[j] - np.log(u2) / (a + b)) # updates the elapsed time
    j += 1

plt.title("SIR Model - infected") # title
plt.xlabel("time") # x-axis label
plt.ylabel("Infected population") # y-axis label
plt.plot(t, CI, color='k', label='Cumulative infected') # plot cumulative infected

popt, popi = curve_fit(logistic_fit, t, CI) # perform logistic fit

print(str(popt[0]) + " " + str(popt[1]) + " " + str(popt[2])) # print the parameters

a_f = float(popt[0]) # constant a
b_f = float(popt[1]) # constant b
c_f = float(popt[2]) # constant c

for i in range(0, len(t)): # for each time interval
    Ps.append(logistic_fit(t[i], a_f, b_f, c_f)) # calculate the logistic fit

plt.plot(t, Ps, color='r', label='Logistic Fit') # plot logistic fit

plt.legend() # legend
plt.show() # show the plot