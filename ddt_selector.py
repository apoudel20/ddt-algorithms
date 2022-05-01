import numpy as np

from ddt_simulator import SourceSimulator

# def greedy(sources: SourceSimulator):

#     itercount = 0

#     while(np.sum(sources.group_count_requirements) != 0):
#         itercount += 1
#         print("Iteration", itercount,":")
#         selec


# without using the tiling paper

##################################### GREEDY ALGORITHM ##########################################

def greedy(d,c,q,g):
    temp = []
    temp2 = []
    iteration = 0

    # while the count requirements have not been fulfilled
    while (sum(q)) != 0:

        iteration += 1
        print("\nAt iteration " + str(iteration) + ":")

        # select a source based on "fitness" of source
        # select = [source distribution, source index in D]
        select = greedyh(d,c,q,g)

        # add source index to temp
        temp += [select[1]]

        # initalize temp1 to hold the distribution of the source we just selected
        temp1 = []
        for k in range(len(select[0])):
            temp1 += [select[0][k]]
        
        temp2 += [temp1]

        # update count requirements
        for i in range(len(select[0])):
            if q[i] >= select[0][i]:
                q[i] = q[i] - select[0][i]
            else:
                q[i] = 0
        for j in range(len(select[0])):
            d[select[1]][j] = 0

        print(" > Updated Count Reqs: " + str(q))
        print()

    return (temp, temp2)


####################################### HELPERS ###############################################

# determines the best source based on cost & how much of the count requirement it fulfilles
def greedyh(d,c,q,g):
    temp = []
    for i in range(len(d)):
        sum1 = 0
        for j in range(len(g)):
            # sum up the maximum tuple we can get
            sum1 += min(q[j],d[i][j])
        
        if sum1 == 0:
            sum1 = 0.0001

        # cost of accessing source / number of tuples we can get from this source
        # essentially cost per tuple
        temp += [c[i]/sum1]

    ##print("here is normalized cost")
    ##print(temp)

    # after calculating fitness for each source, select the one with the lowest (means one with the lowest cost per tuple)
    select = MinIndex(temp)

    print(" > SOURCE " + str(select) + ": " + str(d[select]))
    print(" > Cost of source: " + str(c[select]))
    print(" > Cost per Tuple: " + str(temp[select]))
    
    # returns source distribution and source index in D
    return (d[select],select)


def MinIndex(arr):
    temp = 999
    tempIndex = 0
    for i in range(len(arr)):
        if temp > arr[i]:
            temp = arr[i]
            tempIndex = i
        
    return tempIndex 



source_simulator = SourceSimulator(simulate_sources = True)
# source_simulator.plot_simulation()
