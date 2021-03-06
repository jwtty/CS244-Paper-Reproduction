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
    total = [[0, 0] for i in range(len(flows))]
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
        if time % sampleTime < sampleTime - sampleSize:
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

def DRFSimulator(flows, maxTime = 15000, timeStep = 0.1, sampleTime = 2000, sampleSize = 1000): # For two resources
    """
    Memoryless Dominant Resource Fair Queuing 
    """
    packetsProcessed = [0 for i in range(len(flows))]
    virtualTime = [[-1, -1] for i in range(len(flows))] # (virtual start time, virtual end time) of the first packet in flow
    samples = []
    curVirtualTime = 0 # system virtual time V(t)
    flowInProcess, leftProcessTime = -1, 0.0 # flow being processed currently

    for t in range(round(maxTime/timeStep)):
        time = t * timeStep

        # measure the share of a sample 
        if time > 0 and time % sampleTime == 0:
            samples.append(sample(packetsProcessed, flows, time))
        if time > 0 and time % sampleSize == 0:
            packetsProcessed = [0 for i in range(len(flows))]

        # process current flow
        if flowInProcess != -1:
            leftProcessTime -= timeStep
            if leftProcessTime <= 0:
                packetsProcessed[flowInProcess] += 1
                flowInProcess = -1
        else:
            # schedule flow with the smallest virtual start time to process
            minVirtualStartTime = -1
            for i in range(len(flows)):
                if flows[i].active(time):
                    if virtualTime[i][0] == -1:
                        virtualTime[i][0] = curVirtualTime
                        virtualTime[i][1] = virtualTime[i][0] + max(flows[i].profile)
                    if minVirtualStartTime == -1 or virtualTime[i][0] < minVirtualStartTime:
                        minVirtualStartTime = virtualTime[i][0]
                        flowInProcess = i
            # update system virtual time, flow virtual start and finish time
            curVirtualTime = virtualTime[flowInProcess][0]
            leftProcessTime = virtualTime[flowInProcess][1] - virtualTime[flowInProcess][0]
            virtualTime[flowInProcess][0] = virtualTime[flowInProcess][1]
            virtualTime[flowInProcess][1] = virtualTime[flowInProcess][0] + max(flows[flowInProcess].profile)

    return samples

