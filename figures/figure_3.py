import numpy as np
import matplotlib.pyplot as plt

def lcm(x, y):  
    if x > y:  
        greater = x  
    else:  
        greater = y  
    while(True):  
        if((greater % x == 0) and (greater % y == 0)):
            lcm = greater  
            break  
        greater += 1  
    return lcm  

def BFUsage(profiles):
    bottleneck_src = 0 if sum([profile[0] for profile in profiles]) > sum([profile[1] for profile in profiles]) else 1

    lcm_src = 1
    for profile in profiles:
        lcm_src = lcm(lcm_src, profile[bottleneck_src])

    for profile in profiles:
        for i in range(2):
            profile[i] = profile[i] * lcm_src / profile[bottleneck_src]
    
    sum_1 = sum([profile[0] for profile in profiles])
    sum_2 = sum([profile[1] for profile in profiles])
    max_sum = max(sum_1, sum_2)
    padding = [(max_sum - sum_1) * 100 / max_sum, (max_sum - sum_2) * 100 / max_sum]
    resources = []
    for profile in profiles:
        src = [source * 100 / max_sum for source in profile]
        resources.append(src)
    resources.insert(len(resources) - 1, padding)
    return resources

def plotFigure(resources, figureName):
    N = 2
    ind = np.arange(N)
    width = 0.35
    p1 = plt.bar(ind, resources[0], width, color='darkblue', edgecolor='black')
    p2 = plt.bar(ind, resources[1], width, bottom=resources[0], color='lightblue', edgecolor='black')
    _padding = plt.bar(ind, resources[2], width, bottom=np.array(resources[0]) + np.array(resources[1]), color='w', edgecolor='black')
    p3 = plt.bar(ind, resources[3], width, bottom=np.array(resources[0]) + np.array(resources[1]) + np.array(resources[2]), color='b', edgecolor='black')

    plt.grid(ls='--', axis='y', color='black')
    plt.xticks(ind, ('Link', 'CPU'))
    plt.yticks(np.arange(0, 110, 50), ('0%', '50%', '100%'))
    plt.legend((p1[0], p2[0], p3[0]), ('Flow 1', 'Flow 2', 'Flow 3'))

    plt.savefig(figureName)

plotFigure(BFUsage([[10, 1], [10, 14], [10, 14]]), 'figure_3a.png')
plotFigure(BFUsage([[10, 7], [10, 14], [10, 14]]), 'figure_3b.png')