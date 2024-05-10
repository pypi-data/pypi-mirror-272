def hebb():
    code="""
import random

# Initialize weights
weight1 = random.uniform(-1, 1)
weight2 = random.uniform(-1, 1)

# Learning rate
learning_rate = 0.1

# Inputs and target output
inputs = [[0, 0], [0, 1], [1, 0], [1, 1]]
target_outputs = [0, 1, 1, 1]  # XOR gate

# Training loop
for epoch in range(10000):
    for i in range(len(inputs)):
        input1, input2 = inputs[i]
        target_output = target_outputs[i]

        # Calculate the output of the neuron
        output = input1 * weight1 + input2 * weight2

        # Calculate the error
        error = target_output - output

        # Update weights according to the Hebb rule
        weight1 += learning_rate * error * input1
        weight2 += learning_rate * error * input2

        # Print the weights after every 1000 epochs
        if epoch % 1000 == 0:
            print(f"Epoch {epoch}: Weight1 = {weight1:.2f}, Weight2 = {weight2:.2f}")

# Print the final weights
print(f"\nFinal weights: Weight1 = {weight1:.2f}, Weight2 = {weight2:.2f}")

"""
    return code

def mcpitt():
    code="""
import numpy as np

# Define the activation function
def step_function(x):
    return 1 if x >= 0 else 0

# Define the McCulloch-Pitts neuron
class McCullochPittsNeuron:
    def __init__(self, weights, bias):
        self.weights = np.array(weights)
        self.bias = bias

    def forward(self, inputs):
        weighted_sum = np.dot(inputs, self.weights) + self.bias
        return step_function(weighted_sum)

# Example usage
# Define the inputs and desired output for the AND gate
inputs = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
desired_output = [0, 0, 0, 1]

# Initialize the weights and bias
weights = [0.5, 0.5]
bias = -0.7

# Create the McCulloch-Pitts neuron
neuron = McCullochPittsNeuron(weights, bias)

# Test the neuron on the inputs
for input_vector, expected_output in zip(inputs, desired_output):
    output = neuron.forward(input_vector)
    print(f"Input: {input_vector}, Expected Output: {expected_output}, Actual Output: {output}")
"""
    return code

def kohonen():
    code="""
import numpy as np

class KohonenSOM:
    def __init__(self, m, n, dim, n_iterations=100, alpha=None):
        self.m = m
        self.n = n
        self.dim = dim
        self.n_iterations = n_iterations
        if alpha is None:
            self.alpha = 0.3
        else:
            self.alpha = alpha

        # Initialize the SOM grid with random values
        self.weight_vectors = np.random.rand(m * n, dim)

    def get_bmu(self, input_vector):
        distances = np.linalg.norm(self.weight_vectors - input_vector, axis=1)
        return np.argmin(distances)

    def get_location(self, bmu_idx):
        row = bmu_idx // self.n
        col = bmu_idx % self.n
        return row, col

    def train(self, data):
        for iteration in range(self.n_iterations):
            self.alpha = 0.3 * (self.n_iterations - iteration) / self.n_iterations
            for input_vector in data:
                bmu_idx = self.get_bmu(input_vector)
                bmu_row, bmu_col = self.get_location(bmu_idx)

                for i in range(self.m):
                    for j in range(self.n):
                        distance = np.sqrt((i - bmu_row) ** 2 + (j - bmu_col) ** 2)
                        influence = np.exp(-distance)
                        self.weight_vectors[i * self.n + j] += self.alpha * influence * (input_vector - self.weight_vectors[i * self.n + j])

# Example usage
if __name__ == "__main__":
    # Generate some random data
    data = np.random.rand(1000, 3)

    # Create a Kohonen SOM with a 5x5 grid
    som = KohonenSOM(5, 5, 3)

    # Train the SOM on the data
    som.train(data)

    # Test the SOM on a random input vector
    test_vector = np.random.rand(3)
    bmu_idx = som.get_bmu(test_vector)
    bmu_row, bmu_col = som.get_location(bmu_idx)
    print(f"Best Matching Unit for {test_vector}: ({bmu_row}, {bmu_col})")
"""
    return code
def linearly_seperable():
    code="""
import numpy as np

class Perceptron:
    def __init__(self, learning_rate=0.1, max_iterations=1000):
        self.learning_rate = learning_rate
        self.max_iterations = max_iterations
        self.weights = None
        self.bias = None

    def fit(self, X, y):
        n_samples, n_features = X.shape
        self.weights = np.zeros(n_features)
        self.bias = 0

        for _ in range(self.max_iterations):
            misclassified = False
            for i in range(n_samples):
                x_i = X[i]
                y_i = y[i]
                activation = np.dot(x_i, self.weights) + self.bias

                if y_i * activation <= 0:
                    misclassified = True
                    self.weights += self.learning_rate * y_i * x_i
                    self.bias += self.learning_rate * y_i

            if not misclassified:
                break

    def predict(self, X):
        activations = np.dot(X, self.weights) + self.bias
        return np.sign(activations)

# Example usage: Solving the AND gate problem
X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
y = np.array([-1, -1, -1, 1])

perceptron = Perceptron(learning_rate=0.1, max_iterations=1000)
perceptron.fit(X, y)

print("Weights:", perceptron.weights)
print("Bias:", perceptron.bias)

predictions = perceptron.predict(X)
print("Predictions:", predictions)
"""
    return code
def operation_on_fuzzy():
    code="""
from typing import Dict

def union(fuzzy_set_1: Dict[float, float], fuzzy_set_2: Dict[float, float]) -> Dict[float, float]:

    result = {}
    for x in set(fuzzy_set_1) | set(fuzzy_set_2):
        result[x] = max(fuzzy_set_1.get(x, 0), fuzzy_set_2.get(x, 0))
    return result

def intersection(fuzzy_set_1: Dict[float, float], fuzzy_set_2: Dict[float, float]) -> Dict[float, float]:

    result = {}
    for x in set(fuzzy_set_1) & set(fuzzy_set_2):
        result[x] = min(fuzzy_set_1[x], fuzzy_set_2[x])
    return result

def complement(fuzzy_set: Dict[float, float]) -> Dict[float, float]:

    result = {}
    for x in fuzzy_set:
        result[x] = 1 - fuzzy_set[x]
    return result

def difference(fuzzy_set_1: Dict[float, float], fuzzy_set_2: Dict[float, float]) -> Dict[float, float]:
 
    result = {}
    for x in set(fuzzy_set_1) | set(fuzzy_set_2):
        result[x] = max(fuzzy_set_1.get(x, 0) - fuzzy_set_2.get(x, 0), 0)
    return result

def cartesian_product(fuzzy_set_1: Dict[float, float], fuzzy_set_2: Dict[float, float]) -> Dict[tuple, float]:

    result = {}
    for x in fuzzy_set_1:
        for y in fuzzy_set_2:
            result[(x, y)] = min(fuzzy_set_1[x], fuzzy_set_2[y])
    return result

def max_min_composition(fuzzy_relation_1: Dict[tuple, float], fuzzy_relation_2: Dict[tuple, float]) -> Dict[tuple, float]:

    result = {}
    for (x, y) in fuzzy_relation_1:
        for (z, w) in fuzzy_relation_2:
            if y == z:
                result[(x, w)] = max(result.get((x, w), 0), min(fuzzy_relation_1[(x, y)], fuzzy_relation_2[(z, w)]))
    return result

if __name__ == "__main__":
    # Example fuzzy sets
    fuzzy_set_1 = {1: 0.2, 2: 0.5, 3: 0.8}
    fuzzy_set_2 = {1: 0.6, 2: 0.3, 4: 0.9}

    # Union
    print("Union:", union(fuzzy_set_1, fuzzy_set_2))

    # Intersection
    print("Intersection:", intersection(fuzzy_set_1, fuzzy_set_2))

    # Complement
    print("Complement of fuzzy_set_1:", complement(fuzzy_set_1))

    # Difference
    print("Difference (fuzzy_set_1 - fuzzy_set_2):", difference(fuzzy_set_1, fuzzy_set_2))

    # Cartesian product
    fuzzy_relation = cartesian_product(fuzzy_set_1, fuzzy_set_2)
    print("Fuzzy relation:", fuzzy_relation)

    # Max-min composition
    fuzzy_relation_2 = {(1, 3): 0.4, (2, 3): 0.6, (3, 4): 0.7}
    print("Max-min composition:", max_min_composition(fuzzy_relation, fuzzy_relation_2))
"""
    return code
def fuzzy_relation():
    code="""
from typing import Dict

def max_min_composition(fuzzy_relation_1: Dict[tuple, float], fuzzy_relation_2: Dict[tuple, float]) -> Dict[tuple, float]:

    result = {}
    for (x, y) in fuzzy_relation_1:
        for (z, w) in fuzzy_relation_2:
            if y == z:
                result[(x, w)] = max(result.get((x, w), 0), min(fuzzy_relation_1[(x, y)], fuzzy_relation_2[(z, w)]))
    return result

if __name__ == "__main__":
    # Example fuzzy relations
    fuzzy_relation_1 = {(1, 2): 0.6, (2, 3): 0.8, (3, 4): 0.7}
    fuzzy_relation_2 = {(2, 5): 0.4, (3, 6): 0.9, (4, 5): 0.5}

    # Max-min composition
    composed_relation = max_min_composition(fuzzy_relation_1, fuzzy_relation_2)
    print("Composed Fuzzy Relation:")
    for pair, membership in composed_relation.items():
        print(f"{pair}: {membership}")
"""
    return code
def tsp():
    code="""
import random
import math
import matplotlib.pyplot as plt

class City:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self, city):
        return math.sqrt((self.x - city.x)**2 + (self.y - city.y)**2)

class Fitness:
    def __init__(self, route):
        self.route = route
        self.distance = 0
        self.fitness = 0.0

    def route_distance(self):
        if self.distance == 0:
            path_distance = 0
            for i in range(len(self.route)):
                from_city = self.route[i]
                to_city = None
                if i + 1 < len(self.route):
                    to_city = self.route[i + 1]
                else:
                    to_city = self.route[0]
                path_distance += from_city.distance(to_city)
            self.distance = path_distance
        return self.distance

    def route_fitness(self):
        if self.fitness == 0:
            self.fitness = 1 / float(self.route_distance())
        return self.fitness

def create_route(city_list):
    route = random.sample(city_list, len(city_list))
    return route

def initial_population(city_list, population_size):
    population = []
    for i in range(population_size):
        population.append(create_route(city_list))
    return population

def rank_routes(population):
    fitness_results = []
    for route in population:
        fitness_results.append(Fitness(route))
    fitness_results.sort(key=lambda x: x.route_fitness(), reverse=True)
    return fitness_results

def breed_population(population, elite_size):
    selected_routes = []
    elite_routes = population[:elite_size]
    selected_routes.extend(elite_routes)

    while len(selected_routes) < len(population):
        parent1 = random.choice(population)
        parent2 = random.choice(population)
        child = breed(parent1, parent2)
        selected_routes.append(child)

    return selected_routes

def breed(parent1, parent2):
    child = []
    start_pos = random.randint(0, len(parent1))
    end_pos = random.randint(0, len(parent1))

    if start_pos < end_pos:
        for i in range(start_pos, end_pos):
            child.append(parent1[i])
    else:
        for i in range(start_pos, len(parent1)):
            child.append(parent1[i])
        for i in range(0, end_pos):
            child.append(parent1[i])

    for city in parent2:
        if city not in child:
            child.append(city)

    return child

def mutate_population(population, mutation_rate):
    mutated_population = []
    for route in population:
        mutated_route = mutate(route, mutation_rate)
        mutated_population.append(mutated_route)
    return mutated_population

def mutate(route, mutation_rate):
    for swapped in range(len(route)):
        if random.random() < mutation_rate:
            swap_with = int(random.random() * len(route))

            city1 = route[swapped]
            city2 = route[swap_with]

            route[swapped] = city2
            route[swap_with] = city1
    return route

def genetic_algorithm(city_list, population_size, elite_size, mutation_rate, generations):
    population = initial_population(city_list, population_size)
    print("Initial distance: " + str(1 / rank_routes(population)[0].route_fitness()))

    best_distances = []
    for i in range(generations):
        population = breed_population(population, elite_size)
        population = mutate_population(population, mutation_rate)
        best_distances.append(1 / rank_routes(population)[0].route_fitness())

    print("Final distance: " + str(1 / rank_routes(population)[0].route_fitness()))
    best_route = rank_routes(population)[0].route

    # Plot the convergence curve
    plt.plot(range(generations), best_distances)
    plt.xlabel('Generation')
    plt.ylabel('Best Distance')
    plt.title('Convergence Curve')
    plt.show()

    return best_route

# Example usage
city_list = []
city_list.append(City(60, 200))
city_list.append(City(180, 200))
city_list.append(City(80, 180))
city_list.append(City(140, 180))
city_list.append(City(20, 160))
city_list.append(City(100, 160))
city_list.append(City(200, 160))
city_list.append(City(140, 140))
city_list.append(City(40, 120))
city_list.append(City(100, 120))
city_list.append(City(180, 100))
city_list.append(City(60, 80))
city_list.append(City(120, 80))
city_list.append(City(180, 60))
city_list.append(City(20, 40))
city_list.append(City(100, 40))
city_list.append(City(200, 40))
city_list.append(City(20, 20))
city_list.append(City(60, 20))
city_list.append(City(160, 20))

best_route = genetic_algorithm(city_list, population_size=100, elite_size=20, mutation_rate=0.01, generations=500)
print("Best route: ", best_route)
"""
    return code
def shortestpath():
    code="""
import random
import math

class City:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self, city):
        return math.sqrt((self.x - city.x)**2 + (self.y - city.y)**2)

    def __repr__(self):
        return f"({self.x}, {self.y})"

class Fitness:
    def __init__(self, route):
        self.route = route
        self.distance = self.route_distance()
        self.fitness = 1 / self.distance

    def route_distance(self):
        path_distance = 0
        for i in range(len(self.route)):
            from_city = self.route[i]
            to_city = None
            if i + 1 < len(self.route):
                to_city = self.route[i + 1]
            else:
                to_city = self.route[0]
            path_distance += from_city.distance(to_city)
        return path_distance

def create_route(city_list):
    route = random.sample(city_list, len(city_list))
    return route

def initial_population(city_list, population_size):
    population = []
    for _ in range(population_size):
        population.append(create_route(city_list))
    return population

def rank_routes(population):
    fitness_results = [Fitness(route) for route in population]
    fitness_results.sort(key=lambda x: x.fitness, reverse=True)
    return fitness_results

def breed_population(population):
    selected_routes = []
    fitnesses = rank_routes(population)
    elite_size = int(len(fitnesses) * 0.2)  # Top 20% routes
    elite_routes = [fitness.route for fitness in fitnesses[:elite_size]]
    selected_routes.extend(elite_routes)

    while len(selected_routes) < len(population):
        parent1 = random.choice(fitnesses).route
        parent2 = random.choice(fitnesses).route
        child = breed(parent1, parent2)
        selected_routes.append(child)

    return selected_routes

def breed(parent1, parent2):
    child = []
    start_pos = random.randint(0, len(parent1))
    end_pos = random.randint(0, len(parent1))

    if start_pos < end_pos:
        child = parent1[start_pos:end_pos]
    else:
        child = parent1[start_pos:] + parent1[:end_pos]

    for city in parent2:
        if city not in child:
            child.append(city)

    return child

def mutate_population(population, mutation_rate):
    mutated_population = []
    for route in population:
        mutated_route = mutate(route, mutation_rate)
        mutated_population.append(mutated_route)
    return mutated_population

def mutate(route, mutation_rate):
    for swapped in range(len(route)):
        if random.random() < mutation_rate:
            swap_with = int(random.random() * len(route))

            city1 = route[swapped]
            city2 = route[swap_with]

            route[swapped] = city2
            route[swap_with] = city1
    return route

def genetic_algorithm(city_list, population_size, elite_size, mutation_rate, generations):
    population = initial_population(city_list, population_size)
    print("Initial distance: " + str(1 / rank_routes(population)[0].fitness))

    for i in range(generations):
        population = breed_population(population)
        population = mutate_population(population, mutation_rate)

    print("Final distance: " + str(1 / rank_routes(population)[0].fitness))
    best_route = rank_routes(population)[0].route
    return best_route

# Example usage
city_list = [City(60, 200), City(180, 200), City(80, 180), City(140, 180), City(20, 160),
             City(100, 160), City(200, 160), City(140, 140), City(40, 120), City(100, 120),
             City(180, 100), City(60, 80), City(120, 80), City(180, 60), City(20, 40),
             City(100, 40), City(200, 40), City(20, 20), City(60, 20), City(160, 20)]

shortest_path = genetic_algorithm(city_list, population_size=100, elite_size=20, mutation_rate=0.01, generations=500)
print("Shortest path: ", shortest_path)
"""
    return code
def washingmachine():
    code="""
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Define input variables
dirt = ctrl.Antecedent(np.arange(0, 11, 1), 'dirt')
load = ctrl.Antecedent(np.arange(0, 11, 1), 'load')

# Define output variable
cycle_time = ctrl.Consequent(np.arange(20, 61, 1), 'cycle_time')

# Define membership functions for input variables
dirt['low'] = fuzz.trimf(dirt.universe, [0, 0, 5])
dirt['medium'] = fuzz.trimf(dirt.universe, [0, 5, 10])
dirt['high'] = fuzz.trimf(dirt.universe, [5, 10, 10])

load['small'] = fuzz.trimf(load.universe, [0, 0, 5])
load['medium'] = fuzz.trimf(load.universe, [0, 5, 10])
load['large'] = fuzz.trimf(load.universe, [5, 10, 10])

# Define membership functions for output variable
cycle_time['short'] = fuzz.trimf(cycle_time.universe, [20, 20, 35])
cycle_time['medium'] = fuzz.trimf(cycle_time.universe, [20, 40, 60])
cycle_time['long'] = fuzz.trimf(cycle_time.universe, [35, 60, 60])

# Define fuzzy rules
rule1 = ctrl.Rule(dirt['low'] & load['small'], cycle_time['short'])
rule2 = ctrl.Rule(dirt['low'] & load['medium'], cycle_time['medium'])
rule3 = ctrl.Rule(dirt['low'] & load['large'], cycle_time['medium'])
rule4 = ctrl.Rule(dirt['medium'] & load['small'], cycle_time['medium'])
rule5 = ctrl.Rule(dirt['medium'] & load['medium'], cycle_time['medium'])
rule6 = ctrl.Rule(dirt['medium'] & load['large'], cycle_time['long'])
rule7 = ctrl.Rule(dirt['high'] & load['small'], cycle_time['medium'])
rule8 = ctrl.Rule(dirt['high'] & load['medium'], cycle_time['long'])
rule9 = ctrl.Rule(dirt['high'] & load['large'], cycle_time['long'])

# Create a fuzzy control system
washing_machine = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9])

# Create a simulation environment
washing_machine_simulation = ctrl.ControlSystemSimulation(washing_machine)

# Test the fuzzy system
dirt_level = 8
load_size = 6

washing_machine_simulation.input['dirt'] = dirt_level
washing_machine_simulation.input['load'] = load_size

washing_machine_simulation.compute()
cycle_time_output = washing_machine_simulation.output['cycle_time']

print(f"For dirt level {dirt_level} and load size {load_size}, the recommended cycle time is {cycle_time_output:.2f} minutes.")
"""
    return code
def neuro_fuzzy():
    code="""
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from keras.models import Sequential
from keras.layers import Dense

# Define input variables for fuzzy system
distance_to_obstacle = ctrl.Antecedent(np.arange(0, 101, 1), 'distance_to_obstacle')
speed = ctrl.Antecedent(np.arange(0, 101, 1), 'speed')

# Define output variable for fuzzy system
steering_angle = ctrl.Consequent(np.arange(-45, 46, 1), 'steering_angle')

# Define membership functions for input variables
distance_to_obstacle['close'] = fuzz.trimf(distance_to_obstacle.universe, [0, 0, 25])
distance_to_obstacle['medium'] = fuzz.trimf(distance_to_obstacle.universe, [15, 40, 65])
distance_to_obstacle['far'] = fuzz.trimf(distance_to_obstacle.universe, [55, 100, 100])

speed['slow'] = fuzz.trimf(speed.universe, [0, 0, 30])
speed['medium'] = fuzz.trimf(speed.universe, [20, 50, 80])
speed['fast'] = fuzz.trimf(speed.universe, [70, 100, 100])

# Define membership functions for output variable
steering_angle['left'] = fuzz.trimf(steering_angle.universe, [-45, -45, -15])
steering_angle['straight'] = fuzz.trimf(steering_angle.universe, [-25, 0, 25])
steering_angle['right'] = fuzz.trimf(steering_angle.universe, [15, 45, 45])

# Define fuzzy rules
rule1 = ctrl.Rule(distance_to_obstacle['close'] & speed['slow'], steering_angle['left'])
rule2 = ctrl.Rule(distance_to_obstacle['close'] & speed['medium'], steering_angle['left'])
rule3 = ctrl.Rule(distance_to_obstacle['close'] & speed['fast'], steering_angle['left'])
rule4 = ctrl.Rule(distance_to_obstacle['medium'] & speed['slow'], steering_angle['straight'])
rule5 = ctrl.Rule(distance_to_obstacle['medium'] & speed['medium'], steering_angle['straight'])
rule6 = ctrl.Rule(distance_to_obstacle['medium'] & speed['fast'], steering_angle['right'])
rule7 = ctrl.Rule(distance_to_obstacle['far'] & speed['slow'], steering_angle['straight'])
rule8 = ctrl.Rule(distance_to_obstacle['far'] & speed['medium'], steering_angle['straight'])
rule9 = ctrl.Rule(distance_to_obstacle['far'] & speed['fast'], steering_angle['straight'])

# Create a fuzzy control system
autonomous_vehicle_fuzzy_system = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9])

# Create a simulation environment for the fuzzy system
autonomous_vehicle_simulation = ctrl.ControlSystemSimulation(autonomous_vehicle_fuzzy_system)

# Define the neural network for throttle control
throttle_control_nn = Sequential([
    Dense(8, input_dim=2, activation='relu'),
    Dense(1, activation='linear')
])

# Train the neural network with data (not shown here)
# ...

# Function to control the autonomous vehicle
def control_autonomous_vehicle(distance_to_obstacle, vehicle_speed):
    # Use the fuzzy system to determine the steering angle
    autonomous_vehicle_simulation.input['distance_to_obstacle'] = distance_to_obstacle
    autonomous_vehicle_simulation.input['speed'] = vehicle_speed
    autonomous_vehicle_simulation.compute()
    steering_angle_output = autonomous_vehicle_simulation.output['steering_angle']

    # Use the neural network to determine the throttle
    throttle_input = np.array([[distance_to_obstacle, vehicle_speed]])
    throttle_output = throttle_control_nn.predict(throttle_input)

    return steering_angle_output, throttle_output

# Example usage
distance_to_obstacle = 20
vehicle_speed = 80
steering_angle, throttle = control_autonomous_vehicle(distance_to_obstacle, vehicle_speed)
print(f"Steering angle: {steering_angle:.2f}, Throttle: {throttle[0][0]:.2f}")
"""
    return code

def getname():
    return ["hebb", "mcpitt", "kohonen", "linearly_seperable", "operation_on_fuzzy", "fuzzy_relation", "tsp", "shortestpath", "washingmachine", "neuro_fuzzy"]