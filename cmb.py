import random
import math
import sys
import time
import copy

SOLUTION_FILE = sys.argv[1] 
INSTANCE_FILE = sys.argv[2]
SEED = sys.argv[3]

def get_instance(filename):
    file = open(filename, 'r')

    weights = []

    current_line = 1

    for line in file:
        instance = line.strip().split()

        if current_line == 1:
            num_vertices = int(instance[0]) 
            num_edges = int(instance[1]) 
            num_colors = int(instance[2]) 
            edges = [[0 for x in range(num_vertices)] for y in range(num_vertices)]

        if current_line == 2:
            for i in range(0, num_vertices):
                weights.append(float(instance[i]))

        if (current_line > 2) and (current_line <= (num_edges+2)):
            u = int(instance[0])
            v = int(instance[1])
            edges[u][v] = 1
            
        current_line = current_line + 1
        
    file.close()

    return num_vertices, num_edges, num_colors, weights, edges

def print_instance(num_vertices, num_edges, num_colors, weights, edges):
    print("------- Instance ------- ")
    print(" ")
    print(" vertices: {} ".format(num_vertices)) 
    print(" edges: {} ".format(num_edges))
    print(" colors: {} ".format(num_colors))
    print(" ")

    for i in range(0, num_vertices):
        print(" vertex {} weight: {}".format(i,weights[i]))

    print(" ")
    print(" {} edges:".format(num_edges))
    for u in range(0,num_vertices):
        for v in range(0,num_vertices):
            if edges[u][v] == 1:
                print(" [{}][{}]".format(u,v))
    print(" ")

def is_feasible(solution, num_vertices, num_edges, num_colors, edges):

    return True

def initial_solution(num_vertices, num_edges, num_colors, edges):
    solution = [[0 for x in range(num_vertices)] for y in range(num_vertices)]

    for vertex in range(0,num_vertices):
        color = random.randint(0,num_colors-1)
        solution[vertex][color] = 1

    return solution

def print_initial_solution(solution, num_vertices, num_colors):
    print("--- Initial Solution --- ")
    print(" ")

    for vertex in range(0,num_vertices):
        for color in range(0,num_colors):
            if solution[vertex][color] == 1:
                print(" vertex {} color = {}".format(vertex,color))
    print(" ")


def gen_rand_neighbor(solution, num_vertices, num_edges, num_colors, weights, edges):
        neighbor = copy.deepcopy(solution) #ver copy.deepcopy()

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


random.seed(SEED)

num_vertices, num_edges, num_colors, weights, edges = get_instance(INSTANCE_FILE)
print_instance(num_vertices, num_edges, num_colors, weights, edges)
solution = initial_solution(num_vertices, num_edges, num_colors, edges)
print_initial_solution(solution, num_vertices, num_colors)