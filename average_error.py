import numpy as np # import numpy
import matplotlib.pyplot as plt # library to plot the data
from scipy.optimize import curve_fit # library to perform curve fitting

beta, gamma = 0.9, 0.4 # beta and gamma constants
N = 1000 # sample population
t_end = 30 # time

def simulate(beta, gamma, N, t_end): # simulation function
    
    """
    
    simulate function to simulate the different population groups using the SIR model.

    :param beta: constant for determining the probability of infection
    :param gamma: constant for determining the probability of recovery
    :param N: sample population
    :param t_end: time

    :return: CI - cumulative infected population
    :return: t - time

    """
    
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

        j += 1

    return CI, t  # return the cumulative infected population and the time

def logistic_fit(t, a, b, c):
    
    """
    logisitic fit function to fit the data to the logistic curve.

    :param t: time
    :param a: constant for determining the probability of infection
    :param b: constant for determining the probability of recovery
    :param c: constant for determining the probability of recovery

    :return: y - the fitted curve

    """

    return a / (1 + b * np.exp(-c * t))

time_frames = [3, 6, 9, 12, 15, 18, 21, 24, 27, 30] # time frames

for i in range(0, 30, 3): # loop to run the simulation 10 times
    CI, t = simulate(beta, gamma, N, t_end) # run the simulation

    sample_infected = CI[i // 3 : (i // 3) + 1] # sample the infected population
    sample_time = t[i // 3 : (i // 3) + 1] # sample the time

    p0 = [1000, 10, 1] # initialize p0 as initial population

    popt, pcov = curve_fit(logistic_fit, sample_time, sample_infected, p0) # perform curve fitting

    a_f = popt[0] # fitted constant for determining the probability of infection
    b_f = popt[1] # fitted constant for determining the probability of recovery
    c_f = popt[2] # fitted constant for determining the probability of recovery

    for i in range(len(t)):
        sample_infected.append(logistic_fit(t[i], a_f, b_f, c_f)) # append the fitted curve to the sample infected population

    # find the difference between the last data point of the sample_infected and CI
    error = abs(sample_infected[-1] - CI[-1])

    print("The average error for the time frame of " + str(time_frames[i // 3]) + " is " + str(error)) # print the average error