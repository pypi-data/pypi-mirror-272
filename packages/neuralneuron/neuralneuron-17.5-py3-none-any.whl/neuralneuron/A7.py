def b1():
    print('''

# 7. Implement Artificial Neural Network training process in Python by using Forward Propagation,
# Back Propagation. 

import numpy as np
import matplotlib.pyplot as plt 
import math


# Step 1: Define the sigmoid function and its derivative
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def sigmoid_derivative(x):
    return x * (1 - x)

input_neurons = 0
hidden_neurons = 0
output_neurons = 0
hidden_weights =0
hidden_bias =0
output_weights =0
output_bias =0


def train_neural_network(X, y, learning_rate, epochs):
    print("Training Neural Network")
    global hidden_weights,hidden_bias,output_weights,output_bias,input_neurons,hidden_neurons,output_neurons
    input_neurons = X.shape[1]
    hidden_neurons = 4
    output_neurons = y.shape[1]


    # Initialize the weights and biases with random values
    hidden_weights = np.random.uniform(size=(input_neurons, hidden_neurons))
    hidden_bias = np.random.uniform(size=(1, hidden_neurons))
    output_weights = np.random.uniform(size=(hidden_neurons, output_neurons))
    output_bias = np.random.uniform(size=(1, output_neurons))
    
    
    # Perform the training iterations
    for i in range(epochs):
        # Forward propagation
        hidden_layer_activation = np.dot(X, hidden_weights) + hidden_bias
        hidden_layer_output = sigmoid(hidden_layer_activation)

        output_layer_activation = np.dot(hidden_layer_output, output_weights) + output_bias
        predicted_output = sigmoid(output_layer_activation)

        # Backward propagation
        error = y - predicted_output
        d_predicted_output = error * sigmoid_derivative(predicted_output)

        error_hidden_layer = d_predicted_output.dot(output_weights.T)
        d_hidden_layer = error_hidden_layer * sigmoid_derivative(hidden_layer_output)

        # Update the weights and biases
        output_weights += hidden_layer_output.T.dot(d_predicted_output) * learning_rate
        output_bias += np.sum(d_predicted_output, axis=0, keepdims=True) * learning_rate
        hidden_weights += X.T.dot(d_hidden_layer) * learning_rate
        hidden_bias += np.sum(d_hidden_layer, axis=0, keepdims=True) * learning_rate

    print("Training Complete")

def test_network(X):
    global hidden_weights,hidden_bias,output_weights,output_bias,input_neurons,hidden_neurons,output_neurons
    hidden_layer_activation = np.dot(X, hidden_weights) + hidden_bias
    hidden_layer_output = sigmoid(hidden_layer_activation)

    output_layer_activation = np.dot(hidden_layer_output, output_weights) + output_bias
    predicted_output = sigmoid(output_layer_activation)
    return round(predicted_output[0][0])

#XOR Gate Traning 
X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]]) #inputs
T = np.array([[0], [1], [1], [0]]) # targets

train_neural_network(X, T, learning_rate=0.1, epochs=10000)

print(test_network([0,1]))
print(f"Inputs:{X[0]} Expected:{0} Got:{test_network(X[0])}")
print(f"Inputs:{X[1]} Expected:{1} Got:{test_network(X[1])}")
print(f"Inputs:{X[2]} Expected:{1} Got:{test_network(X[2])}")
print(f"Inputs:{X[3]} Expected:{0} Got:{test_network(X[3])}")
''')
b1()