import numpy as np
import matplotlib.pyplot as plt

# Time axis (one electrical period)
t = np.linspace(0, 2*np.pi, 1000)

# Two orthogonal components (90° phase shift)
alpha = np.sin(t)           # α-axis component
beta  = np.sin(t + np.pi/2) # β-axis component (90° ahead)

# Plot
plt.figure(figsize=(8,4))
plt.plot(t, alpha, label=r'q-s component', color='red', linewidth=2)
plt.plot(t, beta, label=r'd-s component', color='blue', linewidth=2)

# Bold zero line
plt.axhline(0, color='black', linewidth=2)

# Labels and formatting
# plt.title('Conceptual Stationary Reference Frame Components')
plt.xlabel('time')
plt.ylabel('Amplitude')
plt.grid(True, which='both', linestyle='--', linewidth=0.5)

# Remove axis numbers
plt.xticks([])
plt.yticks([])

plt.legend()
plt.tight_layout()
plt.show()