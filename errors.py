'''
Simulate 100 times and determine the error rate by comparing the simulation data with the synthetic data.
Produce a graph using the average number of errors generated from the list of the error rates.
'''

import numpy as np # import numpy
import matplotlib.pyplot as plt # library to plot the data

plt.rcParams.update({'font.size': 12}) # set font size

beta, gamma = 0.9, 0.4 # beta and gamma constants
N = 1000 # sample population
t_end = 30 # time

R = [0] # initialise the recovered list
t = [0] # initialise the time list
I = [10] # initialise the infected list
S = [N - I[0]] # initialise the susceptible list
CI = [0] # initialise the cumulative infected list

def simulation(N, t_end, R, t, I, S, CI): # function to generate the synthetic and simulated data

    beta, gamma = 0.9, 0.4 # beta and gamma constants

    j = 0 # counter to track the time

    while I[j] > 0 and t[j] < t_end:
        a = beta * S[j] * I[j] / N # calculate the a constant
        b = gamma * I[j] # calculate the b constant

        p_i = a / (a + b) # calculate the probability of infection
        p_r = b / (a + b) # calculate the probability of recovery

        u1 = np.random.uniform(0, 1) # generate a random number u1
        u2 = np.random.uniform(0, 1) # generate a random number u2

        if 0 < u1 <= p_i: # if infected
            S.append(S[j] - 1) # updates the susceptible population
            I.append(I[j] + 1) # updates the infected population
            CI.append(R[j] + I[j]) # updates the cumulative infected population
            R.append(R[j]) # updates the recovered population
        elif p_i < u1 < 1: # if an individual recovered
            S.append(S[j]) # updates the susceptible population
            I.append(I[j] - 1) # updates the infected population
            CI.append(R[j] + I[j]) # updates the cumulative infected population
            R.append(R[j] + 1) # updates the recovered population

        t.append(t[j] - np.log(u2) / (a + b)) # updates the time

        j += 1

    return R, t, I, S, CI

real_R, real_t, real_I, real_S, real_CI = simulation(beta, gamma, N, t_end, R, t, I, S, CI) # synthetic data 

for i in range(100):

    R, t, I, S, CI = simulation(N, t_end, R, t, I, S, CI) # simulate data

    differences = [] # list to store the differences

    for j in range(len(real_I)): # iterate through the synthetic data

        difference = abs(real_I[j] - I[j]) # calculate the difference between the synthetic and simulated data

        differences.append(difference) # append the difference to the list

plt.title("SIR Model - ERRORS") # title
plt.xlabel("Time") # x-axis label
plt.ylabel("Number of Errors") # y-axis label
plt.plot(real_t, differences) # plot the data
plt.show() # show the graph