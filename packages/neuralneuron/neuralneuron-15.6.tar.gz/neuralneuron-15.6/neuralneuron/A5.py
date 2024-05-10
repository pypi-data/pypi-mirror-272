def a5():
    print('''

import numpy as np

class BAM:
    def __init__(self, input_size, output_size):
        self.input_size = input_size
        self.output_size = output_size
        self.weights = np.zeros((input_size, output_size))

    def train(self, input_patterns, output_patterns):
        for input_pattern, output_pattern in zip(input_patterns, output_patterns):
            self.weights += np.outer(input_pattern, output_pattern)

    def recall(self, input_pattern):
        output_pattern = np.dot(input_pattern, self.weights.T)
        output_pattern[output_pattern >= 0] = 1
        output_pattern[output_pattern < 0] = -1
        return output_pattern

# Example with two pairs of vectors
input_patterns = np.array([[1, -1], [1, 1]])
output_patterns = np.array([[1, 1], [-1, 1]])

# Create and train the BAM
bam = BAM(input_size=len(input_patterns[0]), output_size=len(output_patterns[0]))
bam.train(input_patterns, output_patterns)

# Test recall
test_input = np.array([1, -1])
recalled_output = bam.recall(test_input)

# Display results
print("Input Pattern:", test_input)
print("Recalled Output Pattern:", recalled_output)

''')
a5()

