import warnings
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams.update({'font.size': 10})

beta = 0.9  # Effective contact rate [1/min]
gamma = 0.4  # Recovery(+Mortality) rate[1/min]
N = 1000  # the total population 𝑁=𝑆+𝐼+𝑅
t_end = 30 # time

R = [0]  # Recovered or Fatal (= Recovered + Fatal)
t = [0]  # The elapsed time from the start date
I = [10]  # Infected (=Confirmed - Recovered - Fatal)
S = [N - I[0]]  # Susceptible (= Population - Confirmed)
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
    
    # random number to determine if infected
    u1 = np.random.uniform(0, 1) 
    # random number to determine time
    u2 = np.random.uniform(0, 1) 

    if (j + 1) % 100 == 0:
        # print('Time: ' + str(t[j]))

        x = t[:j + 1]
        y = CI[:j + 1]
        
        # extrapolate using x and y values
        fit = np.polyfit(x, y, 3)

        line = np.poly1d(fit)
        if len(x) == len(line(x)) == len(y):
            print("Line size: " + str(len(line(x))))
        
        Ptis.append(x)
        Ps.append(line(x))
        Pts.append(int(t[j]))

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
colori = 0
for i in range(len(Ps)):
    colori += 1
    if colori == len(colors):
        colori = 0
    # print("color index: " + str(colori))
    plt.plot(Ptis[i], Ps[i], color=colors[colori], label='Fit ends at ' + str(Pts[i]))

plt.legend()
plt.show()
