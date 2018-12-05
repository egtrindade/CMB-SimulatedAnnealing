import random
import math
import sys
from time import time
import copy

OUTPUT_FILE = sys.argv[1] 
INSTANCE_FILE = sys.argv[2]
COOLING_FACTOR = sys.argv[3]
ITERATIONS = sys.argv[4]
INITIAL_PROB = sys.argv[5]
FINAL_PROB = sys.argv[6]
SEED = sys.argv[7]

def write_output(out_filename,instance_filename, num_vertices, num_edges, r, I, initial_prob, final_prob, time, seed, best_value, solution):
    out_file = open(out_filename, "w")

    out_file.write("Instance File:\n  " + instance_filename + "\n")
    out_file.write("\nTime:\n  " + str(time_elapsed) + "\n")
    out_file.write("\nParameters:\n")
    out_file.write("  Cooling Factor r: " + str(r) + "\n")
    out_file.write("  Instances I: " + str(I) + "\n")
    out_file.write("  Initial probability: " + str(initial_prob) + "\n")
    out_file.write("  Final probability: " + str(final_prob) + "\n")
    out_file.write("  Seed: " + str(seed) + "\n")
    out_file.write("\nValue:\n  " + str(best_value) + "\n")
    out_file.write("\nSolution:\n")
    for vertex in range(0,num_vertices):
        for color in range(0,num_colors):
            if solution[vertex][color] == 1:
                out_file.write("  Vertex {} color = {}\n".format(vertex,color))
    out_file.close()

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

def initial_solution(num_vertices, num_edges, num_colors):
    solution = [[0 for x in range(num_vertices)] for y in range(num_vertices)]

    for vertex in range(0,num_vertices):
        color = random.randint(0,num_colors-1)
        solution[vertex][color] = 1

    return solution

def print_solution(solution, num_vertices, num_colors):
    print("------- Solution ------- ")
    print(" ")

    for vertex in range(0,num_vertices):
        for color in range(0,num_colors):
            if solution[vertex][color] == 1:
                print(" vertex {} color = {}".format(vertex,color))
    print(" ")

def get_solution_value(solution, num_vertices, num_edges, num_colors, weights):
    values = [0.0, 0.0, 0.0]

    for color in range(0,num_colors):
        for vertex in range(0,num_vertices):
            if solution[vertex][color] == 1:
                values[color]= values[color] + weights[vertex]

    return max(values), values

def print_color_values(color_values, num_colors):
    print("----- Color Values ----- ")
    print(" ")

    print(" Max color value:")
    print(" " + str(max(color_values)) + "\n ")

    for color in range(0,num_colors):
        print(" Value of color {} = {}".format(color,color_values[color]))
    print(" ")
        
def gen_rand_neighbor(solution, num_vertices, num_colors):
        neighbor = copy.deepcopy(solution)
        found = 0
        color = 0

        vertex = random.randint(0,num_vertices-1)
        new_color = random.randint(0,num_colors-1)
        
        while found == 0:
            if neighbor[vertex][color] == 1:
                found = 1
                while new_color == color:
                    new_color = random.randint(0,num_colors-1)      
                neighbor[vertex][color] = 0
                neighbor[vertex][new_color] = 1
            
            color = color + 1

        return neighbor

def initial_temperature(solution, temperature, r, I, initial_prob, num_vertices, num_edges, num_colors, weights, edges):
    initial_temp = temperature

    return initial_temp

def simulated_annealing(num_vertices, num_edges, num_colors, weights, edges):
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

def cmb(num_vertices, num_edges, num_colors, weights, edges, r, I, initial_prob, final_prob):
    best_value = 0

    start = time()

    solution = initial_solution(num_vertices, num_edges, num_colors)
    print_solution(solution, num_vertices, num_colors)

    solution_value, color_values = get_solution_value(solution,num_vertices, num_edges, num_colors, weights)
    print_color_values(color_values, num_colors)

    neighbor = gen_rand_neighbor(solution,num_vertices,num_colors)
    neighbor_value, neighbor_color_values = get_solution_value(neighbor,num_vertices, num_edges, num_colors, weights)
    print_color_values(neighbor_color_values, num_colors)
    print_solution(neighbor, num_vertices, num_colors)

    end = time()
    time_elapsed = end - start

    return solution, best_value, time_elapsed

seed = SEED
out_file = OUTPUT_FILE
instance = INSTANCE_FILE
r = COOLING_FACTOR
I = ITERATIONS
pi = INITIAL_PROB
pf = FINAL_PROB

random.seed(seed)
num_vertices, num_edges, num_colors, weights, edges = get_instance(instance)
print_instance(num_vertices, num_edges, num_colors, weights, edges)
solution, best_value, time_elapsed = cmb(num_vertices, num_edges, num_colors, weights, edges, r, I, pi, pf)
write_output(out_file,instance,num_vertices,num_edges,r,I,pi,pf,time_elapsed,seed,best_value,solution)