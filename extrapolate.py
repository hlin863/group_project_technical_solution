import warnings
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams.update({'font.size': 10})

beta, gamma = 0.9, 0.4 # effective contact rate, recovery rate
N = 1000 # population
t_end = 30 # time

R = [0] # Recovered Population
t = [0] # Elapsed Time
I = [10] # Infected Population
S = [N - I[0]] # Susceptible Population
CI = [0] # Cumulative Infected Population

Ptis = [] # List to store polyfit time intervals
Ps = [] # List to store polyfit data
Pts = [] # List to store polyfit time interval data

j = 0 # counter to track the time


while I[j] > 0 and t[j] < t_end:
    a = beta * S[j] * I[j] / N
    b = gamma * I[j]

    p_i = a / (a + b) # probability of infection
    p_r = b / (a + b) # probability of recovery

    u1 = np.random.uniform(0, 1) # random number to determine if infected
    u2 = np.random.uniform(0, 1) # random number to determine time

    # use infection data to predict future cases every 5 days. 
    if (j + 1) % 100 == 0:
        # polyfit to predict future cases

        with warnings.catch_warnings():
            # ignore warning for polyfit
            warnings.simplefilter("ignore")
            z = np.polyfit(x, y, 1) # fit a line to the data
            line = np.poly1d(z) # create a line based on the fit  
            # perform line formula on the x-axis
            p = line(x)
        
        Ptis.append(x) # store time interval
        Ps.append(line(x)) # stores polyfit data
        Pts.append(j + 1) # stores time interval

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

# plot polyfit onto a graph
for i in range(len(Ps)):
    plt.plot(Ptis[i], Ps[i], color='r', label='Fit ends at ' + str(Pts[i]))

plt.legend()
plt.show()