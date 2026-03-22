import numpy as np
import matplotlib.pyplot as plt

# --- Configuration ---
S = 12          # Number of slots
p = 1           # Number of pole pairs (2 poles)
slot_pitch_deg = 360 / S  # 30 degrees per slot

# Coil Pitch (Short pitch: 5 slots instead of 6)
coil_pitch_slots = 5 
gamma_deg = coil_pitch_slots * slot_pitch_deg 

theta = np.linspace(0, 360, 1000)

def get_wf(pitch_deg):
    wf = np.zeros_like(theta)
    # Phase A occupies 2 slots (q=2)
    # Slot 1 (0°) and Slot 2 (30°)
    for start_deg in [0, 30]:
        end_deg = start_deg + pitch_deg
        # Periodic pulse logic
        pulse = ((theta % 360 >= start_deg) & (theta % 360 <= end_deg)).astype(float)
        wf += pulse
    return wf - np.mean(wf)



def get_wf_full():
    return np.where(theta % 360 < 180, 1, -1)

def get_wf_simple(coil_location):
    wf = np.zeros_like(theta)
    
    return None

wf_full = get_wf_full()
wf_short = get_wf(gamma_deg)

# --- Plotting ---
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

# Subplot 1: Winding Function with Coil Markers
ax1.step(theta, wf_full, label='Full Pitch (180°)', alpha=0.5, color='blue', linestyle='--')
ax1.step(theta, wf_short, label=f'Short Pitch', color='red', where='post', linewidth=2)

# Add Coil Placement Markers for Short Pitch
# Phase A: Slots 1,2 (Go) and Slots 6,7 (Return)
# go_slots = [0, 30]
# return_slots = [0 + gamma_deg, 30 + gamma_deg]

# ax1.scatter(go_slots, [0, 0,], color='blue', s=100, label='Coil Side: Go (In)', zorder=5)
# ax1.scatter(return_slots, [0, 0], facecolors='none', edgecolors='blue', s=100, 
#             linewidth=2, label='Coil Side: Return (Out)', zorder=5)

# Labeling slots
for i in range(S):
    ax1.annotate(f'S{i+1}', (i*slot_pitch_deg, 0.1), ha='center', fontsize=9, color='gray')

ax1.set_title(f'Winding Function: {S}-Slot, {2*p}-Pole Stator')
ax1.set_xlabel('Electrical Angle (Degrees)')
ax1.set_ylabel('Normalized MMF')
ax1.set_xticks(np.arange(0, 361, 30))
ax1.grid(True, linestyle=':', alpha=0.6)
ax1.legend(loc='upper right')

# Subplot 2: FFT Comparison
N = len(wf_short)
fft_full = np.abs(np.fft.rfft(wf_full)) / (N / 2)
fft_short = np.abs(np.fft.rfft(wf_short)) / (N / 2)
harmonics = np.arange(1, 15)

width = 0.35
ax2.bar(harmonics - width/2, fft_full[1:15], width, label='Full Pitch')
ax2.bar(harmonics + width/2, fft_short[1:15], width, label='Short Pitch', color='red')

ax2.set_title('Harmonic Magnitude Comparison')
ax2.set_xlabel('Harmonic Order')
ax2.set_ylabel('Amplitude')
ax2.set_xticks(harmonics)
ax2.grid(axis='y', linestyle='--', alpha=0.7)
ax2.legend()

plt.tight_layout()
plt.show()