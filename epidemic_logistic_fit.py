import warnings
import numpy as np # import numpy
import matplotlib.pyplot as plt # library to plot the data
from scipy.optimize import curve_fit # library to perform curve fitting

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

print(sample_time) # print the sample time
print(sample_infected) # print the sample data

plt.plot(sample_time, sample_infected, color = 'k') # plot the sample data
plt.xlabel('Time (days)') # x-axis label
plt.ylabel('Cumulative Infected Population') # y-axis label
plt.title('Cumulative Infected Population vs. Time') # title
plt.show() # show the plot
