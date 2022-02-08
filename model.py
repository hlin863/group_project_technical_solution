import numpy as np
import matplotlib.pyplot as plt

plt.rcParams.update({'font.size': 22})

beta = 0.9  # Effective contact rate [1/min]
gamma = 0.4  # Recovery(+Mortality) rate[1/min]
N = 1000     # 𝑁=𝑆+𝐼+𝑅  is the total population
t_end = 30

Rs = []  # Recovered or Fatal (= Recovered + Fatal)
ts = []  # The elapsed time from the start date.
Is = []  # Infected (=Confirmed - Recovered - Fatal)
Ss = []  # Susceptible (= Population - Confirmed)
CIs = []  # Total cumulative cases

for i in range(3):
    R = [0]
    t = [0]
    I = [10]
    S = [N - I[0]]
    CI = [0]

    j = 0

    while I[j] > 0 and t[j] < t_end:
        a = beta * S[j] * I[j] / N
        b = gamma * I[j]

        p_i = a / (a + b)
        p_r = b / (a + b)

        u1 = np.random.uniform(0, 1)
        u2 = np.random.uniform(0, 1)

        if 0 < u1 <= p_i:
            S.append(S[j] - 1)
            I.append(I[j] + 1)
            CI.append(R[j] + I[j])
            # R.append(R[int(t[j])])
            R.append(R[j])
        elif p_i < u1 < 1:
            S.append(S[j])
            I.append(I[j] - 1)
            CI.append(R[j] + I[j])
            # R.append(R[int(t[j])] + 1)
            R.append(R[j] + 1)
        
        if S[j] + I[j] + R[j] != N:
                print('Population: ' + str(S[j] + I[j] + R[j]))
        
        t.append(t[j] - np.log(u2) / (a + b))
        j += 1
    
    Rs.append(R)
    ts.append(t)
    Is.append(I)
    Ss.append(S)
    CIs.append(CI)

plt.title("SIR Model - infected")
plt.xlabel("time")
plt.ylabel("population")
plt.plot(ts[0], Is[0], color='r' , label='Infected 1')
plt.plot(ts[0], Rs[0], color='g', label='Recovered 1')
plt.plot(ts[0], Ss[0], color='b', label='Susceptible 1')
plt.plot(ts[0], CIs[0], color='k', label='Cumulative infected 1')

# plt.plot(ts[0], Is[0] + Rs[0] + Ss[0], color='k', label='Total 1')
# plt.plot(ts[1], Is[1], color='r', label='Infected 2')
# plt.plot(ts[2], Is[2], color='g', label='Infected 3')
plt.legend()
plt.show()
