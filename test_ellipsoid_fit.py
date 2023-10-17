import numpy as np
import matplotlib.pyplot as plt

import fittinglib as ft

# %%
p_radi = 35
p_sens = np.array([[0.95, 0.02, 0.04], [0.02, 1.05, 0.06], [0.04, 0.06, 1.0]])
p_bias = np.array([-10,20,-30]).reshape(3,1)

v = p_radi * ft.get_sphere(n=300)
vr = (np.linalg.inv(p_sens) @ v + p_bias)

fit = ft.ellipsoid(v=vr)

sens = fit.get('sens')
bias = fit.get('bias')
radi = fit.get('radi')
vc = (sens @ (vr - bias))

print(sens)
print(bias)
print(radi)

# %%

x, y, z = v
fig = plt.figure("sphere points")
ax = fig.add_subplot(111, aspect='equal', projection='3d')

# ax.plot_surface(x, y, z, cmap=plt.cm.YlGnBu_r)
ax.scatter(*vr)
ax.scatter(*vc)
ax.axis('equal')
plt.show()

# %%
