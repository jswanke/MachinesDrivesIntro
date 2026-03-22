import numpy as np
import matplotlib.pyplot as plt

S = 12          # Number of slots
p=1
slot_pitch_deg = 360 / S  # 30 degrees per slot

# Coil Location Tracker
coil_full = np.zeros(S)
coil_pitch = np.zeros(S)
coil_distr = np.zeros(S)

# place coils
coil_full[0] = 1
coil_full[6] = -1

# coil_pitch[1] = 1
# coil_pitch[5] = -1
# coil_pitch[7] = -1
# coil_pitch[11] = 1

coil_pitch[0] = 1
coil_pitch[5] = -1
coil_pitch[6] = -1
coil_pitch[11] = 1

coil_distr[0] = 1/3
coil_distr[1] = 1/3
coil_distr[2] = 1/3
# coil_distr[3] = 1/4
coil_distr[6] = -1/3
coil_distr[7] = -1/3
coil_distr[8] = -1/3
# coil_distr[9] = -1/4

theta = np.linspace(0, 360, 1000)

def getWF(coil_placement):
    wf = np.zeros_like(theta)
    for ii in range(len(theta)):
        index = int(np.floor(theta[ii] / slot_pitch_deg))
        if index == S: index = 0
        if ii > 0:
            wf[ii] = wf[ii-1] + coil_placement[index]
        else:
            wf[ii] = coil_placement[index]

    return wf - np.mean(wf)

def getWF_alt(coil_placement):
    wf = np.zeros_like(theta)
    for ii in range(len(coil_placement)):
        start_angle = ii*slot_pitch_deg
        pulse = coil_placement[ii] * np.where(theta > start_angle, 1, 0)
        wf += pulse

    return wf - np.mean(wf)

wf_full = getWF_alt(2*coil_full)
wf_short = getWF_alt(coil_pitch)
wf_dist = getWF_alt(2*coil_distr)

# --- Plotting ---
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 7))

# Subplot 1: Winding Function with Coil Markers
ax1.step(theta, wf_full, label='Full Pitch (180°)', alpha=0.5, color='blue', linestyle='--')
# ax1.step(theta, wf_short, label=f'Short Pitch', color='red', where='post', linewidth=2)
ax1.step(theta, wf_dist, label=f'Distributed', color='green', where='post', linewidth=2)

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
fft_dist = np.abs(np.fft.rfft(wf_dist)) / (N / 2)
harmonics = np.arange(1, 15)

width = 0.35
ax2.bar(harmonics - width/2, fft_full[1:15], width, label='Full Pitch')
# ax2.bar(harmonics + width/2, fft_short[1:15], width, label='Short Pitch', color='red')
ax2.bar(harmonics + width/2, fft_dist[1:15], width, label='Distributed', color='green')

ax2.set_title('Harmonic Magnitude Comparison')
ax2.set_xlabel('Harmonic Order')
ax2.set_ylabel('Amplitude')
ax2.set_xticks(harmonics)
ax2.grid(axis='y', linestyle='--', alpha=0.7)
ax2.legend()

plt.tight_layout()
plt.show()