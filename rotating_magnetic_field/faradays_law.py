import numpy as np
import matplotlib.pyplot as plt

# Time vector (conceptual)
t = np.linspace(0, 2*np.pi, 500)

# Flux linkage (sinusoidal)
flux = np.sin(t)

# Induced voltage (Faraday's Law: v = dλ/dt)
voltage = np.gradient(flux, t)

fig, axs = plt.subplots(2, 1, figsize=(8,6), sharex=True)

# ---- Top Plot: Flux Linkage ----
axs[0].plot(t, flux, linewidth=2)
axs[0].set_title("Flux Linkage")
axs[0].set_ylabel("Flux Linkage (λ)")
#axs[0].grid(True)

# Bold black zero line
axs[0].axhline(0, color='black', linewidth=2)

# ---- Bottom Plot: Induced Voltage ----
axs[1].plot(t, voltage, linewidth=2)
axs[1].set_title("Induced Voltage")
axs[1].set_ylabel("Voltage (v)")
axs[1].set_xlabel("Time")
#axs[1].grid(True)

# Bold black zero line
axs[1].axhline(0, color='black', linewidth=2)

# Remove tick labels (conceptual illustration)
for ax in axs:
    ax.set_xticklabels([])
    ax.set_yticklabels([])

plt.tight_layout()
plt.show()