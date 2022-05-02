import numpy as np
import cvxpy as cp

from ddt_simulator import SourceSimulator

from itertools import chain, combinations
def all_subsets(ss):
    return chain(*map(lambda x: combinations(ss, x), range(1, len(ss)+1)))

sources = SourceSimulator(3,10)

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

    return np.array(best_fit_sources)

# print(type(np.array([])))
# print(sources.bars[1])

# sources.plot_simulation()

unit_selected_sources = get_best_fit(sources.group_count_requirements, sources.bars[1:])

source_id = list()
for x in unit_selected_sources:
    for i,y in enumerate(sources.bars[1:]):
        print(x,y)
        if((x==y).all()):
            source_id.append(i)
print(source_id, ":", unit_selected_sources)

def linear_combination(sources: np.array, requirements: np.array, access_costs):
    # input_matrix = sources.T # column-first
    # x = cp.Variable(m_sources) # sources as variables. group composition invariant
    # b = np.random.randn(n_groups)
    # cost = cp.sum_squares(input_matrix @ x - b)
    # print("logged")
    # solver = cp.Problem(cp.Minimize(cost), [x >=0, cp.sum(x) == 1])
    # solver.solve()


    target = requirements

    # Define and solve the CVXPY problem.
    x = cp.Variable(sources.shape[0])
    cost = cp.sum_squares(sources.T @ (x @ access_costs) - target)
    prob = cp.Problem(cp.Minimize(cost), [x>=0, cp.sum(x)==1])
    prob.solve()

    return x.value

print(linear_combination(sources.source_group_dist, sources.group_count_requirements, sources.access_costs))
