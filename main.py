import math
import random

print("Hello world")

bias_default = 1
activation_default = 0
weights_default = (1, 1, 1, 1, 1, 1, 1, 1, 1, 1)
brain = [[]]
data = (1, 0, 0, 0)

class IdleNeuron:
    def __init__(self, weight, position):
        self.weight = weight #only one weight for singular input from global data
        self.output = 0
        self.position = position


    def get_input(self):
        global data
        return data[self.position] #get data corresponding to own position on diagram


    def process(self):
        self.output = self.weight * self.get_input() #idle neurons are linear

class Neuron:
    def __init__(self, activation, weights, layer, biasmode = False):
        self.activation = activation
        self.weights = weights
        self.layer = layer
        self.biasmode = biasmode
        self.active = False
        self.output = 0


    def gather_input(self):
        global brain
        result = 0
        while len(brain[self.layer-2]) > len(self.weights): #safe measure if previous layers are extended (eg. bias)
            self.weights.append((random.randint(0,100) / 100))

        for i in range(len(brain[self.layer-2])): #for previous layer + indexing
            result = result + self.weights[i] * brain[self.layer - 2][i].output #add Neuron output here /// -2 because indexing AND previous layer
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


def add_neuron_to_layer(layer, biasmode = True, activation = activation_default):
    global brain
    global data
    weight = []
    if layer > 1:
        for i in range(len(brain[layer - 2])):
            weight.append((random.randint(0, 100) / 100))
    else:
        for i in range(len(data)):
            weight.append((random.randint(0, 100) / 100))
    brain[layer-1].append(Neuron(activation, weight, layer, biasmode))

def add_default_layer(amount):
    global brain
    brain.append([])
    for i in range(amount):
        add_neuron_to_layer(len(brain), False)

def include_bias():
    for i in range(len(brain)):
        add_neuron_to_layer(i+1)

def prepare_idle_layer(amount):
    global brain
    for position in range(amount):
        brain[0].append(IdleNeuron((random.randint(0,100) / 100), position))

def process_forward():
    for layer in range(len(brain)):
        for neuron in range(len(brain[layer])):
            brain[layer][neuron].process()

def analyze_final_output():
    print("Final output:")
    for neuron in range(len(brain[-1])):
        print(brain[-1][neuron].output)
    print("*****************")

def analyze_layer_output(layer):
    print("Layer ", layer, " output:")
    for neuron in range(len(brain[layer - 1])):
        print(brain[layer - 1][neuron].output)
    print("*****************")

print(brain)
brain[0] = []
prepare_idle_layer(len(data))
add_default_layer(4)
add_default_layer(3)
add_default_layer(2)
add_default_layer(5)
add_neuron_to_layer(5, False)
add_neuron_to_layer(4, False)
include_bias()
print(brain)
process_forward()
analyze_layer_output(1)
analyze_layer_output(2)
analyze_layer_output(3)
analyze_layer_output(4)
analyze_layer_output(5)
analyze_final_output()



