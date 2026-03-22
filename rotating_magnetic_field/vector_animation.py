import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

# --- Parameters ---
omega = 2 * np.pi * 1   # 1 Hz electrical frequency
t_max = 2               # seconds
fps = 100

# Time array for waveform plot
t_array = np.linspace(0, t_max, 1000)

# Phase axis angles
theta_A = 0
theta_B = 2*np.pi/3
theta_C = 4*np.pi/3

# --- Figure with 2 subplots ---
fig, (ax_field, ax_wave) = plt.subplots(1, 2, figsize=(12, 6))

# =========================
# LEFT: ROTATING FIELD
# =========================
ax_field.set_aspect('equal')
ax_field.set_xlim(-1.5, 1.5)
ax_field.set_ylim(-1.5, 1.5)
ax_field.set_title("Rotating Magnetic Field")

circle = plt.Circle((0, 0), 1.2, fill=False)
ax_field.add_patch(circle)

def draw_axis(theta, label, color):
    x = np.cos(theta)
    y = np.sin(theta)
    ax_field.plot([-x, x], [-y, y], linestyle='--', color=color)
    ax_field.text(1.3*x, 1.3*y, label, color=color, ha='center')

draw_axis(theta_A, "A", 'red')
draw_axis(theta_B, "B", 'green')
draw_axis(theta_C, "C", 'blue')

vec_A, = ax_field.plot([], [], color='red', linewidth=3)
vec_B, = ax_field.plot([], [], color='green', linewidth=3)
vec_C, = ax_field.plot([], [], color='blue', linewidth=3)
vec_sum, = ax_field.plot([], [], color='black', linewidth=4)

# =========================
# RIGHT: CURRENT WAVEFORMS
# =========================
ax_wave.set_title("3-Phase Currents")
ax_wave.set_xlim(0, t_max)
ax_wave.set_ylim(-1.5, 1.5)
ax_wave.set_xlabel("Time (s)")
ax_wave.set_ylabel("Current")

# Waveforms
iA_wave = np.sin(omega * t_array)
iB_wave = np.sin(omega * t_array - 2*np.pi/3)
iC_wave = np.sin(omega * t_array - 4*np.pi/3)

ax_wave.plot(t_array, iA_wave, color='red', label='iA')
ax_wave.plot(t_array, iB_wave, color='green', label='iB')
ax_wave.plot(t_array, iC_wave, color='blue', label='iC')

# Vertical time indicator
time_line = ax_wave.axvline(0, linestyle='--')

# Moving markers
marker_A, = ax_wave.plot([], [], 'o', color='red')
marker_B, = ax_wave.plot([], [], 'o', color='green')
marker_C, = ax_wave.plot([], [], 'o', color='blue')

ax_wave.legend()

# =========================
# ANIMATION UPDATE
# =========================
def update(frame):
    t = frame / fps

    # Currents
    iA = np.sin(omega * t)
    iB = np.sin(omega * t - 2*np.pi/3)
    iC = np.sin(omega * t - 4*np.pi/3)

    # Phase vectors
    Ax = iA * np.cos(theta_A)
    Ay = iA * np.sin(theta_A)

    Bx = iB * np.cos(theta_B)
    By = iB * np.sin(theta_B)

    Cx = iC * np.cos(theta_C)
    Cy = iC * np.sin(theta_C)

    # Resultant
    Rx = Ax + Bx + Cx
    Ry = Ay + By + Cy

    # Update field vectors
    vec_A.set_data([0, Ax], [0, Ay])
    vec_B.set_data([0, Bx], [0, By])
    vec_C.set_data([0, Cx], [0, Cy])
    vec_sum.set_data([0, Rx], [0, Ry])

    # Update waveform time line
    time_line.set_xdata([t])

    # Update markers
    marker_A.set_data([t], [iA])
    marker_B.set_data([t], [iB])
    marker_C.set_data([t], [iC])

    return (vec_A, vec_B, vec_C, vec_sum,
            time_line, marker_A, marker_B, marker_C)

# --- Run animation ---
frames = int(t_max * fps)
ani = FuncAnimation(fig, update, frames=frames, interval=1000/fps, blit=True)

plt.tight_layout()

# =========================
# SAVE TO GIF
# =========================
gif_filename = "rotating_magnetic_field.gif"
writer = PillowWriter(fps=fps)

ani.save(gif_filename, writer=writer)

print(f"GIF saved as: {gif_filename}")