import numpy as np

def SFQScheduler(flows):
    """
    Takes in a list of Flow
    """
    return

class Flow:
    def __init__(self, profile, startTime = 0, endTime = 2000):
        self.profile = profile
        self.startTime = startTime
        self.endTime = endTime
        return 
    def active(self, time):
        return time >= self.startTime and time <= self.endTime


def PFScheduler(flows, maxTime = 2000, timeStep = 0.1, bufferThreshold = 1): # For two resources
    """
    Takes in a list of Flow
    """
    packetsProcessed = [0 for i in range(len(flows))]
    packetInProcess1 = [0 for i in range(len(flows))]
    packetInProcess2 = [0 for i in range(len(flows))]
    buffer = [0 for i in range(len(flows))]
    for t in range(round(maxTime/timeStep)):
        time = t * timeStep
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
        #print('buffer:', buffer)
        #print('packets processed:', packetsProcessed)
        #print('packetInProcess2', packetInProcess2)

    total = [[0, 0]] * len(flows)
    maxResource = [0, 0]
    for i in range(len(flows)):
        total[i] = [total[i][j] + packetsProcessed[i] * flows[i].profile[j] for j in range(2)]
        maxResource = [maxResource[j] + packetsProcessed[i] * flows[i].profile[j] for j in range(2)]
    maxResource = max(maxResource)
    share = [[total[i][j] / maxResource for j in range(2)] for i in range(len(flows))]
    print(share)
    return packetsProcessed


PFScheduler([Flow((4, 1)), Flow((1, 2))])
PFScheduler([Flow((4, 2)), Flow((1, 2))])
