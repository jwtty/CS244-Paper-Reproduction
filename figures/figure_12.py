import numpy as np
import matplotlib.pyplot as plt
import figure_11 as util



#---------------------------------------------------------------
# Plotting Figure 11
pf = util.SFSimulator([Flow((0.1, 1), startTime = 15000, endTime = 85000), \
    Flow((1, 1), startTime = 0, endTime = 100000)], maxTime = 100000)
_fig, axs = plt.subplots(3, 1)

time = [pf[t][0][0] for t in range(len(pf))]
jobStyle = ['go-', 'bD-']
label = ['Flow 1 <0.1, 1>', 'Flow 2 <1, 1>']
for i in range(2): # for each flow
    rsc1 = [pf[t][i][1] for t in range(len(pf))] # resource 1
    rsc2 = [pf[t][i][2] for t in range(len(pf))] # resource 2
    dom = [max(pf[t][i][1], pf[t][i][2]) for t in range(len(pf))] # dominant resource 
    axs[2].plot(time, rsc1, jobStyle[i])
    axs[1].plot(time, rsc2, jobStyle[i])
    axs[0].plot(time, dom, jobStyle[i], label=label[i])

# setting axis labels
axs[2].set(xlabel='Time', ylabel='Res. 1 Share')
axs[1].set(xlabel='Time', ylabel='Res. 2 Share')
axs[0].set(xlabel='Time', ylabel='Dom. Share')
axs[0].legend(loc = 'center right')

plt.savefig('figure_11.png')
plt.show()

