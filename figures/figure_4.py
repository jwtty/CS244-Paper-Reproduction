import numpy as np
import matplotlib.pyplot as plt

def DRFUsage(R, demands):
    numRes = R.shape[0]
    numUser = demands.shape[0]
    
    consumed = np.zeros(numRes)
    dominant = np.zeros(numUser)
    usage = np.zeros((numUser, numRes))

    while (True):
        pickedUser = np.argmin(dominant)
        canAllocate = np.all(np.greater_equal(R, consumed + demands[pickedUser]))
        if not canAllocate:
            break
        consumed = consumed + demands[pickedUser]
        usage[pickedUser] = usage[pickedUser] + demands[pickedUser]
        dominant[pickedUser] = np.amax(usage[pickedUser] / R)
    usage = np.insert(usage, 1, R - np.sum(usage, axis=0), axis=0)
    return usage * 100 / R

def plotFigure(resources, figureName):
    N = 2
    ind = np.arange(N)
    width = 0.45
    p1 = plt.bar(ind, resources[0], width, color='darkblue', edgecolor='black')
    _padding = plt.bar(ind, resources[1], width, bottom=resources[0], color='w', edgecolor='black')
    p2 = plt.bar(ind, resources[2], width, bottom=resources[0] + resources[1], color='lightblue', edgecolor='black')

    plt.grid(ls='--', axis='y', color='black')
    plt.xticks(ind, ('r1', 'r2'))
    plt.yticks(np.arange(0, 110, 50), ('0%', '50%', '100%'))
    plt.legend((p1[0], p2[0]), ('job 1', 'job 2'))
    plt.savefig(figureName)

plotFigure(DRFUsage(np.array([2000, 2000]), np.array([[4, 1], [1, 3]])), 'figure_4.png')