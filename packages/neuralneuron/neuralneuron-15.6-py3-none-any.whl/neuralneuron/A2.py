def a2():
    print('''

import numpy as np

def mp(n, w1, w2, x1):
    w = p = 0
    if (w1 < 0 or w2 < 0):
        p = 1
    if (w1 >= 0 or w2 >= 0):
        w = 1

    theta = n * w - p  # Threshold calculation
    yin =  [0] * 4
    ytarget = [0] * 4
 
    for i in range(len(x1)):
        yin[i] = (w1 * x1[i] + w2 * x2[i])
        ytarget[i] = 1 if(yin[i] >= theta) else 0
    
    return yin, ytarget, theta

x1 = [0, 0, 1, 1]
x2 = [0, 1, 0, 1]
t  = [0, 0, 1, 0]
n = 2
w1 = 1
w2 = -1

yin, ytarget, theta = mp(n, w1, w2, x1)

print(f"threshold = {theta}")
print("\nANDNOT function using McCulloch-Pitts neural network\n")
print("x1 \t x2 \t t \t yin \t y")
for i in range(len(x1)):
    print(f"{x1[i]} \t {x2[i]} \t {t[i]} \t {yin[i]} \t{ytarget[i]}")''')
a2()