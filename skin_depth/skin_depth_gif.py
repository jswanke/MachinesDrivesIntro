import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

# -----------------------------
# User Inputs
# -----------------------------
frequency = 10000        # Hz
radius = 0.01           # meters
sigma = 5.8e7           # copper conductivity
mu0 = 4*np.pi*1e-7
mu_r = 1
frames = 100

# -----------------------------
# Derived Parameters
# -----------------------------
omega = 2 * np.pi * frequency
mu = mu0 * mu_r
delta = np.sqrt(2 / (omega * mu * sigma))

print(f"Skin depth: {delta*1000:.3f} mm")

# -----------------------------
# Grid
# -----------------------------
n = 200
x = np.linspace(-radius, radius, n)
y = np.linspace(-radius, radius, n)
X, Y = np.meshgrid(x, y)
R = np.sqrt(X**2 + Y**2)
mask = R <= radius

# -----------------------------
# Current Density
# -----------------------------
def current_density(r, t):
    return np.exp(-(radius - r) / delta) * np.sin(omega * t)

# -----------------------------
# Plot Setup
# -----------------------------
fig, ax = plt.subplots(figsize=(6, 6))
ax.set_aspect('equal')
ax.set_title(f"Frequency: {frequency}, Cond.: {sigma}, ur: {mu_r}")

Z = np.zeros_like(R)
Z[mask] = current_density(R[mask], 0)

im = ax.imshow(
    Z,
    extent=[-radius, radius, -radius, radius],
    origin='lower',
    cmap='seismic',
    vmin=-1,
    vmax=1
)

circle = plt.Circle((0, 0), radius, color='black', fill=False, linewidth=2)
ax.add_patch(circle)

ax.set_xticks([])
ax.set_yticks([])

plt.colorbar(im, label="Current Density (normalized)")

# -----------------------------
# Animation function (FuncAnimation)
# -----------------------------
def update(frame):
    t = frame / frames * (2 / frequency)
    Z = np.zeros_like(R)
    Z[mask] = current_density(R[mask], t)
    im.set_array(Z)
    return (im,)

# -----------------------------
# Create animation
# -----------------------------
anim = FuncAnimation(fig, update, frames=frames, interval=50, blit=True)

# -----------------------------
# Save GIF
# -----------------------------
anim.save(f"skin_effect_f{frequency}_c{round(sigma/10**6, 0)}_ur{mu_r}.gif", writer=PillowWriter(fps=20))

print("Saved: skin_effect.gif")

plt.show()