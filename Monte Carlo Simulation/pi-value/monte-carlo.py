import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

num_points = 10000

x = np.random.uniform(-1, 1, num_points)
y = np.random.uniform(-1, 1, num_points)

distance = np.sqrt(x**2 + y**2)

inside_circle = distance <= 1
num_inside_circle = np.sum(inside_circle)

# estimativa de Pi usando a fórmula da área do círculo
estimated_pi = 4 * (num_inside_circle / num_points)


data = pd.DataFrame({'x': x, 'y': y, 'inside_circle': inside_circle})
plt.figure(figsize=(8, 8))
plt.scatter(data['x'], data['y'], c=data['inside_circle'], cmap='coolwarm', alpha=0.5)
plt.xlabel('x')
plt.ylabel('y')
plt.title('Estimativa de Pi usando Monte Carlo')
circle = plt.Circle((0, 0), 1, color='black', fill=False)
plt.gca().add_artist(circle)
plt.axis('equal')
plt.show()

print("Valor estimado de Pi:", estimated_pi)
