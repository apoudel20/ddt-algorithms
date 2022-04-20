import random

import numpy as np
import matplotlib.pyplot as plt

np.random.seed(200)
class SourceSimulator():
    def __init__(self,n_groups, m_sources, group_count_requirements = None, tuple_count_per_source = None):

        N_GROUPS = n_groups # two categories in each group
        M_SOURCES = m_sources
        SOURCE_GROUP_DIST = np.random.rand(N_GROUPS * M_SOURCES).reshape(M_SOURCES, N_GROUPS) # distribution probabilities for group satisfaction by source
        TUPLE_COUNT_PER_SOURCE = np.random.randint(20,100, M_SOURCES) if tuple_count_per_source is None else tuple_count_per_source
        GROUP_COUNT_REQUIREMENTS = np.random.randint(10,20, N_GROUPS) if group_count_requirements is None else group_count_requirements

        print("SIMULATION PARAMETERS")
        print("Tuples per source", TUPLE_COUNT_PER_SOURCE)
        print("Group count requirements", GROUP_COUNT_REQUIREMENTS)
        print("Source group satisfaction probability distribution\n", SOURCE_GROUP_DIST)

        print("SIMULATION RESULTS")
        # SIMULATING THE SOURCES

        self.sources = [
            [
                    [np.random.choice((0,1), p = (1-x,x)) for x in y
                    ] for k in range(TUPLE_COUNT_PER_SOURCE[i])
                ] for i,y in enumerate(SOURCE_GROUP_DIST)
            ]

        # SIMULATED SOURCES

        bars = np.array(GROUP_COUNT_REQUIREMENTS)
        for i, source in enumerate(self.sources):
            print("Source", i,":", source)
            bars = np.vstack((
                bars,
                np.count_nonzero(source, axis = 0)
                ))
        self.bars = bars
        print("Counts per sources: \n",self.bars)
    # PLOTTING COUNTS PER GROUP
    def plot(self):
        bar_labels = ['Required Counts','Source 0','Source 1', 'Source 2', 'Source 3']

        X_axis = np.arange(len(bar_labels))
            
        plt.bar(X_axis - 0.3, self.bars[:,0], 0.3, label = 'Group 0')
        plt.bar(X_axis, self.bars[:,1], 0.3, label = 'Group 1')
        plt.bar(X_axis + 0.3, self.bars[:,2], 0.3, label = 'Group 2')
            
        plt.xticks(X_axis, bar_labels)
        plt.xlabel("Sources")
        plt.ylabel("Counts fulfilling groups")
        plt.title("Distribution of required groups across sources")
        plt.legend()
        plt.show()

# USAGE

ddt_sim = SourceSimulator(3,4, [10] * 3)
ddt_sim.plot()

