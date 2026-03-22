import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# -----------------------------
# User Inputs
# -----------------------------
frequency = 10000        # Hz
radius = 0.01           # meters (1 cm conductor)
sigma = 5.8e7           # S/m (copper)
mu0 = 4*np.pi*1e-7      # permeability of free space
mu_r = 1                # relative permeability
frames = 100

# -----------------------------
# Derived Parameters
# -----------------------------
omega = 2 * np.pi * frequency
mu = mu0 * mu_r
delta = np.sqrt(2 / (omega * mu * sigma))  # skin depth

print(f"Skin depth: {delta*1000:.3f} mm")

# -----------------------------
# Create Grid (circular cross-section)
# -----------------------------
n = 200
x = np.linspace(-radius, radius, n)
y = np.linspace(-radius, radius, n)
X, Y = np.meshgrid(x, y)

R = np.sqrt(X**2 + Y**2)

# Mask outside conductor
mask = R <= radius

# -----------------------------
# Current density function
# -----------------------------
def current_density(r, t):
    # avoid division issues at center
    return np.exp(-(radius - r) / delta) * np.sin(omega * t)

# -----------------------------
# Plot Setup
# -----------------------------
fig, ax = plt.subplots(figsize=(6, 6))
ax.set_aspect('equal')
ax.set_title("Skin Effect in Circular Conductor")

# Initial field
Z = np.zeros_like(R)
Z[mask] = current_density(R[mask], 0)

cmap = plt.cm.seismic
im = ax.imshow(
    Z,
    extent=[-radius, radius, -radius, radius],
    origin='lower',
    cmap=cmap,
    vmin=-1,
    vmax=1
)

# Draw conductor boundary
circle = plt.Circle((0, 0), radius, color='black', fill=False, linewidth=2)
ax.add_patch(circle)

ax.set_xticks([])
ax.set_yticks([])

cbar = plt.colorbar(im)
cbar.set_label("Current Density (normalized)")

# -----------------------------
# Animation Update Function
# -----------------------------
def update(frame):
    t = frame / frames * (1 / frequency) * 2  # scale time
    Z = np.zeros_like(R)
    Z[mask] = current_density(R[mask], t)
    im.set_array(Z)
    return [im]

# -----------------------------
# Run Animation
# -----------------------------
anim = FuncAnimation(
    fig,
    update,
    frames=frames,
    interval=50,
    blit=True
)

plt.show()