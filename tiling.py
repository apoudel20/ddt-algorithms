import math
from random import random, choice
from select import select
import numpy as np
import cvxpy as cp # optimization problem solver package

from ddt_simulator import SourceSimulator

from itertools import chain, combinations

def random_select(sources):
    
    count_requirement_fulfilled = np.array([0,0,0])
    original_count = sources.group_count_requirements
    while(np.max(sources.group_count_requirements) > 0):
        random_source = choice(list(range(sources.m_sources))) # randomly pick a source
        # query it to receive a tuple and update count
        if(len(sources.sources[random_source]) == 0):
            continue
        selected_tuple = sources.sources[random_source].pop() # single query on the random source
        count_requirement_fulfilled = count_requirement_fulfilled + np.array(selected_tuple)
        sources.group_count_requirements -= np.array(selected_tuple)
    print(sources.group_count_requirements, count_requirement_fulfilled)
    return 1 + np.sum(sources.group_count_requirements)/np.sum(count_requirement_fulfilled)

        


def all_subsets(ss):
    return chain(*map(lambda x: combinations(ss, x), range(1, len(ss)+1)))


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



def linear_combination(sources: np.array, requirements: np.array, access_costs, tuple_count_per_source):
    # input_matrix = sources.T # column-first
    # x = cp.Variable(m_sources) # sources as variables. group composition invariant
    # b = np.random.randn(n_groups)
    # cost = cp.sum_squares(input_matrix @ x - b)
    # print("logged")
    # solver = cp.Problem(cp.Minimize(cost), [x >=0, cp.sum(x) == 1])
    # solver.solve()


    target = requirements

    # Define and solve the CVXPY problem.
    x = cp.Variable(sources.shape[0]) # x is k
    cost = cp.sum_squares(sources.T @ x - target) # integrate cost. right now, this function only does equicost. mean squared error. multiply tuple (x) by cost
    prob = cp.Problem(cp.Minimize(cost + sum(x @ access_costs)), [x>=0, x <= tuple_count_per_source])
    prob.solve()

    return x.value, cp.norm(sources.T @ x - target).value

# will probably need to keep track of is size of sources. her algorithm has the N_i in the denominator

sources = SourceSimulator(3, 10, group_count_requirements = [40] * 3)
# mask = np.array([1,1,1])
# mask = np.array([.9,.9,1])
# mask = np.array([.8,.9,1])
# mask = np.array([.5,.8,1])
# mask = np.array([.5,.5,1])
mask = np.array([.1,.3,1])
sources.source_group_dist *= mask
sources.source_simulation()

unit_selected_sources = get_best_fit(sources.group_count_requirements, sources.bars[1:])

source_id = list()
for x in unit_selected_sources:
    for i,y in enumerate(sources.bars[1:]):
        # print(x,y)
        if((x==y).all()):
            source_id.append(i)
print(source_id, ":", unit_selected_sources)

results = linear_combination(sources.source_group_dist, sources.group_count_requirements, sources.access_costs, sources.tuple_count_per_source)
# print(np.sum(unit_selected_sources))
print("k per source:", [round(x) for x in results[0]])
print("Cost:", results[1])

random_results = random_select(sources)
print("Cost:", random_results)

# sources.plot_simulation()