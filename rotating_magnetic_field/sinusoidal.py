import numpy as np
import matplotlib.pyplot as plt

# Time vector for one electrical period
t = np.linspace(0, 2*np.pi, 1000)

# Three-phase waveforms (120° phase shift)
phase_a = np.sin(t)
phase_b = np.sin(t - 2*np.pi/3)
phase_c = np.sin(t - 4*np.pi/3)

# Plot
plt.figure()
plt.plot(t, phase_a, color='r', label='Phase A')
plt.plot(t, phase_b, color='g', label='Phase B')
plt.plot(t, phase_c, color='b', label='Phase C')

plt.xlabel("Time")
plt.ylabel("Current")
# plt.title("Three-Phase Waveforms (One Period)")
# plt.legend()
plt.grid(True)
plt.xlim(0, 2*np.pi)

# Hide numbers but keep gridlines
plt.tick_params(labelbottom=False, labelleft=False)

plt.show()
