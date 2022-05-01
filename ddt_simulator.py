import random

import numpy as np
import matplotlib.pyplot as plt

np.random.seed(2000)
class SourceSimulator():
    def __init__(self,n_groups = 3, m_sources = 4, group_count_requirements = None, tuple_count_per_source = None, access_costs = None, simulate_sources = False, plot = False):


        self.n_groups = n_groups # two categories in each group
        self.m_sources = m_sources
        self.group_count_requirements = np.random.randint(10,20, n_groups) if group_count_requirements is None else group_count_requirements
        self.access_costs = np.random.randint(10,50, m_sources) if access_costs is None else np.array(access_costs)
        
        # Generating source group distributions for the simulator as well as the tuple count per source.
        self.source_group_dist = np.random.rand(m_sources * n_groups).reshape(m_sources, n_groups) # distribution probabilities for group satisfaction by source
        self.tuple_count_per_source = np.random.randint(20,100, m_sources) if tuple_count_per_source is None else tuple_count_per_source

        print("Source group satisfaction probability distribution\n", self.source_group_dist)
        print("Source access costs", self.access_costs)

        self.simulate_sources = simulate_sources
        self.plot = plot

        if(self.simulate_sources):
            self.source_simulation()

    def source_simulation(self):
        """
        Simulates sources if called
        """
        self.simulate_sources = True

        print("*** SIMULATION PARAMETERS ***")
        
        print("Tuples per source", self.tuple_count_per_source)
        print("Group count requirements", self.group_count_requirements)

        print("*** SIMULATION RESULTS ***")
        
        if(self.simulate_sources):
            self.sources = [
                [
                        [np.random.choice((0,1), p = (1-x,x)) for x in y
                        ] for k in range(self.tuple_count_per_source[i])
                    ] for i,y in enumerate(self.source_group_dist)
                ]

        # SIMULATED SOURCES

        bars = np.array(self.group_count_requirements)

        for i, source in enumerate(self.sources):
            print("Source", i,":", source)
            bars = np.vstack((
                bars,
                (np.count_nonzero(source, axis = 0)
                #  / (max(self.access_costs) - min(self.access_costs)
                )
                ))
        bars[1:] = bars[1:] / np.min(bars[1:])
        self.bars = bars
        print("Counts per sources: \n",self.bars)

        if(self.plot):
            self.plot_simulation()


    def plot_simulation(self):
        """
        Plots counts fulfilment per group if the sources are simulated
        """
        self.plot = True # enabled when called directly
        if(self.simulate_sources and self.plot):

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
        else:
            print("Sources not plotted.")

# USAGE

# ddt_sim = SourceSimulator(3,4, [15] * 3, simulate_sources = True, plot = True)
# if(ddt_sim.simulate_sources):
#     ddt_sim.plot_simulation()



