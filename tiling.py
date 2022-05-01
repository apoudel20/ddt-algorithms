import numpy as np
from ddt_simulator import SourceSimulator

sources = SourceSimulator()

sources.source_simulation()

def fitness(requirement: np.array, sources: np.array):
    combination = np.sum(sources, axis = 0)
    print(requirement, combination)
    print(requirement/combination)
    return sum(requirement / combination) - 1


# print(type(np.array([])))
# print(sources.bars[1])

sources.plot_simulation()

print(fitness(np.array([10,10,10]), np.array([[5,5,5]])))