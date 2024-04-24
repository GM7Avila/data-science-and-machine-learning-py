import numpy as np

Nt = 10000
Nin = 0

for i in range(Nt):
    x = np.random.rand(1)
    y = np.random.rand(1)
    
    if y**2 + x**2 <= 1:
        Nin += 1
    
PI = 4 * Nin/Nt
print("Valor de pi:", PI)