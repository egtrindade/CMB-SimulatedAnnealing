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

def write_output(out_filename,instance_filename, num_vertices, num_edges, r, I, initial_prob, final_prob, time, seed, initial_value, best_value, solution):
    out_file = open(out_filename, "w")

    out_file.write("Instance File:\n  " + instance_filename + "\n")
    out_file.write("\nTime:\n  " + str(time_elapsed) + "\n")
    out_file.write("\nParameters:\n")
    out_file.write("  Cooling Factor r: " + str(r) + "\n")
    out_file.write("  Instances I: " + str(I) + "\n")
    out_file.write("  Initial probability: " + str(initial_prob) + "\n")
    out_file.write("  Final probability: " + str(final_prob) + "\n")
    out_file.write("  Seed: " + str(seed) + "\n")
    out_file.write("\nInitial Solution Value:\n  " + str(initial_value) + "\n")
    out_file.write("\nFinal Solution Value:\n  " + str(best_value) + "\n")
    out_file.write("\nSolution:\n")
    for vertex in range(0,num_vertices):
        color = get_vertex_color(vertex,solution,num_vertices,num_edges)
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

def get_vertex_color(vertex, solution, num_vertices, num_colors):
    found = 0
    color = 0
 
    while found == 0:
        if solution[vertex][color] == 1:
            found = 1
        else:   
            color = color + 1

    return color

def count_color_conflicts(solution, num_vertices, num_edges, num_colors, edges):
    color_conflicts = 0

    for u in range(0,num_vertices):
        for v in range(0,num_vertices):
            if edges[u][v] == 1:
                u_color = get_vertex_color(u,solution,num_vertices,num_edges)
                v_color = get_vertex_color(v,solution,num_vertices,num_edges)
                if u_color == v_color:
                    color_conflicts = color_conflicts + 1

    return color_conflicts

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
        color = get_vertex_color(vertex,solution,num_vertices,num_colors)
        print(" vertex {} color = {}".format(vertex,color))

    print(" ")

def get_solution_value(solution, num_vertices, num_edges, num_colors, weights):
    values = [0.0, 0.0, 0.0]

    for color in range(0,num_colors):
        for vertex in range(0,num_vertices):
            if solution[vertex][color] == 1:
                values[color] = values[color] + weights[vertex]

    return max(values), values

def print_color_values(color_values, num_colors):
    print("----- Color Values ----- ")
    print(" ")

    print(" Max color value:")
    print(" " + str(max(color_values)) + "\n ")

    for color in range(0,num_colors):
        print(" Value of color {} = {}".format(color,color_values[color]))
    print(" ")
        
def get_rand_neighbor(solution, num_vertices, num_colors):
    neighbor = copy.deepcopy(solution)

    vertex = random.randint(0,num_vertices-1)
    color = get_vertex_color(vertex,neighbor,num_vertices,num_edges)
    
    new_color = random.randint(0,num_colors-1)

    while new_color == color:
        new_color = random.randint(0,num_colors-1)      
    
    neighbor[vertex][color] = 0
    neighbor[vertex][new_color] = 1

    return neighbor

def initial_temperature(solution, temperature, r, I, initial_prob, num_vertices, num_edges, num_colors, weights):
    current_value = get_solution_value(solution,num_vertices, num_edges, num_colors, weights)
    aprox_temp = temperature
    aprox_prob = 1

    while(temperature > 0.0001):
        accepted_moves = 0
        moves_tried = 0
        for i in range(0,I):
            neighbor = get_rand_neighbor(solution,num_vertices,num_colors)
            candidate_value = get_solution_value(neighbor,num_vertices, num_edges, num_colors, weights)
            
            delta =  candidate_value - current_value 

            if delta <= 0:
                solution = neighbor
                current_value = candidate_value
            else:
                moves_tried = moves_tried + 1
                prob = math.exp((-delta)/temperature)
                rand = random.random()
                if rand < prob:
                    accepted_moves = accepted_moves + 1
                    solution = neighbor
                    current_value = candidate_value
        if moves_tried > 0:
            if ((initial_prob - 0.005) <= (accepted_moves/moves_tried)) and ((accepted_moves/moves_tried) <= (initial_prob + 0.005)): #approximately equal to the initial probability
                return temperature
            else:
                if abs((accepted_moves/moves_tried) - initial_prob) < abs(aprox_prob - initial_prob):
                    aprox_temp = temperature
                    aprox_prob = (accepted_moves/moves_tried)
        temperature = temperature * r	

    return aprox_temp

def simulated_annealing(solution, temperature, r, I, final_prob, num_vertices, num_edges, num_colors, weights):
    current_value = get_solution_value(solution,num_vertices, num_edges, num_colors, weights)
    counter = 0
    
    while(counter < 5):
        accepted_moves = 0
        moves_tried = 0
        for i in range(0,I):
            neighbor = get_rand_neighbor(solution,num_vertices,num_colors)
            candidate_value = get_solution_value(neighbor,num_vertices, num_edges, num_colors, weights)
            
            delta =  candidate_value - current_value 

            if delta <= 0:
                solution = neighbor
                current_value = candidate_value
            else:
                moves_tried = moves_tried + 1
                prob = math.exp((-delta)/temperature)
                rand = random.random()
                if rand < prob:
                    accepted_moves = accepted_moves + 1
                    solution = neighbor
                    current_value = candidate_value
        if moves_tried > 0:
            if final_prob > (accepted_moves/moves_tried):
                counter = counter + 1
        temperature = temperature * r	

    return solution
        
def cmb(num_vertices, num_edges, num_colors, weights, edges, r, I, initial_prob, final_prob):
    best_value = 0

    start = time()

    solution = initial_solution(num_vertices, num_edges, num_colors)
    print_solution(solution, num_vertices, num_colors)

    initial_value, color_values = get_solution_value(solution,num_vertices, num_edges, num_colors, weights)
    print_color_values(color_values, num_colors)
    num_conflicts = count_color_conflicts(solution,num_vertices,num_edges,num_colors,edges)
    print(" Conflicts = {}".format(num_conflicts))

    print("************ Neighbor ************\n")
    neighbor = get_rand_neighbor(solution,num_vertices,num_colors)

    neighbor_value, neighbor_color_values = get_solution_value(neighbor,num_vertices, num_edges, num_colors, weights)
    print_solution(neighbor, num_vertices, num_colors)
    print_color_values(neighbor_color_values, num_colors)
    num_conflicts = count_color_conflicts(solution,num_vertices,num_edges,num_colors,edges)
    print(" Conflicts = {}".format(num_conflicts))

    end = time()
    time_elapsed = end - start

    best_value = neighbor_value

    return solution, initial_value, best_value, time_elapsed


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
solution, initial_value, best_value, time_elapsed = cmb(num_vertices, num_edges, num_colors, weights, edges, r, I, pi, pf)
write_output(out_file,instance,num_vertices,num_edges,r,I,pi,pf,time_elapsed,seed,initial_value,best_value,solution)