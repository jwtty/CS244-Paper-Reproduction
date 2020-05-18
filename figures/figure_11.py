import numpy as np
import matplotlib.pyplot as plt

class Flow:
    def __init__(self, profile, startTime = 0, endTime = 10000):
        self.profile = profile
        self.startTime = startTime
        self.endTime = endTime
        return 
    def active(self, time):
        return time >= self.startTime and time <= self.endTime

def sample(packetsProcessed, flows, time):
    total = [[0, 0]] * len(flows)
    maxResource = [0, 0]
    for i in range(len(flows)):
        total[i] = [total[i][j] + packetsProcessed[i] * flows[i].profile[j] for j in range(2)]
        maxResource = [maxResource[j] + packetsProcessed[i] * flows[i].profile[j] for j in range(2)]
    maxResource = max(maxResource)
    if maxResource == 0:
        return [[time] + [0 for j in range(2)] for i in range(len(flows))]
    else: return [[time] + [total[i][j] / maxResource for j in range(2)] for i in range(len(flows))]



def SFSimulator(flows, maxTime = 15000, timeStep = 0.1, sampleTime = 2000, sampleSize = 1000): # For two resources
    """
    Single-resource Fair Queuing (For the first resource)
    """
    packetsProcessed = [0 for i in range(len(flows))]
    packetInProcess = [0 for i in range(len(flows))]
    samples = []

    for t in range(round(maxTime/timeStep)):
        time = t * timeStep

        # measure the share of a sample 
        if time > 0 and time % sampleTime == 0:
            samples.append(sample(packetsProcessed, flows, time))
        if time > 0 and time % sampleSize == 0:
            packetsProcessed = [0 for i in range(len(flows))]

        # counting active flows for resource 1
        activeFlowNum = 0
        for i in range(len(flows)): 
            if flows[i].active(time): activeFlowNum += 1
        for i in range(len(flows)):
            if flows[i].active(time):
                if packetInProcess[i] <= 0:
                    packetInProcess[i] = flows[i].profile[0]
                packetInProcess[i] -= timeStep/activeFlowNum
                if packetInProcess[i] <= 0: # finish processing a packet for rsc 1
                    packetsProcessed[i] += 1

    return samples


def PFSimulator(flows, maxTime = 15000, timeStep = 0.1, bufferThreshold = 1, \
    sampleTime = 2000, sampleSize = 1000): # For two resources
    """
    Per-Resource Fairness
    """

    packetsProcessed = [0 for i in range(len(flows))]
    packetInProcess1 = [0 for i in range(len(flows))]
    packetInProcess2 = [0 for i in range(len(flows))]
    buffer = [0 for i in range(len(flows))]
    samples = []

    for t in range(round(maxTime/timeStep)):
        time = t * timeStep

        # measure the share of a sample 
        if time > 0 and time % sampleTime == 0:
            samples.append(sample(packetsProcessed, flows, time))
        if time > 0 and time % sampleSize == 0:
            packetsProcessed = [0 for i in range(len(flows))]

        # counting active flows for resource 1
        activeFlowNum = 0
        for i in range(len(flows)): # a flow is only competing for resource 1 if the buffer for rsc 2 is not full
            if flows[i].active(time) and buffer[i] < bufferThreshold: activeFlowNum += 1
        for i in range(len(flows)):
            if flows[i].active(time) and buffer[i] < bufferThreshold:
                if packetInProcess1[i] <= 0:
                    packetInProcess1[i] = flows[i].profile[0]
                packetInProcess1[i] -= timeStep/activeFlowNum
                if packetInProcess1[i] <= 0: # finish processing a packet for rsc 1
                    buffer[i] += 1

        # counting active flows for resource 2
        activeFlowNum = 0
        for i in range(len(flows)):
            if packetInProcess2[i] > 0 or buffer[i] > 0:
                activeFlowNum += 1
        for i in range(len(flows)):
            if packetInProcess2[i] <= 0 and buffer[i] > 0:
                packetInProcess2[i] = flows[i].profile[1]
                buffer[i] -= 1
            if packetInProcess2[i] > 0:
                packetInProcess2[i] -= timeStep/activeFlowNum
                if packetInProcess2[i] <= 0: # finish processing a packet
                    packetsProcessed[i] += 1      

    return samples


#---------------------------------------------------------------
# Plotting Figure 11
pf = SFSimulator([Flow((0.1, 1), startTime = 15000, endTime = 85000), \
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

