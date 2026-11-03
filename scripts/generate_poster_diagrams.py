import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

out_dir = r"E:\weather predection\static\poster_assets"
os.makedirs(out_dir, exist_ok=True)

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']

# ==============================================================================
# Fig 1: System Architecture Diagram
# ==============================================================================
fig, ax = plt.subplots(figsize=(7.5, 4.4), dpi=300)
ax.set_facecolor('#F8FAFC')
fig.patch.set_facecolor('#F8FAFC')

# Helper to draw rounded rectangle box
def draw_box(ax, x, y, w, h, bg, border, title, items=[], radius=0.08, title_bg=None, title_color='#0F172A'):
    # main box
    rect = patches.FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad={radius}", ec=border, fc=bg, lw=1.5)
    ax.add_patch(rect)
    
    # header banner if requested
    if title_bg:
        th = 0.22 * h
        t_rect = patches.FancyBboxPatch((x, y + h - th), w, th, boxstyle=f"round,pad={radius}", ec=title_bg, fc=title_bg, lw=1)
        ax.add_patch(t_rect)
        ax.text(x + w/2, y + h - th/2, title, ha='center', va='center', fontsize=8.5, fontweight='bold', color='#FFFFFF')
        curr_y = y + h - th - 0.12
    else:
        ax.text(x + w/2, y + h - 0.15, title, ha='center', va='top', fontsize=8.5, fontweight='bold', color=title_color)
        curr_y = y + h - 0.42

    for itm in items:
        ax.text(x + w/2, curr_y, itm, ha='center', va='top', fontsize=7.2, color='#334155')
        curr_y -= 0.26

# Helper for arrow
def draw_arrow(ax, x1, y1, x2, y2, color='#475569', label=''):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(facecolor=color, edgecolor=color, width=1.5, headwidth=6, headlength=6, shrink=0.05))
    if label:
        ax.text((x1+x2)/2, (y1+y2)/2 + 0.08, label, ha='center', va='bottom', fontsize=6.8, fontweight='bold', color=color)

# Column 1: SENSING (Blue)
ax.text(1.2, 4.15, "SENSING LAYER", ha='center', va='center', fontsize=9, fontweight='bold', color='#1E40AF')
draw_box(ax, 0.2, 2.7, 2.0, 1.25, '#EFF6FF', '#3B82F6', "Bosch BMP280", ["Barometric Pressure", "High-res Temp", "I²C (A4 / A5)"])
draw_box(ax, 0.2, 1.2, 2.0, 1.25, '#EFF6FF', '#3B82F6', "Sensirion DHT11", ["Relative Humidity", "Ambient Temp", "1-Wire (Pin D2)"])

# Column 2: EDGE CONTROLLER & GATEWAY (Green)
ax.text(3.7, 4.15, "EDGE ACQUISITION & GATEWAY", ha='center', va='center', fontsize=9, fontweight='bold', color='#065F46')
draw_box(ax, 2.7, 2.7, 2.0, 1.25, '#ECFDF5', '#10B981', "Arduino Uno R3", ["Sensor Ingestion", "Dew Point Sanity", "UART 115200 Baud"])
draw_box(ax, 2.7, 1.2, 2.0, 1.25, '#ECFDF5', '#10B981', "ESP32 Gateway", ["Dual-Core MCU", "NTP Time Sync", "120-Pkt RAM Buffer", "Wi-Fi HTTP Client"])

# Arrows from Sensing to Uno
draw_arrow(ax, 2.2, 3.32, 2.7, 3.32, '#2563EB', 'I²C')
draw_arrow(ax, 2.2, 1.82, 2.7, 2.9, '#2563EB', '1-Wire')

# Arrow Uno to ESP32
draw_arrow(ax, 3.7, 2.7, 3.7, 2.45, '#059669', 'Direct UART (TX->RX2)')

# Column 3: BACKEND AI ENGINE (Purple)
ax.text(6.2, 4.15, "DJANGO AI BACKEND", ha='center', va='center', fontsize=9, fontweight='bold', color='#5B21B6')
draw_box(ax, 5.2, 2.3, 2.0, 1.65, '#F5F3FF', '#8B5CF6', "AI Forecast Engine", [
    "Django 5 REST API", 
    "Quantile Boosters", 
    "P10 / P50 / P90 Horiz.",
    "Nightly Retraining",
    "33k ERA5 Archive"
])

# Arrow ESP32 to Django
draw_arrow(ax, 4.7, 1.82, 5.2, 2.8, '#059669', 'Wi-Fi HTTP POST')

# Row Bottom: DISASTER & ALERT ENGINE (Red / Amber)
ax.text(3.7, 0.95, "EXTREME HAZARD ENGINE & DISPATCH", ha='center', va='center', fontsize=8.5, fontweight='bold', color='#991B1B')
draw_box(ax, 0.5, 0.1, 1.9, 0.72, '#FEF2F2', '#EF4444', "ΔP / 3h Baro Drop", ["Severe Threshold < -3.5 hPa"])
draw_box(ax, 2.7, 0.1, 2.0, 0.72, '#FEF2F2', '#EF4444', "Disaster Catalogs", ["2015 Floods, Vardah, Michaung"])
draw_box(ax, 5.0, 0.1, 2.2, 0.72, '#FEF3C7', '#F59E0B', "Alert Dispatchers", ["Telegram, SMS, Email, Web UI"])

draw_arrow(ax, 2.4, 0.46, 2.7, 0.46, '#DC2626')
draw_arrow(ax, 4.7, 0.46, 5.0, 0.46, '#DC2626')
draw_arrow(ax, 6.2, 2.3, 6.2, 0.85, '#7C3AED', 'Hazard Eval')

ax.set_xlim(-0.1, 7.5)
ax.set_ylim(-0.05, 4.45)
ax.axis('off')

plt.tight_layout()
fig1_path = os.path.join(out_dir, "fig1_system_architecture.png")
plt.savefig(fig1_path, bbox_inches='tight', dpi=300)
plt.close()
print("Saved:", fig1_path)

# ==============================================================================
# Fig 2: Circuit Diagram & Wiring Schematic
# ==============================================================================
fig, ax = plt.subplots(figsize=(7.5, 4.4), dpi=300)
ax.set_facecolor('#FFFFFF')
fig.patch.set_facecolor('#FFFFFF')

# Microcontroller Boxes
rect_uno = patches.FancyBboxPatch((0.4, 1.0), 2.2, 3.0, boxstyle="round,pad=0.08", ec='#1E3A8A', fc='#DBEAFE', lw=2)
ax.add_patch(rect_uno)
ax.text(1.5, 3.75, "Arduino Uno R3\n(ATmega328P)", ha='center', va='center', fontsize=8.5, fontweight='bold', color='#1E3A8A')

rect_esp = patches.FancyBboxPatch((4.8, 1.0), 2.2, 3.0, boxstyle="round,pad=0.08", ec='#065F46', fc='#D1FAE5', lw=2)
ax.add_patch(rect_esp)
ax.text(5.9, 3.75, "ESP32 DevKit V1\n(Wi-Fi Gateway)", ha='center', va='center', fontsize=8.5, fontweight='bold', color='#065F46')

# Sensors on the far left
rect_bmp = patches.FancyBboxPatch((-1.6, 2.7), 1.6, 1.2, boxstyle="round,pad=0.06", ec='#64748B', fc='#F1F5F9', lw=1.2)
ax.add_patch(rect_bmp)
ax.text(-0.8, 3.65, "Bosch BMP280", ha='center', va='top', fontsize=8, fontweight='bold', color='#0F172A')
ax.text(-0.8, 3.35, "VCC  GND\nSCL  SDA", ha='center', va='top', fontsize=7, color='#475569')

rect_dht = patches.FancyBboxPatch((-1.6, 1.1), 1.6, 1.2, boxstyle="round,pad=0.06", ec='#64748B', fc='#F1F5F9', lw=1.2)
ax.add_patch(rect_dht)
ax.text(-0.8, 2.05, "DHT11 (3-Pin)", ha='center', va='top', fontsize=8, fontweight='bold', color='#0F172A')
ax.text(-0.8, 1.75, "VCC (+)\nDATA (OUT)\nGND (-)", ha='center', va='top', fontsize=7, color='#475569')

# Draw Connections: BMP280 to Uno
ax.plot([-0.1, 0.4], [3.2, 3.2], color='#2563EB', lw=1.5) # SCL -> A5
ax.text(0.15, 3.25, "SCL->A5", fontsize=6.5, color='#2563EB', ha='center')

ax.plot([-0.1, 0.4], [3.0, 3.0], color='#0284C7', lw=1.5) # SDA -> A4
ax.text(0.15, 3.05, "SDA->A4", fontsize=6.5, color='#0284C7', ha='center')

# Draw Connections: DHT11 to Uno
ax.plot([-0.1, 0.4], [1.6, 1.6], color='#16A34A', lw=1.5) # DATA -> D2
ax.text(0.15, 1.65, "DATA->D2", fontsize=6.5, color='#16A34A', ha='center')

# Power rails left
ax.plot([-0.1, 0.4], [3.4, 3.4], color='#DC2626', lw=1.5) # 3.3V
ax.plot([-0.1, 0.4], [1.9, 1.9], color='#EA580C', lw=1.5) # 5V
ax.plot([-0.1, 0.4], [1.3, 1.3], color='#1E293B', lw=1.5) # GND

# Inter-MCU Connections (Direct UART)
# Pin 1 TX to GPIO16 RX2
ax.annotate('', xy=(4.8, 2.9), xytext=(2.6, 2.9),
            arrowprops=dict(facecolor='#2563EB', edgecolor='#2563EB', width=1.8, headwidth=6, shrink=0.02))
ax.text(3.7, 3.02, "Pin 1 (TX)  -->  GPIO 16 (RX2)\n[Direct Wire, No Divider]", ha='center', va='bottom', fontsize=7.2, fontweight='bold', color='#1E40AF')

# Pin 0 RX to GPIO17 TX2
ax.annotate('', xy=(2.6, 2.3), xytext=(4.8, 2.3),
            arrowprops=dict(facecolor='#0284C7', edgecolor='#0284C7', width=1.5, headwidth=6, shrink=0.02))
ax.text(3.7, 2.38, "Pin 0 (RX)  <--  GPIO 17 (TX2)", ha='center', va='bottom', fontsize=7.0, color='#0284C7')

# Common Ground Line
ax.plot([2.6, 4.8], [1.4, 1.4], color='#0F172A', lw=2.2, linestyle='-')
ax.text(3.7, 1.5, "Common Ground Rail (GND <--> GND)", ha='center', va='bottom', fontsize=7.2, fontweight='bold', color='#0F172A')

# Wi-Fi Output from ESP32
rect_wifi = patches.FancyBboxPatch((7.6, 2.0), 1.6, 1.4, boxstyle="round,pad=0.06", ec='#8B5CF6', fc='#F5F3FF', lw=1.5)
ax.add_patch(rect_wifi)
ax.text(8.4, 3.1, "Django Server", ha='center', va='top', fontsize=8, fontweight='bold', color='#6D28D9')
ax.text(8.4, 2.7, "LAN: Port 8000\nREST API\nNTP Sync :123", ha='center', va='top', fontsize=7, color='#475569')

draw_arrow(ax, 7.0, 2.7, 7.6, 2.7, '#7C3AED', 'Wi-Fi')

# Legend at bottom
ax.text(3.7, 0.45, "— Signal Line    — 5V / 3.3V Rail    — Common Ground    ... Wi-Fi 2.4GHz", ha='center', va='center', fontsize=7.5, color='#334155',
        bbox=dict(boxstyle="round,pad=0.3", fc="#F8FAFC", ec="#CBD5E1", lw=1))

ax.set_xlim(-1.9, 9.4)
ax.set_ylim(0.2, 4.3)
ax.axis('off')

plt.tight_layout()
fig2_path = os.path.join(out_dir, "fig2_circuit_diagram.png")
plt.savefig(fig2_path, bbox_inches='tight', dpi=300)
plt.close()
print("Saved:", fig2_path)

# ==============================================================================
# Fig 3: Prototype Layout & Physical Station Setup
# ==============================================================================
fig, ax = plt.subplots(figsize=(7.5, 4.4), dpi=300)
ax.set_facecolor('#F1F5F9')
fig.patch.set_facecolor('#F1F5F9')

# Draw Station Mast / Enclosure representation
# Mast pole
ax.plot([4.2, 4.2], [0.3, 3.9], color='#475569', lw=6)
# Crossbar
ax.plot([2.0, 6.4], [3.3, 3.3], color='#475569', lw=4)

# 1. Stevenson Screen (Enclosure)
rect_screen = patches.FancyBboxPatch((1.0, 2.3), 2.2, 1.6, boxstyle="round,pad=0.08", ec='#1E3A8A', fc='#FFFFFF', lw=2)
ax.add_patch(rect_screen)
# Slats
for y_s in [2.6, 2.9, 3.2, 3.5]:
    ax.plot([1.2, 3.0], [y_s, y_s], color='#94A3B8', lw=1.5)
ax.text(2.1, 2.45, "Stevenson Screen", ha='center', va='center', fontsize=7.5, fontweight='bold', color='#1E3A8A')

# 2. BMP280 chamber & 3. DHT11 port inside/adjacent
rect_bmp_int = patches.FancyBboxPatch((1.3, 2.8), 0.6, 0.5, boxstyle="round,pad=0.02", ec='#3B82F6', fc='#DBEAFE', lw=1)
ax.add_patch(rect_bmp_int)
ax.text(1.6, 3.05, "BMP", fontsize=6, fontweight='bold', ha='center', va='center', color='#1E40AF')

rect_dht_int = patches.FancyBboxPatch((2.2, 2.8), 0.6, 0.5, boxstyle="round,pad=0.02", ec='#10B981', fc='#D1FAE5', lw=1)
ax.add_patch(rect_dht_int)
ax.text(2.5, 3.05, "DHT", fontsize=6, fontweight='bold', ha='center', va='center', color='#065F46')

# Electronics Box (Uno + ESP32) mounted lower on mast
rect_box = patches.FancyBboxPatch((3.2, 1.0), 2.0, 1.5, boxstyle="round,pad=0.08", ec='#334155', fc='#E2E8F0', lw=2)
ax.add_patch(rect_box)
ax.text(4.2, 2.2, "MCU Gateway Enclosure", ha='center', va='center', fontsize=7.5, fontweight='bold', color='#0F172A')

rect_u = patches.FancyBboxPatch((3.4, 1.2), 0.7, 0.7, boxstyle="round,pad=0.03", ec='#1E40AF', fc='#93C5FD', lw=1)
ax.add_patch(rect_u)
ax.text(3.75, 1.55, "Uno", fontsize=6.5, fontweight='bold', ha='center', va='center', color='#1E3A8A')

rect_e = patches.FancyBboxPatch((4.3, 1.2), 0.7, 0.7, boxstyle="round,pad=0.03", ec='#065F46', fc='#6EE7B7', lw=1)
ax.add_patch(rect_e)
ax.text(4.65, 1.55, "ESP32", fontsize=6.5, fontweight='bold', ha='center', va='center', color='#065F46')

# Antenna on ESP32
ax.plot([4.65, 4.65], [1.9, 2.6], color='#047857', lw=2)
ax.plot([4.5, 4.8], [2.6, 2.6], color='#047857', lw=2)

# Power & USB Base (7)
rect_pwr = patches.FancyBboxPatch((3.5, 0.2), 1.4, 0.6, boxstyle="round,pad=0.04", ec='#D97706', fc='#FEF3C7', lw=1.5)
ax.add_patch(rect_pwr)
ax.text(4.2, 0.5, "Power & USB Bridge", ha='center', va='center', fontsize=6.5, fontweight='bold', color='#B45309')

# Numbered Callouts (1 to 7) matching template style exactly:
# Template has numbered circles 1..7
callouts = [
    (1, 1.0, 3.8, "1", "Solar-shielded Screen"),
    (2, 1.6, 3.4, "2", "BMP280 Baro Chamber"),
    (3, 2.5, 3.4, "3", "DHT11 Humidity Port"),
    (4, 3.75, 0.9, "4", "Arduino Uno MCU"),
    (5, 4.9, 1.55, "5", "ESP32 Gateway"),
    (6, 4.2, 4.1, "6", "Poonamallee Mast"),
    (7, 4.2, 0.05, "7", "Power & Telemetry")
]

for num, cx, cy, label, desc in callouts:
    # circular badge
    circle = patches.Circle((cx, cy), 0.16, fc='#DC2626' if num in [1,6] else '#1E40AF', ec='#FFFFFF', lw=1.5, zorder=10)
    ax.add_patch(circle)
    ax.text(cx, cy, label, ha='center', va='center', color='#FFFFFF', fontsize=7.5, fontweight='bold', zorder=11)

# Caption box at right side
desc_text = (
    "Layout Callouts:\n"
    "① Stevenson louvered shelter\n"
    "② Bosch BMP280 baro chamber\n"
    "③ Sensirion DHT11 intake port\n"
    "④ Arduino Uno R3 A/D sampler\n"
    "⑤ ESP32 Wi-Fi gateway (UART)\n"
    "⑥ Poonamallee mounting mast\n"
    "⑦ Regulated power / USB link"
)
ax.text(6.0, 2.1, desc_text, ha='left', va='center', fontsize=7.2, color='#1E293B',
        bbox=dict(boxstyle="round,pad=0.4", fc="#FFFFFF", ec="#CBD5E1", lw=1))

ax.set_xlim(0.2, 7.8)
ax.set_ylim(-0.15, 4.4)
ax.axis('off')

plt.tight_layout()
fig3_path = os.path.join(out_dir, "fig3_prototype_design.png")
plt.savefig(fig3_path, bbox_inches='tight', dpi=300)
plt.close()
print("Saved:", fig3_path)
