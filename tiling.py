import numpy as np
from ddt_simulator import SourceSimulator

from itertools import chain, combinations
def all_subsets(ss):
    return chain(*map(lambda x: combinations(ss, x), range(1, len(ss)+1)))

sources = SourceSimulator()

sources.source_simulation()

def fitness(requirement: np.array, sources: np.array):
    combination = np.sum(sources, axis = 0)
    combination = combination / np.max(combination)
    requirement = requirement / np.max(requirement)
    # print(sum(requirement - combination))
    return sum(requirement - combination)


def get_best_fit(requirement: np.array, sources: np.array):
    # calls fitness on all possible combinations choose(n,<n)
    # minimize fitness

    min_fit = float('inf')
    best_fit_sources = None

    for subset in all_subsets(sources):
        nfit = fitness(requirement, subset)
        if(nfit < min_fit):
            best_fit_sources = subset
            min_fit = nfit

    return best_fit_sources

# print(type(np.array([])))
# print(sources.bars[1])

sources.plot_simulation()

print(get_best_fit(sources.group_count_requirements, sources.bars[1:]))

