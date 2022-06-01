import math
import random

print("Hello world")

bias_default = 1
activation_default = -10
weights_default = (1, 1, 1, 1, 1, 1, 1, 1, 1, 1)
brain = [[]]
data = (1, 0, 0, 0)
learn_rate = 1
momentum = 0
total_error = 0

class IdleNeuron:
    def __init__(self, weight, position):
        self.weight = weight #only one weight for singular input from global data
        self.weights_update = weight
        self.output = 0
        self.position = position
        self.error = 0


    def get_input(self):
        global data
        return data[self.position] #get data corresponding to own position on diagram

    def process(self):
        self.output = self.weight * self.get_input() #idle neurons are linear

    def calculate_cost(self):
        cost_delta = self.error * self.get_input()
        return cost_delta

    def learn(self):
        print("smart stuff here")

    def set_error(self, new_error):
        self.error = new_error

    def update_weights(self):
        self.weight += self.weights_update

class Neuron:
    def __init__(self, activation, weights, layer, biasmode = False):
        self.activation = activation
        self.weights = weights
        self.weights_update = weights
        self.layer = layer
        self.biasmode = biasmode
        self.active = False
        self.output = 0
        self.error = 0

    def gather_input(self):
        global brain
        result = 0
        while len(brain[self.layer-2]) > len(self.weights): #safe measure if previous layers are extended (eg. bias)
            self.weights.append((random.randint(0,100) / 100))

        for z in range(len(brain[self.layer-2])): #for previous layer + indexing
            result = result + self.weights[z] * brain[self.layer - 2][z].output #add Neuron output here /// -2 because indexing AND previous layer
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


#############################
#NETWORK STRUCTURE FUNCTIONS#
#############################
def add_neuron_to_layer(layer, biasmode = True, activation = activation_default):
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

def include_bias(): #use as last option!!!
    for q in range(len(brain) - 1):
        add_neuron_to_layer(q+1)

def prepare_idle_layer(amount):
    global brain
    for position in range(amount):
        brain[0].append(IdleNeuron((random.randint(0,100) / 100), position))


######################
#PROCESSING FUNCTIONS#
######################
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
    for neuron in range(len(brain[-1])): #calculate error for last layer
        error = data[neuron] - brain[-1][neuron].output  #average squared error
        #print("tu jest error: ", error)
        brain[-1][neuron].set_error(error)
        total_error += error ** 2 #MSE for one error in sum

    for layer in range(len(brain), 1, -1):#for each layer
        print("layer number: ", layer)
        for prev_neuron in range(len(brain[layer - 2])):#for each previous neuron
            local_error = 0
            prev_output = brain[layer - 2][prev_neuron].output
            print("prev_output: ", prev_output)
            for curr_neuron in range(len(brain[layer - 1])):#each current neuron

                update_value = brain[layer - 1][curr_neuron].calculate_cost() * prev_output #* learn_rate + (momentum * 3) #ADD MOMENTUM FORMULA
                local_error += brain[layer - 1][curr_neuron].calculate_cost() * brain[layer - 1][curr_neuron].weights[prev_neuron]
                brain[layer - 1][curr_neuron].set_weight_delta(update_value, prev_neuron)

            brain[layer - 2][prev_neuron].set_error(local_error)
            #local_error = 1 * brain[layer].weights[1] #wtf
 #   for layer in range(len(brain)):
  #      for neuron in range(len(brain[layer])):
   #         brain[layer][neuron].update_weights()

#########################
#DATA ANALYSIS FUNCTIONS#
#########################
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

print(brain)
brain[0] = []
prepare_idle_layer(len(data))
add_default_layer(4)
add_default_layer(3)
add_default_layer(2)
add_default_layer(5)
add_last_layer()
print(brain)
#include_bias()
for i in range(len(brain)):
    analyze_layer_error(i+1)
process_forward()
analyze_final_output()
process_backward()
for i in range(10):
    process_forward()
    process_backward()
for i in range(len(brain)):
    analyze_layer_error(i+1)
analyze_layer_output(6)
print(total_error)




