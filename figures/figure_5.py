import numpy as np
import matplotlib.pyplot as plt
import copy
import math

def lcm(x, y):  
    return abs(x * y) // math.gcd(x, y)

# Given the resource profile of each job, and bottleneck resource
# Return the resource share of each job
def BFScheduler(profiles, bottleneck):
    numSrc = len(profiles[0])
    curProfiles = copy.deepcopy(profiles)
    lcm_src = 1
    for profile in curProfiles:
        lcm_src = lcm(lcm_src, profile[bottleneck])
    for profile in curProfiles:
        times = lcm_src / profile[bottleneck]
        for i in range(numSrc):
            profile[i] = profile[i] * times
    total = max([sum([profile[i] for profile in curProfiles]) for i in range(numSrc)])
    share = []
    for profile in curProfiles:
        src = [source / total for source in profile]
        share.append(src)
    return share

def BFSimulator(profiles):
    numJob, numSrc = len(profiles), len(profiles[0])
    bottleneck = 0
    # Test for 200 seconds with statistics collected per 5 seconds
    numData = 40
    statistics = np.zeros((numSrc, numJob, numData))
    for i in range(numData):
        # Change bottleneck every 30 secs as stated in the paper
        if i != 0 and i % 6 == 0:
            bottleneck = bottleneck + 1
            if bottleneck == numSrc:
                bottleneck = 0
        share = BFScheduler(profiles, bottleneck)
        for jobIndex in range(numJob):
            for srcIndex in range(numSrc):
                statistics[srcIndex][jobIndex][i] = share[jobIndex][srcIndex]
    return statistics

def plotFigure(datapoints, labels, figureName):
    numSrc, numJob, _ = datapoints.shape
    _fig, axs = plt.subplots(numSrc, 1)
    x = np.arange(5, 205, 5)
    jobStyle = ['gs-', 'bo-', 'rD-']
    for srcIndex in range(numSrc):
        for jobIndex in range(numJob):
            axs[srcIndex].plot(x, datapoints[srcIndex][jobIndex], jobStyle[jobIndex], label=labels[jobIndex])
        axs[srcIndex].set(xlabel='Time', ylabel='Resource ' + str(srcIndex + 1) + ' Share')
        axs[srcIndex].grid(ls=':', color='black')
        axs[srcIndex].set_xlim([0, 200])
        axs[srcIndex].set_ylim([0, 1.0])
        axs[srcIndex].set_xticks([0, 50, 100, 150, 200])
    axs[0].legend()
    for ax in axs.flat:
        ax.label_outer()
    plt.savefig(figureName)
   
plotFigure(BFSimulator([[6, 1], [1, 7], [1, 1]]), ['Flow 1 <6, 1>', 'Flow 2 <1, 7>', 'Flow 3 <1, 1>'], 'figure_5.png')
        