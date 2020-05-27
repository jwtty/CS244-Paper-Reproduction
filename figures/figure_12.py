import numpy as np
import matplotlib.pyplot as plt
import FQ_simulation as FQ

#---------------------------------------------------------------
# Confirming resource shares in 4.2
pf1 = FQ.PFSimulator([FQ.Flow((4, 1)), FQ.Flow((1, 2))], maxTime = 2001)[0]
pf2 = FQ.PFSimulator([FQ.Flow((4, 2)), FQ.Flow((1, 2))], maxTime = 2001)[0]

print('Profile\t Resource 1 \t\t Resource 2')
print('<4, 1>:\t', pf1[0][1], '\t', pf1[0][2])
print('<1, 2>:\t', pf1[1][1], '\t', pf1[1][2], '\n')
print('<4, 2>:\t', pf2[0][1], '\t\t\t', pf2[0][2])
print('<1, 2>:\t', pf2[1][1], '\t\t\t', pf2[1][2])

#---------------------------------------------------------------
# Plotting Figure 12
# generate the 10 flows
flows = [FQ.Flow((20, 1), startTime = 0, endTime = 25000)]
flows += [FQ.Flow((20, 11), startTime = 25000, endTime = 50000)]
flows += [FQ.Flow((10, 11), startTime = 0, endTime = 50000) for i in range(9)]
# print(flows)
pf = FQ.PFSimulator(flows, maxTime = 50000, sampleSize = 800, bufferThreshold = 2)
_fig, axs = plt.subplots(2, 1)

# pf[time][flow][resource]
time = [pf[t][0][0] for t in range(len(pf))]
jobStyle = ['rs-', 'go-']
label = ['Flow 1 <20, 1>', 'Flow 2-10 <10, 11>']
# dominant resource 
dom1 = [max(pf[t][0][1]+pf[t][1][1], pf[t][0][2]+pf[t][1][2]) for t in range(len(pf))] 
axs[1].plot(time, dom1, jobStyle[0], label=label[0])
for i in range(2, 11):
    domRest = [max(pf[t][i][1], pf[t][i][2]) for t in range(len(pf))]
    if i == 2:
        axs[1].plot(time, domRest, jobStyle[1], label=label[1])
    else: axs[1].plot(time, domRest, jobStyle[1])

# setting axis labels
axs[0].set(xlabel='Time', ylabel='Dom. Share (DRFQ)')
axs[1].set(xlabel='Time', ylabel='Dom. Share (PF)')
axs[1].legend(loc = 'upper left')
for i in range(2):
    axs[i].grid(ls=':', color='black')
    axs[i].set_xlim([0, 50000])
    axs[i].set_ylim([0, 0.5])
    axs[i].label_outer()
plt.savefig('figure_12.png')
plt.show()

