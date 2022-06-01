import math
import random

print("Hello world")

weights_grand_index = []

bias_default = 1
activation_default = -10
weights_default = (1, 1, 1, 1, 1, 1, 1, 1, 1, 1)
brain = [[]]
dataset = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
data = [1, 0, 0, 0]
learn_rate = 0.2
momentum = 0.9
total_error = 0
grand_sum_error = 0


class IdleNeuron:
    def __init__(self, weight, position):
        self.weights = weight  # only one weight for singular input from global data
        self.weights_update = 0
        self.output = 0
        self.position = position
        self.error = 0

    def get_input(self):
        global data
        return data[self.position]  # get data corresponding to own position on diagram

    def process(self):
        self.output = self.weights * self.get_input()  # idle neurons are linear

    def calculate_cost(self):
        cost_delta = self.error * self.get_input()
        return cost_delta

    def set_error(self, new_error):
        self.error = new_error

    def update_weights(self):
        self.weights += self.weights_update


class Neuron:
    def __init__(self, activation, weights, layer, biasmode = False):
        self.activation = activation
        self.weights = weights
        self.weights_update = [0]
        for o in range(len(weights)):
            self.weights_update.append(0)
        self.layer = layer
        self.biasmode = biasmode
        self.active = False
        self.output = 0
        self.error = 0

    def gather_input(self):
        global brain
        result = 0
        while len(brain[self.layer-2]) > len(self.weights):  # safe measure if previous layers are extended (eg. bias)
            self.weights.append((random.randint(0, 100) / 100))

        for z in range(len(brain[self.layer-2])):  # for previous layer + indexing
            result = result + self.weights[z] * brain[self.layer - 2][z].output  # add Neuron output here /// -2 because indexing AND previous layer
        if result > self.activation:
            self.active = True
            return result
        else:
            self.active = False
            return 0

    def process(self):
        if self.biasmode:
            self.output = bias_default
            return self.output
        else:
            factor = self.gather_input()
            if self.active:
                self.output = 1 / (1 + math.e ** -factor)
                self.active = False
                return self.output
            else:
                self.output = 0
                return self.output

    def set_error(self, new_error):
        self.error = new_error

    def set_weight_delta(self, value, position):
        self.weights_update[position] = value

    def calculate_cost(self):
        derivative = self.output * (1 - self.output)
        cost_delta = self.error * derivative
        return cost_delta

    def update_weights(self):
        for x in range(len(self.weights)):
            self.weights[x] += self.weights_update[x]


###############################
# NETWORK STRUCTURE FUNCTIONS #
###############################
def add_neuron_to_layer(layer, biasmode=True, activation=activation_default):
    global brain
    global data
    weight = []
    if layer > 1:
        for n in range(len(brain[layer - 2])):
            weight.append((random.randint(0, 100) / 100))
    else:
        for n in range(len(data)):
            weight.append((random.randint(0, 100) / 100))
    brain[layer-1].append(Neuron(activation, weight, layer, biasmode))


def add_default_layer(amount):
    global brain
    brain.append([])
    for u in range(amount):
        add_neuron_to_layer(len(brain), False)


def add_last_layer():
    add_default_layer(len(data))


def include_bias():  # use as last option!!!
    for q in range(len(brain) - 1):
        add_neuron_to_layer(q+1)


def prepare_idle_layer(amount):
    global brain
    for position in range(amount):
        brain[0].append(IdleNeuron((random.randint(0, 100) / 100), position))


########################
# PROCESSING FUNCTIONS #
########################
def process_forward():
    global brain
    for layer in range(len(brain)):
        for neuron in range(len(brain[layer])):
            brain[layer][neuron].process()


def process_backward():
    global brain
    global total_error
    global learn_rate
    global momentum
    total_error = 0
    for neuron in range(len(brain[-1])):  # calculate error for last layer
        error = data[neuron] - brain[-1][neuron].output  # average squared error
        # print("tu jest error: ", error)
        brain[-1][neuron].set_error(error)
        total_error += error ** 2  # MSE for one error in sum

    for layer in range(len(brain), 1, -1):  # for each layer
        # print("layer number: ", layer)
        for prev_neuron in range(len(brain[layer - 2])):  # for each previous neuron
            local_error = 0
            prev_output = brain[layer - 2][prev_neuron].output
            # print("prev_output: ", prev_output)
            for curr_neuron in range(len(brain[layer - 1])):  # each current neuron

                update_value = brain[layer - 1][curr_neuron].calculate_cost() * prev_output * learn_rate + (momentum * brain[layer - 1][curr_neuron].weights_update[prev_neuron]) # ADD MOMENTUM FORMULA
                local_error += brain[layer - 1][curr_neuron].calculate_cost() * brain[layer - 1][curr_neuron].weights[prev_neuron]
                brain[layer - 1][curr_neuron].set_weight_delta(update_value, prev_neuron)

            brain[layer - 2][prev_neuron].set_error(local_error)
            # local_error = 1 * brain[layer].weights[1] #wtf
    for layer in range(len(brain)):
        for neuron in range(len(brain[layer])):
            brain[layer][neuron].update_weights()


###########################
# DATA ANALYSIS FUNCTIONS #
###########################
def analyze_final_output():
    global brain
    print("Final output:")
    for neuron in range(len(brain[-1])):
        print(brain[-1][neuron].output)
    print("*****************")


def analyze_layer_output(layer):
    global brain
    print("Layer ", layer, " output:")
    for neuron in range(len(brain[layer - 1])):
        print(brain[layer - 1][neuron].output)
    print("*****************")


def analyze_final_error():
    global brain
    print("Final layer error:")
    for neuron in range(len(brain[-1])):
        print(brain[-1][neuron].error)
    print("*****************")


def analyze_layer_error(layer):
    global brain
    print("Layer ", layer, " error:")
    for neuron in range(len(brain[layer - 1])):
        print(brain[layer - 1][neuron].error)
    print("*****************")


def analyze_layer_weights(layer):
    global brain
    print("Layer ", layer, " weights:")
    for neuron in range(len(brain[layer - 1])):
        if layer != 1:
            print("Neuron ", neuron, ": ")
            for weight in range(len(brain[layer - 1][neuron].weights)):
                print(brain[layer - 1][neuron].weights[weight])
        else:
            if neuron != len(brain[layer - 1]) - 1:
                print("Neuron ", neuron, ": ")
                print(brain[layer - 1][neuron].weights)
            else:
                print("Neuron ", neuron, ": ")
                for n in range(len(brain[0][-1].weights)):
                    print(brain[0][-1].weights[n])
    print("*****************")


def raw_layer_weights(layer):
    global brain
    for neuron in range(len(brain[layer - 1])):
        if layer != 1:
            for weight in range(len(brain[layer - 1][neuron].weights)):
                print(brain[layer - 1][neuron].weights[weight])
        else:
            if neuron != len(brain[layer - 1]) - 1:
                print(brain[layer - 1][neuron].weights)
            else:
                for n in range(len(brain[0][-1].weights)):
                    print(brain[0][-1].weights[n])


print(brain)
brain[0] = []
prepare_idle_layer(len(data))
add_default_layer(2)
add_last_layer()
print(brain)
include_bias()
choice = input("Random learning *1* / Sorted learning *2*")
print("*****START LEARNING*****")
for i in range(10000):
    grand_sum_error = 0
    for w in range(4):
        sum_error = 0
        if int(choice) == 1:
            random.shuffle(dataset)
        data = dataset[w]
        process_forward()
        process_backward()
        for t in range(4):
            sum_error += abs(data[t] - brain[len(brain) - 1][t].output)
        grand_sum_error += sum_error

    if grand_sum_error < 0.15:
        print("Finished after ", i, " epochs")
        break

print("*****LEARNING FINISHED*****")
dataset = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]  # Change back to normal order in case choice = 1
while True:
    number = input("Choose which dataset to use (1 - 4)")
    if int(number) == 5:
        break
    data = dataset[int(number) - 1]
    process_forward()
    analyze_final_output()
    print("Grand error sum for dataset: ", grand_sum_error)
for k in range(len(brain)):
    raw_layer_weights(k+1)

