import numpy as np
import matplotlib.pyplot as plt
import PF_simulation as PF

#---------------------------------------------------------------
# Confirming resource shares in 4.2
pf1 = PF.PFSimulator([PF.Flow((4, 1)), PF.Flow((1, 2))], maxTime = 2001)[0]
pf2 = PF.PFSimulator([PF.Flow((4, 2)), PF.Flow((1, 2))], maxTime = 2001)[0]

print('Profile\t Resource 1 \t\t Resource 2')
print('<4, 1>:\t', pf1[0][1], '\t', pf1[0][2])
print('<1, 2>:\t', pf1[1][1], '\t', pf1[1][2], '\n')
print('<4, 2>:\t', pf2[0][1], '\t\t\t', pf2[0][2])
print('<1, 2>:\t', pf2[1][1], '\t\t\t', pf2[1][2])

#---------------------------------------------------------------
# Plotting Figure 12
# generate the 10 flows
flows = [PF.Flow((20, 1), startTime = 15000, endTime = 85000)]
pf = PF.PFSimulator([PF.Flow((0.1, 1), startTime = 15000, endTime = 85000), \
    PF.Flow((1, 1), startTime = 0, endTime = 100000)], maxTime = 100000)
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

