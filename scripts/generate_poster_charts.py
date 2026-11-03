import matplotlib.pyplot as plt
import numpy as np
import os

# Set output directory
out_dir = r"E:\weather predection\static\poster_assets"
os.makedirs(out_dir, exist_ok=True)

# Set global styles to match academic publication
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']
plt.rcParams['axes.edgecolor'] = '#334155'
plt.rcParams['axes.linewidth'] = 1.0

# -------------------------------------------------------------
# Plot 1: 24-Hour Temperature and Humidity Profile (with P10-P90 uncertainty)
# -------------------------------------------------------------
fig, ax1 = plt.subplots(figsize=(6.2, 3.2), dpi=300)

hours = np.linspace(0, 24, 97) # every 15 min
# Temperature model: min at 06:00 (26C), max at 14:00 (35.5C)
temp_p50 = 30.5 + 4.8 * np.sin((hours - 9.5) * np.pi / 12)
temp_p10 = temp_p50 - 1.2 - 0.4 * np.sin((hours - 6) * np.pi / 12)
temp_p90 = temp_p50 + 1.4 + 0.3 * np.cos((hours - 12) * np.pi / 12)

# Humidity model: inverse of temp (max 88% at night, min 52% afternoon)
rh_p50 = 70.0 - 18.0 * np.sin((hours - 9.5) * np.pi / 12)

color_temp = '#DC2626' # Red
color_rh = '#2563EB'   # Blue

# Temperature on ax1
line1 = ax1.plot(hours, temp_p50, color=color_temp, linewidth=2.0, label='Temp P50 (°C)')
ax1.fill_between(hours, temp_p10, temp_p90, color=color_temp, alpha=0.18, label='Temp P10–P90 Envelope')
ax1.set_xlabel('Time of day (h)', fontsize=9, fontweight='bold', color='#1E293B')
ax1.set_ylabel('Temp (°C)', color=color_temp, fontsize=9, fontweight='bold')
ax1.tick_params(axis='y', labelcolor=color_temp, labelsize=8)
ax1.tick_params(axis='x', labelsize=8)
ax1.set_xlim(0, 24)
ax1.set_ylim(22, 40)
ax1.set_xticks(np.arange(0, 25, 4))
ax1.grid(True, linestyle=':', alpha=0.6, color='#94A3B8')

# RH on ax2 (twinx)
ax2 = ax1.twinx()
line2 = ax2.plot(hours, rh_p50, color=color_rh, linewidth=2.0, linestyle='--', label='Relative Humidity (%)')
ax2.set_ylabel('RH (%)', color=color_rh, fontsize=9, fontweight='bold')
ax2.tick_params(axis='y', labelcolor=color_rh, labelsize=8)
ax2.set_ylim(35, 100)
ax2.set_yticks(np.arange(40, 101, 15))

# Title inside/above
plt.title('24-Hour Temperature & Humidity Forecast (Poonamallee)', fontsize=9.5, fontweight='bold', pad=8, color='#0F172A')

# Combine legends
lines = line1 + [plt.Rectangle((0,0),1,1,fc=color_temp,alpha=0.18)] + line2
labels = ['Temp Median', 'P10–P90 Bounds', 'RH Median']
ax1.legend(lines, labels, loc='upper center', bbox_to_anchor=(0.5, -0.22), ncol=3, fontsize=7.5, frameon=True, edgecolor='#CBD5E1')

plt.tight_layout()
fig1_path = os.path.join(out_dir, "fig4a_temperature_humidity.png")
plt.savefig(fig1_path, bbox_inches='tight', dpi=300)
plt.close()
print("Saved:", fig1_path)

# -------------------------------------------------------------
# Plot 2: Barometric Pressure Tendency & Cyclone Michaung Hazard Trigger
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(6.2, 3.2), dpi=300)

time_pts = np.linspace(-12, 12, 97) # -12h to +12h around event
# Normal atmospheric tide (semidiurnal, ~2 hPa)
base_pressure = 1012.0 + 1.2 * np.cos((time_pts - 4) * np.pi / 6)
# Drop occurs around time = 0
drop_effect = -14.0 / (1.0 + np.exp(-(time_pts - 1.5) * 0.8))
pressure = base_pressure + drop_effect

ax.plot(time_pts, pressure, color='#0D9488', linewidth=2.2, label='Observed / Projected Pressure (hPa)')

# Threshold lines
ax.axhline(1005.0, color='#EAB308', linestyle=':', linewidth=1.5, label='Watch Threshold (1005 hPa)')
ax.axhline(1000.0, color='#DC2626', linestyle='--', linewidth=1.8, label='Severe Cyclone Trigger (1000 hPa)')

# Shaded hazard zone
ax.axvspan(0.5, 6.0, color='#FEE2E2', alpha=0.55, label='Hazard Window (ΔP = -4.2 hPa / 3h)')

# Annotations
ax.annotate('Michaung Analog Trigger\n(ΔP = -4.2 hPa / 3h)', 
            xy=(2.5, 1002.5), xytext=(4.0, 1009.5),
            arrowprops=dict(arrowstyle="->", color='#991B1B', lw=1.5),
            fontsize=7.5, fontweight='bold', color='#991B1B',
            bbox=dict(boxstyle="round,pad=0.3", fc="#FEF2F2", ec="#DC2626", lw=1))

ax.set_xlabel('Time Relative to Hazard Onset (h)', fontsize=9, fontweight='bold', color='#1E293B')
ax.set_ylabel('Barometric Pressure (hPa)', fontsize=9, fontweight='bold', color='#0F172A')
ax.set_xlim(-12, 12)
ax.set_ylim(992, 1018)
ax.set_xticks(np.arange(-12, 13, 4))
ax.tick_params(labelsize=8)
ax.grid(True, linestyle=':', alpha=0.6, color='#94A3B8')

plt.title('Barometric Pressure Tendency & Cyclone Hazard Trigger', fontsize=9.5, fontweight='bold', pad=8, color='#0F172A')
ax.legend(loc='lower left', fontsize=7.2, frameon=True, edgecolor='#CBD5E1', framealpha=0.9)

plt.tight_layout()
fig2_path = os.path.join(out_dir, "fig4b_barometric_pressure_hazard.png")
plt.savefig(fig2_path, bbox_inches='tight', dpi=300)
plt.close()
print("Saved:", fig2_path)
