import random
import math

def getInstance(filename):
    file = open(filename)


    return

def genRandNeighbor(self, current_state):
        ep = self.EPSILON
        neighbor = current_state.copy()

        for i in range(0, len(current_state) - 1):
            r = random.randint(0,2)
            if r == 0:
                neighbor[i] += ep
            if r == 1:
                neighbor[i] -= ep

        return neighbor

def simulatedAnnealing(self, weights):
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