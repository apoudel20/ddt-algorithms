import random
from ddt_simulator import SourceSimulator

def randomBase(d,c,count):
        leng = len(d)
        cost = 0
        selected = []
        q = copyArr(count)
        temp = []
        while (sum(q)) != 0:
            index = int(random.random()*leng)
            selected += [index]
            cost += c[index]
            temp += [d[index]]
            for i in range(len(d[index])):
                if q[i] >= d[index][i]:
                    q[i] = q[i] - d[index][i]
                else:
                    q[i] = 0
        return (selected, cost, temp)

def copyArr(arr1):
    arr2 = []
    for i in range(len(arr1)):
        arr2 += [arr1[i]]
    return arr2

def copyArr2(arr1):
    arr2 = []
    for i in range(len(arr1)):
        arr3 = []
        for j in range(len(arr1[i])):
            arr3 += [arr1[i][j]]
        arr2 += [arr3]
    return arr2


def greedyh(d,c,q,g):
    temp = []
    for i in range(len(d)):
        sum1 = 0
        for j in range(len(g)):
            sum1 += min(q[j],d[i][j])
        
        if sum1 == 0:
            sum1 = 0.0001
        temp += [c[i]/sum1]
    ##print("here is normalized cost")
    select = MinIndex(temp)
    
    return (d[select],select)

def greedy(dis,c,count,g):
    d = copyArr2(dis)
    temp = []
    temp2 = []
    cost = 0
    q = copyArr(count)
    while (sum(q)) != 0:
        select = greedyh(d,c,q,g)
        temp += [select[1]]
        cost += c[select[1]]
        temp1 = []
        for k in range(len(select[0])):
            temp1 += [select[0][k]]
        temp2 += [temp1]
        for i in range(len(select[0])):
            if q[i] >= select[0][i]:
                q[i] = q[i] - select[0][i]
            else:
                q[i] = 0
        for j in range(len(select[0])):
            d[select[1]][j] = 0

    return (temp,cost,temp2)
        
                

def MinIndex(arr):
    temp = 999
    tempIndex = 0
    for i in range(len(arr)):
        if temp > arr[i]:
            temp = arr[i]
            tempIndex = i
        
    return tempIndex 

# USAGE
SourceDis = [0.9,0.5,0.5]
ddt_sim = SourceSimulator(3,400,None,[15] * 3, simulate_sources = True, plot = True)
# if(ddt_sim.simulate_sources):
#     ddt_sim.plot_simulation()
tempSum = 0
for i in range(100):
    tempSum += randomBase(ddt_sim.bars[1:],ddt_sim.access_costs,ddt_sim.bars[0])[1]      
print("Cost: ")
print(tempSum/100)

group = [0,1,2]

tempSum2 = 0
for i in range(100):
    tempSum2 += greedy(ddt_sim.bars[1:],ddt_sim.access_costs,ddt_sim.bars[0],group)[1]      
print("Cost: ")
print(tempSum2/100)
