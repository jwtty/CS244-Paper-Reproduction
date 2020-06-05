import numpy as np 
import matplotlib.pyplot as plt
# These arrays should be filled with results output from NS2 simulation
flows = [[9,10,10,10,10,6,5,5,5,5,4,3,3,4,3,4,5,5,5,5,5,5,5,5,5,5,5,5,5,6,10,10,10,10,10], 
         [0,0,0,0,0,4,5,5,5,5,3,4,3,3,4,4,5,5,5,5,5,5,5,5,5,5,5,5,5,4,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0,3,3,4,3,3,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]

profiles = [[2, 10], [10, 4], [3, 10]]
N = 35

source1 = np.zeros((3, N))
for i in range(N):
    total = sum([10 * flows[j][i] for j in range(3)])
    for j in range(3):
        source1[j][i] = (1.0 * profiles[j][0] * flows[j][i]) / (1.0 * total)

source2 = np.zeros((3, N))
for i in range(N):
    total = sum([10 * flows[j][i] for j in range(3)])
    for j in range(3):
        source2[j][i] = (1.0 * profiles[j][1] * flows[j][i]) / (1.0 * total)

dominant = np.maximum(source1, source2)

_fig, axs = plt.subplots(3, 1)

x = np.arange(0, 35)
data = [source1, source2, dominant]

label = ['Flow 1', 'Flow 2', 'Flow 3']
ylabels = ['CPU Share', 'Bandwidth Share', 'Dominant Share']
styles = ['b-', 'r--', 'k:']

for i in range(3):
    for j in range(3):
        axs[i].plot(x, data[i][j], styles[j], label=label[j])
    axs[i].set(xlabel='Time (s)', ylabel=ylabels[i])
    axs[i].legend(loc = 'upper center', ncol=3)
    axs[i].set_yticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
plt.savefig('figure_9.png')
plt.show()