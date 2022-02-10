import warnings
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

plt.rcParams.update({'font.size': 10})

beta, gamma = 0.9, 0.4 # effective contact rate, recovery rate
N = 1000 # population
t_end = 30 # time

def logistic_fit(t, a, b, c):
    # function to perform logistic fit
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

# variable to store the colors
colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']

while I[j] > 0 and t[j] < t_end:
    a = beta * S[j] * I[j] / N
    b = gamma * I[j]

    p_i = a / (a + b) # probability of infection
    p_r = b / (a + b) # probability of recovery

    u1 = np.random.uniform(0, 1) # random number to determine if infected
    u2 = np.random.uniform(0, 1) # random number to determine time

    if 0 < u1 <= p_i:
        S.append(S[j] - 1)
        I.append(I[j] + 1)
        CI.append(R[j] + I[j])
        R.append(R[j])
    elif p_i < u1 < 1:
        S.append(S[j])
        I.append(I[j] - 1)
        CI.append(R[j] + I[j])
        R.append(R[j] + 1)
        
    if S[j] + I[j] + R[j] != N:
        print('Population: ' + str(S[j] + I[j] + R[j]))
        
    t.append(t[j] - np.log(u2) / (a + b))
    j += 1

plt.title("SIR Model - infected")
plt.xlabel("time")
plt.ylabel("Infected population")
plt.plot(t, CI, color='k', label='Cumulative infected')

popt, popi = curve_fit(logistic_fit, t, CI)

print(str(popt[0]) + " " + str(popt[1]) + " " + str(popt[2]))

a_f = float(popt[0])
b_f = float(popt[1])
c_f = float(popt[2])

for i in range(0, len(t)):
    Ps.append(logistic_fit(t[i], a_f, b_f, c_f))

plt.plot(t, Ps, color='r', label='Logistic Fit')

plt.legend()
plt.show()