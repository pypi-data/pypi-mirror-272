def a8():
    print('''


import numpy as np

# Activation function (sigmoid)
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

# Derivative of sigmoid function
def sigmoid_derivative(x):
    return x * (1 - x)

# Input data for XOR
X = np.array([[0, 0],
              [0, 1],
              [1, 0],
              [1, 1]])

# Corresponding output data for XOR
y = np.array([[0],
              [1],
              [1],
              [0]])

# Initialize weights and biases randomly
np.random.seed(1)
input_neurons = 2
hidden_neurons = 2
output_neurons = 1

weights_input_hidden = np.random.uniform(size=(input_neurons, hidden_neurons))
biases_hidden = np.random.uniform(size=(1, hidden_neurons))
weights_hidden_output = np.random.uniform(size=(hidden_neurons, output_neurons))
biases_output = np.random.uniform(size=(1, output_neurons))

# Training the network
learning_rate = 0.1
epochs = 10000

for epoch in range(epochs):
    # Forward propagation
    hidden_layer_input = np.dot(X, weights_input_hidden) + biases_hidden
    hidden_layer_output = sigmoid(hidden_layer_input)
    output_layer_input = np.dot(hidden_layer_output, weights_hidden_output) + biases_output
    output = sigmoid(output_layer_input)

    # Backpropagation
    error = y - output
    d_output = error * sigmoid_derivative(output)
    error_hidden_layer = d_output.dot(weights_hidden_output.T)
    d_hidden_layer = error_hidden_layer * sigmoid_derivative(hidden_layer_output)

    # Update weights and biases
    weights_hidden_output += hidden_layer_output.T.dot(d_output) * learning_rate
    biases_output += np.sum(d_output, axis=0, keepdims=True) * learning_rate
    weights_input_hidden += X.T.dot(d_hidden_layer) * learning_rate
    biases_hidden += np.sum(d_hidden_layer, axis=0, keepdims=True) * learning_rate

# Testing the network
hidden_layer_input = np.dot(X, weights_input_hidden) + biases_hidden
hidden_layer_output = sigmoid(hidden_layer_input)
output_layer_input = np.dot(hidden_layer_output, weights_hidden_output) + biases_output
output = sigmoid(output_layer_input)

# Print the final output
print("Final Output:")
print(output)

''')
a8()