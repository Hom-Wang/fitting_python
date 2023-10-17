import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

import fittinglib as ft

# %%
p_radi = 35
p_sens = np.array([[0.95, 0.02, 0.04], [0.02, 1.05, 0.06], [0.04, 0.06, 1.0]])
p_bias = np.array([-10,20,-30]).reshape(3,1)

print(f'''
    Ground Truth
    -- sens --------------------------- bias ------- radi
    {p_sens[0,0]:8.5f}, {p_sens[0,1]:8.5f}, {p_sens[0,2]:8.5f},   {p_bias[0,0]:9.3f},   {p_radi:9.3f},
    {p_sens[1,0]:8.5f}, {p_sens[1,1]:8.5f}, {p_sens[1,2]:8.5f},   {p_bias[1,0]:9.3f},
    {p_sens[2,0]:8.5f}, {p_sens[2,1]:8.5f}, {p_sens[2,2]:8.5f},   {p_bias[2,0]:9.3f},''')

v = p_radi * ft.get_sphere(n=300)
vr = (np.linalg.inv(p_sens) @ v + p_bias)

fit = ft.ellipsoid(v=vr)

sens = fit.get('sens')
bias = fit.get('bias')
radi = fit.get('radi')
vc = (sens @ (vr - bias))

print(f'''
    Ellipsoid Fitting
    -- sens --------------------------- bias ------- radi
    {sens[0,0]:8.5f}, {sens[0,1]:8.5f}, {sens[0,2]:8.5f},   {bias[0,0]:9.3f},   {radi:9.3f},
    {sens[1,0]:8.5f}, {sens[1,1]:8.5f}, {sens[1,2]:8.5f},   {bias[1,0]:9.3f},
    {sens[2,0]:8.5f}, {sens[2,1]:8.5f}, {sens[2,2]:8.5f},   {bias[2,0]:9.3f},
''')

# %%

x, y, z = v
fig = plt.figure("ellipsoid fitting", tight_layout=True, figsize=(12, 8))
gs = gridspec.GridSpec(3, 4, figure=fig)

ax1 = fig.add_subplot(gs[0, 0])
ax1.plot(vr[0, :], vr[1, :], '.')
ax1.plot(vc[0, :], vc[1, :], '.')
ax1.axis('equal')
ax1.grid()
ax1.set_xlabel('X-axis [uT]')
ax1.set_ylabel('Y-axis [uT]')

ax2 = fig.add_subplot(gs[1, 0], aspect='equal')
ax2.plot(vr[1, :], vr[2, :], '.')
ax2.plot(vc[1, :], vc[2, :], '.')
ax2.axis('equal')
ax2.grid()
ax2.set_xlabel('Y-axis [uT]')
ax2.set_ylabel('Z-axis [uT]')

ax3 = fig.add_subplot(gs[2, 0], aspect='equal')
ax3.plot(vr[2, :], vr[0, :], '.')
ax3.plot(vc[2, :], vc[0, :], '.')
ax3.axis('equal')
ax3.grid()
ax3.set_xlabel('Z-axis [uT]')
ax3.set_ylabel('X-axis [uT]')

ax3d = fig.add_subplot(gs[:, 1:], aspect='equal', projection='3d')
ax3d.scatter(*vr)
ax3d.scatter(*vc)
ax3d.axis('equal')
ax3d.set_xlabel('X-axis [uT]')
ax3d.set_ylabel('Y-axis [uT]')
ax3d.set_zlabel('Z-axis [uT]')

plt.show()

# %%
