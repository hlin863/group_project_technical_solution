'''
Simulate 100 times and determine the error rate by comparing the simulation data with the synthetic data.
Produce a graph using the average number of errors generated from the list of the error rates.
'''

import numpy as np # import numpy
import matplotlib.pyplot as plt # library to plot the data
from scipy.optimize import curve_fit # library to perform curve fitting

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

def simulation_synthetic(beta, gamma, N, t_end, R, t, I, S, CI):
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
    
    return I, t

def simulation_projected(beta, gamma, N, t_end, R, t, I, S, CI):

    j = 0 # counter to track the time

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

    sample_size = 20 # sample size

    sample_infected = [] # list to store the sample infected data
    sample_time = [] # initialize sample_time

    # iterate through the sample data with steps of 20
    for i in range(0, len(t) - 1, sample_size):
        sample_infected.append(CI[i]) # append infection data to sample data
        sample_time.append(t[i]) # append time data to sample data

    plt.plot(sample_time, sample_infected, color = 'k') # plot the sample data
    plt.scatter(sample_time, sample_infected, color = 'r') # plot the individual data points

    # split the sample_data into 5 sections to plot 5 lines
    sample_infected_1 = sample_infected[0:int(len(sample_infected)/5)] # first section
    sample_time_1 = sample_time[0:int(len(sample_time)/5)] # first section

    sample_infected_2 = sample_infected[0:int(len(sample_infected)/5)*2] # second section
    sample_time_2 = sample_time[0:int(len(sample_time)/5)*2] # second section

    sample_infected_3 = sample_infected[0:int(len(sample_infected)/5)*3] # third section
    sample_time_3 = sample_time[0:int(len(sample_time)/5)*3] # third section

    sample_infected_4 = sample_infected[0:int(len(sample_infected)/5)*4] # fourth section
    sample_time_4 = sample_time[0:int(len(sample_time)/5)*4] # fourth section

    sample_infected_5 = sample_infected[0:int(len(sample_infected))] # fifth section
    sample_time_5 = sample_time[0:int(len(sample_time))] # fifth section

    def sample_simulation(total_time, sample_t, sample_infected, fit_function): # function to perform simulation on the samples.

        sample_output = [] # initialize sample_output

        p0 = [1000, 10, 1] # initialize p0 as initial population

        popt, pcov = curve_fit(fit_function, sample_t, sample_infected, p0) # perform curve fitting on the sample data

        a_f = float(popt[0]) # a_f is the fitted parameter a
        b_f = float(popt[1]) # b_f is the fitted parameter b
        c_f = float(popt[2]) # c_f is the fitted parameter c

        for i in range(0, len(total_time)): # iterate through the total time
            sample_output.append(logistic_fit(total_time[i], a_f, b_f, c_f)) # append the fitted data to the sample_output list

        return sample_output

    sample_1_output = sample_simulation(t, sample_time_1, sample_infected_1, logistic_fit) # perform simulation on the first section
    sample_2_output = sample_simulation(t, sample_time_2, sample_infected_2, logistic_fit) # perform simulation on the second section
    sample_3_output = sample_simulation(t, sample_time_3, sample_infected_3, logistic_fit) # perform simulation on the third section
    sample_4_output = sample_simulation(t, sample_time_4, sample_infected_4, logistic_fit) # perform simulation on the fourth section
    sample_5_output = sample_simulation(t, sample_time_5, sample_infected_5, logistic_fit) # perform simulation on the fifth section

    return sample_1_output, sample_2_output, sample_3_output, sample_4_output, sample_5_output

I, t = simulation_synthetic(beta, gamma, N, t_end, R, t, I, S, CI) # simulates the synthetic data

for index in range(100):
    sample_1_I, sample_2_I, sample_3_I, sample_4_I, sample_5_I = simulation_projected(beta, gamma, N, t_end, R, t, I, S, CI) # simulates the projected data

    # combine the sample_1_I, sample_2_I, sample_3_I, sample_4_I, sample_5_I into one list
    sample_I = sample_1_I + sample_2_I + sample_3_I + sample_4_I + sample_5_I

    # find the difference between the I and sample I
    differences = []

    for j in range(len(I)):

        differences.append(abs(I[j] - sample_I[j]))

plt.title("Error between the synthetic and projected data")
plt.xlabel("Time")
plt.ylabel("Error")
plt.plot(t, differences, color = 'k')
plt.show()