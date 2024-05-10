def a5():
    print('''

# Bidirectional Associative Memory
import numpy as np
X=np.array([
    [ 1, -1, -1, -1],
    [-1,  1,  1, -1]
])

Y=np.array([
    [-1,  1],
    [ 1, -1]
])

W = np.dot(X.T, Y)
print(W)

def activate(x):
    return np.where(x>0,1,-1)

# Forward Pass s->t
print("Forward Pass")
x_test = X[0]
y_test = activate(np.dot(x_test, W))
print(f"Input(X):{x_test} Output(Y):{y_test}")
x_test = X[1]
y_test = activate(np.dot(x_test, W))
print(f"Input(X):{x_test} Output(Y):{y_test}")

# Backward Pass t->s
print("\nBackward Pass")
y_test = Y[0]
x_test = activate(np.dot(y_test,W.T))
print(f"Input(Y):{y_test} Output(X):{x_test}")
y_test = Y[1]
x_test = activate(np.dot(y_test,W.T))
print(f"Input(Y):{y_test} Output(X):{x_test}")

''')
a5()

