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

plt.title("SIR Model - infected") # title
plt.xlabel("time") # x label
plt.ylabel("population") # y label
plt.plot(t, I, color='r' , label='Infected') # plot the infected population
plt.plot(t, R, color='g', label='Recovered') # plot the recovered population
plt.plot(t, S, color='b', label='Susceptible') # plot the susceptible population
plt.plot(t, CI, color='k', label='Cumulative infected') # plot the cumulative infected population

plt.legend() # legend
plt.show() # show the plot