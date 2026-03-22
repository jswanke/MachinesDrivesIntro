import numpy as np
import matplotlib.pyplot as plt

# --- Configuration ---
S = 12          # Number of slots
p = 1           # 2 poles
slot_pitch_deg = 360 / S 

# Short pitch: 5 slots (150 electrical degrees)
coil_pitch_slots = 5
gamma_deg = coil_pitch_slots * slot_pitch_deg

theta = np.linspace(0, 360, 1000)

def get_true_winding_function(pitch_slots):
    """Calculates MMF by integrating current distribution (steps at slots)."""
    # Initialize current density (impulses at slots)
    current_dist = np.zeros(S)
    
    # Phase A: q=2 (Slots 1 and 2)
    # Go sides (+1) at slots 0 and 1
    # Return sides (-1) at slots (0+pitch) and (1+pitch)
    current_dist[0] = 1
    current_dist[1] = 1
    current_dist[(0 + pitch_slots) % S] -= 1
    current_dist[(1 + pitch_slots) % S] -= 1
    
    # Integrate to get winding function (staircase)
    # We repeat the slots to handle the circularity and then find the mean
    wf_steps = np.cumsum(current_dist)
    wf_steps -= np.mean(wf_steps) # Remove DC offset
    
    # Map slot steps to the continuous theta array
    wf_continuous = np.zeros_like(theta)
    for i in range(S):
        mask = (theta >= i * slot_pitch_deg) & (theta < (i + 1) * slot_pitch_deg)
        wf_continuous[mask] = wf_steps[i]
    return wf_continuous

wf_full = get_true_winding_function(6)     # 6 slots = 180 deg
wf_short = get_true_winding_function(5)    # 5 slots = 150 deg

# --- Plotting ---
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

# Subplot 1: Corrected Winding Functions
ax1.step(theta, wf_full, label='Full Pitch (180°)', where='post', alpha=0.6, linestyle='--')
ax1.step(theta, wf_short, label=f'Short Pitch ({gamma_deg}°)', color='red', where='post', linewidth=2)

# Coil Markers (Go = Blue, Return = White/Blue)
ax1.scatter([0, 30], [0, 0], color='blue', s=100, label='Phase A+ (Go)', zorder=5)
ax1.scatter([0 + gamma_deg, 30 + gamma_deg], [0, 0], facecolors='none', 
            edgecolors='blue', s=100, linewidth=2, label='Phase A- (Return)', zorder=5)

ax1.set_title('Corrected MMF Winding Function (Staircase Waveform)')
ax1.set_ylabel('Winding Function $w(\phi)$')
ax1.set_xticks(np.arange(0, 361, 30))
ax1.grid(True, linestyle=':', alpha=0.6)
ax1.legend()

# Subplot 2: FFT Comparison
N = len(wf_short)
fft_full = np.abs(np.fft.rfft(wf_full)) / (N / 2)
fft_short = np.abs(np.fft.rfft(wf_short)) / (N / 2)
harmonics = np.arange(1, 15)

width = 0.35
ax2.bar(harmonics - width/2, fft_full[1:15], width, label='Full Pitch')
ax2.bar(harmonics + width/2, fft_short[1:15], width, label='Short Pitch', color='red')

ax2.set_title('Harmonic Magnitude Comparison')
ax2.set_xticks(harmonics)
ax2.set_ylabel('Magnitude')
ax2.legend()

plt.tight_layout()
plt.show()