import numpy as np
import matplotlib.pyplot as plt

# Stationary reference frame snapshot
t = np.linspace(0, 2*np.pi, 1000)

# d-axis and q-axis constant values
d_axis = np.full_like(t, 1.0)  # d-axis constant
q_axis = np.full_like(t, 0.0)  # q-axis zero

# Plot
plt.figure(figsize=(8,4))
plt.plot(t, d_axis, label=r'$d$-axis', color='blue', linewidth=2)
plt.plot(t, q_axis, label=r'$q$-axis', color='red', linewidth=2)

# Bold zero line
# plt.axhline(0, color='black', linewidth=2)

# Labels and formatting
#plt.title('Stationary Reference Frame Snapshot')
plt.xlabel('time')
plt.ylabel('Amplitude')
plt.grid(True, which='both', linestyle='--', linewidth=0.5)

# Remove axis numbers
plt.xticks([])
plt.yticks([])

plt.legend()
plt.tight_layout()
plt.show()