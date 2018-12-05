import random
import math
import sys

INSTANCE_FILE = sys.argv[1]
SOLUTION_FILE = sys.argv[2] 

def get_instance(filename):
    file = open(filename, 'r')

    w = [] #vertex weights

    current_line = 1

    for line in file:
        instance = line.strip().split()

        if current_line == 1:
            n = int(instance[0]) #number os vertex
            e = int(instance[1]) #number os edges
            k = int(instance[2]) #number of colors
            E = [[0 for x in range(n)] for y in range(n)]

        if current_line == 2:
            for i in range(0, n):
                w.append(float(instance[i]))

        if (current_line > 2) and (current_line <= (e+2)):
            u = int(instance[0])
            v = int(instance[1])
            E[u][v] = 1
            
        current_line = current_line + 1
        
    file.close()

    return n, e, k, w, E

def print_instance(n, e, k, w, E):
    print("----------------------- ")
    print(" Instance:")
    print(" ")
    print(" n: {}, e: {}, k: {}".format(n,e,k)) 
    print(" ")

    for i in range(0, n):
        print(" vertex {} weight: {}".format(i,w[i]))

    print(" ")
    print(" {} edges:".format(e))
    for u in range(0,n):
        for v in range(0,n):
            if E[u][v] == 1:
                print(" [{}][{}]".format(u,v))
    print("----------------------- ")

def gen_rand_neighbor(self, current_state):
        ep = self.EPSILON
        neighbor = current_state.copy()

        for i in range(0, len(current_state) - 1):
            r = random.randint(0,2)
            if r == 0:
                neighbor[i] += ep
            if r == 1:
                neighbor[i] -= ep

        return neighbor

def simulated_annealing(self, weights):
    dec_temp = 0.93
    num_iter = 20
        
    current_value = self.run_episode(weights)
    current_state = weights.copy()

    print("Value: ", current_value)

    temperature = 100.0

    while True:
        temperature *= dec_temp
            
        print("Temperature: ", temperature)
        print("Value: ", current_value)
        if temperature < 0.15:
            return current_state
            
        for i in range(1,num_iter):
            candidate_state = self.genRandNeighbor(current_state)
            candidate_value = self.run_episode(candidate_state)

            delta = candidate_value - current_value

            if delta > 0:
                current_state = candidate_state.copy()
                current_value = candidate_value
            else:
                prob = math.exp(delta/temperature)
                r = random.random()
                if r < prob:
                    current_state = candidate_state.copy()
                    current_value = candidate_value



n, e, k, w, E = get_instance(INSTANCE_FILE)
print_instance(n, e, k, w, E)