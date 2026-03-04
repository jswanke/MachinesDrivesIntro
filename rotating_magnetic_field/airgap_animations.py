import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# =========================
# Load Excel Data
# =========================
file_path = "C:\\Users\\james\\git-c\\MachinesDrivesIntro\\rotating_magnetic_field\\6s2p_data_updated.xlsx"   # <-- change to your file path
df = pd.read_excel(file_path, sheet_name="3phase")

export_gif = True              # Set to True to export GIF
gif_filename = "3phase.gif"
fps = 15

angle = df["Angle"].values
step_columns = [col for col in df.columns if col.startswith("Step")]

# =========================
# Setup Plot
# =========================
fig, ax = plt.subplots(figsize=(8, 5))
line, = ax.plot([], [])

ax.set_xlim(angle.min(), angle.max())
ax.set_ylim(df[step_columns].values.min(),
            df[step_columns].values.max())

ax.set_xlabel("Electrical Angle (deg)", fontsize=12)
ax.set_ylabel("Airgap Radial Field (T)", fontsize=12)
title = ax.set_title("Radial Magnetic Field", fontsize=14)

ax.grid(True)

# =========================
# Animation Functions
# =========================
def init():
    line.set_data([], [])
    return line,

def update(frame):
    step_name = step_columns[frame]
    y_data = df[step_name].values
    
    line.set_data(angle, y_data)
    title.set_text(f"{step_name}")
    
    return line, title

# =========================
# Create Animation
# =========================
ani = FuncAnimation(
    fig,
    update,
    frames=len(step_columns),
    init_func=init,
    interval=100,   # milliseconds between frames
    blit=True,
    repeat=True
)

plt.tight_layout()


# =========================
# Export Option
# =========================
if export_gif:
    print("Saving GIF...")
    ani.save(gif_filename, writer="pillow", fps=fps)
    print(f"Saved as {gif_filename}")

plt.show()