def a1():
	print('''

import numpy as np
import matplotlib.pyplot as plt

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def tanh(x):
    return np.tanh(x)

def relu(x):
    return np.maximum(0, x)

def leaky_relu(x, alpha=0.01):
    return np.where(x > 0, x, alpha * x)

def softmax(x):
    exp_x = np.exp(x - np.max(x))  # To prevent overflow
    return exp_x / exp_x.sum(axis=0, keepdims=True)

# Generate data
x = np.linspace(-5, 5, 100)

# Calculate activation function values
sigmoid_values = sigmoid(x)
tanh_values = tanh(x)
relu_values = relu(x)
leaky_relu_values = leaky_relu(x)
softmax_values = softmax(x)
print("choose which plot want-")
print("1.Sigmoid Activation Function\n2.Tanh Activation Function\n3.ReLU Activation Function\n4.Leaky ReLU Activation Function\n5.Softmax Activation Function\n")

ch=int(input("Enter choice number->"))
# Plotting
plt.figure(figsize=(12, 8))
if ch==1:
    plt.subplot(2, 3, 1)
    plt.plot(x, sigmoid_values, label='Sigmoid')
    plt.title('Sigmoid Activation Function')
    plt.legend()
elif ch==2:
    plt.subplot(2, 3, 2)
    plt.plot(x, tanh_values, label='Tanh')
    plt.title('Tanh Activation Function')
    plt.legend()
elif ch==3:
    plt.subplot(2, 3, 3)
    plt.plot(x, relu_values, label='ReLU')
    plt.title('ReLU Activation Function')
    plt.legend()
elif ch==4:
    plt.subplot(2, 3, 4)
    plt.plot(x, leaky_relu_values, label='Leaky ReLU')
    plt.title('Leaky ReLU Activation Function')
    plt.legend()
elif ch==5:
    plt.subplot(2, 3, 5)
    plt.plot(x, softmax_values, label='Softmax')
    plt.title('Softmax Activation Function')
    plt.legend()

plt.tight_layout()
plt.show()
''')
a1()