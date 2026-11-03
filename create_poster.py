"""
ACADEMIC RESEARCH POSTER - PIXEL-PERFECT, ZERO-OVERLAP, EXACT-ALIGNED GENERATOR
AI-Based Local Weather Forecasting and Prediction System Using Arduino Uno and ESP32
Canvas: A0 Landscape 33.11" x 23.39"
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

W = 33.11
H = 23.39

prs = Presentation()
prs.slide_width  = Inches(W)
prs.slide_height = Inches(H)
slide = prs.slides.add_slide(prs.slide_layouts[6])

# ── Color Palette ─────────────────────────────────────────────────────────────
NAVY    = RGBColor(0x0D, 0x2B, 0x55)
MIDBLUE = RGBColor(0x1A, 0x5F, 0xA8)
LTBLUE  = RGBColor(0xD6, 0xE8, 0xF7)
TEAL    = RGBColor(0x00, 0x7B, 0x83)
WHITE   = RGBColor(0xFF, 0xFF, 0xFF)
BLACK   = RGBColor(0x0D, 0x0D, 0x0D)
LGRAY   = RGBColor(0xF2, 0xF5, 0xF8)
DGRAY   = RGBColor(0xC4, 0xD0, 0xDC)
GREEN   = RGBColor(0x13, 0x7A, 0x2B)

BASE        = r"e:\weather predection\static\poster_assets"
IMG_ARCH    = os.path.join(BASE, "fig1_system_architecture.png")
IMG_CIRCUIT = os.path.join(BASE, "fig2_circuit_diagram.png")
IMG_PROTO   = os.path.join(BASE, "fig3_prototype_design.png")
IMG_RESULTS = os.path.join(BASE, "fig4_results_combined.png")

# ── Typography & Sizing Standards ─────────────────────────────────────────────
FS_SECTION  = 13.5
FS_BODY     = 11.2
FS_BODY_SM  = 10.6
FS_TBL_HDR  = 10.5
FS_TBL_BODY = 10.0
FS_CAPTION  = 9.5
FS_FOOTER   = 10.5

SH_H  = 0.42          # Section header strip height
SH_DY = 0.46          # Advance after section header

ROW_H_HDR  = 0.36     # Table header row height
ROW_H_BODY = 0.38     # Table body row height

SP_BODY = Pt(5)       # Spacing between body paragraphs
SP_LIST = Pt(6)       # Spacing between list items
SP_REF  = Pt(5)       # Spacing between reference lines

# ── Layout Primitives ─────────────────────────────────────────────────────────

def R(x, y, w, h, fill=None, line=None, lw=0.4):
    shp = slide.shapes.add_shape(1, Inches(x), Inches(y), Inches(w), Inches(h))
    if fill:
        shp.fill.solid()
        shp.fill.fore_color.rgb = fill
    else:
        shp.fill.background()
    if line:
        shp.line.color.rgb = line
        shp.line.width = Pt(lw)
    else:
        shp.line.fill.background()
    return shp

def T(text, x, y, w, h, sz=FS_BODY, bold=False, italic=False, col=BLACK, align=PP_ALIGN.LEFT):
    txb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = txb.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.04)
    tf.margin_right = Inches(0.04)
    tf.margin_top = Inches(0.02)
    tf.margin_bottom = Inches(0.02)
    p = tf.paragraphs[0]
    p.alignment = align
    r = p.add_run()
    r.text = text
    r.font.size = Pt(sz)
    r.font.bold = bold
    r.font.italic = italic
    r.font.color.rgb = col
    return txb

def ML(lines, x, y, w, h, sz=FS_BODY, col=BLACK, sp=SP_BODY):
    txb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = txb.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.04)
    tf.margin_right = Inches(0.04)
    tf.margin_top = Inches(0.02)
    tf.margin_bottom = Inches(0.02)
    for i, ln in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = PP_ALIGN.LEFT
        p.space_after = sp
        r = p.add_run()
        r.text = ln
        r.font.size = Pt(sz)
        r.font.color.rgb = col
    return txb

def MIXED_LIST(items, x, y, w, h, sz=FS_BODY_SM, sp=SP_LIST):
    txb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = txb.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.04)
    tf.margin_right = Inches(0.04)
    tf.margin_top = Inches(0.02)
    tf.margin_bottom = Inches(0.02)
    for i, (kw, body) in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_after = sp
        if kw:
            r1 = p.add_run()
            r1.text = kw + "  "
            r1.font.bold = True
            r1.font.size = Pt(sz)
            r1.font.color.rgb = MIDBLUE
        r2 = p.add_run()
        r2.text = body
        r2.font.size = Pt(sz)
        r2.font.color.rgb = BLACK
    return txb

def SH(title, x, y, w):
    R(x, y, w, SH_H, fill=MIDBLUE)
    T(title, x + 0.08, y + 0.04, w - 0.16, SH_H - 0.08,
      sz=FS_SECTION, bold=True, col=WHITE)

def IMG(path, x, y, w, h):
    slide.shapes.add_picture(path, Inches(x), Inches(y), Inches(w), Inches(h))

# ── Background ────────────────────────────────────────────────────────────────
R(0, 0, W, H, fill=LGRAY)

# ── Header Banner ─────────────────────────────────────────────────────────────
HDR = 2.40
R(0, 0,        W, HDR,  fill=NAVY)
R(0, 0,        W, 0.12, fill=TEAL)
R(0, HDR-0.12, W, 0.12, fill=TEAL)

T("AI-Based Local Weather Forecasting and Prediction System Using Arduino Uno and ESP32",
  0.30, 0.16, W - 0.60, 0.95, sz=42, bold=True, col=WHITE, align=PP_ALIGN.CENTER)

T("Modular Dual-Microcontroller Edge-Server Architecture  |  SGD Classifier  |  "
  "Real-Time Inference (<15 ms)  |  Continual Self-Learning  |  Open-Meteo Historical Training Data",
  0.30, 1.15, W - 0.60, 0.44, sz=17, italic=True, col=LTBLUE, align=PP_ALIGN.CENTER)

T("Balavignesh K  (E0225002)   |   Sudharsan N  (E0225010)",
  0.30, 1.62, W - 0.60, 0.36, sz=16, bold=True, col=WHITE, align=PP_ALIGN.CENTER)

T("B.Tech - Computer Science & Engineering (Cyber Security & Internet of Things)   |   "
  "Sri Ramachandra Faculty of Engineering and Technology, SRIHER, Porur, Chennai - 600116   |   September, 2026",
  0.30, 2.00, W - 0.60, 0.32, sz=12.0, col=LTBLUE, align=PP_ALIGN.CENTER)

# ── Column Geometry (5-Column Grid, Perfectly Aligned) ────────────────────────
TOP = HDR + 0.22      # 2.62 in
BOT = H - 0.44        # 22.95 in
COL_H = BOT - TOP     # 20.33 in
LM  = 0.24
GAP = 0.17
PAD = 0.10

C1x, C1w = LM,          5.45
C2x, C2w = C1x+C1w+GAP, 5.45
C3x, C3w = C2x+C2w+GAP, 6.70
C4x, C4w = C3x+C3w+GAP, 7.00
C5x, C5w = C4x+C4w+GAP, W - (C4x+C4w+GAP) - LM   # 6.99 in

for cx, cw in [(C1x,C1w),(C2x,C2w),(C3x,C3w),(C4x,C4w),(C5x,C5w)]:
    R(cx, TOP, cw, COL_H, fill=WHITE, line=DGRAY, lw=0.35)

# ═══════════════════════════════════════════════════════════════════════════════
# COLUMN 1: Abstract | Need for Study | Problem Statement | Objectives | References
# ═══════════════════════════════════════════════════════════════════════════════
y = TOP + 0.05

SH("Abstract", C1x, y, C1w); y += SH_DY
ML([
    "The reason behind the development of this AI-based weather prediction system is the failure "
    "of generic weather apps to catch localized microclimates and neighborhood rainfall storms. "
    "Standard mobile weather services pull their data from regional airports spanning 15 to 25 "
    "kilometers away, averaging out the acute barometric pressure drops and humidity spikes that "
    "signal approaching precipitation. Most internet-reliant weather devices also fail during "
    "intense storms when local cell towers cut out.",

    "An Arduino Uno samples temperature and relative humidity (DHT11) plus barometric pressure "
    "(Bosch BMP280, I2C, 16x oversampling) every 60 s. The ESP32 gateway adds NTP IST timestamps "
    "and Wi-Fi RSSI, then forwards enriched packets via HTTP POST to a Django REST API backend "
    "(port 8000). A 120-record FIFO offline buffer ensures zero data loss during network drops.",

    "The Django backend auto-computes fused temperature (arithmetic mean of BMP280 and DHT11), "
    "NOAA Heat Index, Magnus-Tetens Dew Point, and 3-hour barometric pressure trend per reading. "
    "A 24-hour circular history (1,440 samples) feeds delta-P_3h, delta-P_6h, delta-RH_3h into an "
    "SGDClassifier - forecasting Clear, Cloudy, or Rain in under 15 ms. Multi-channel hazard alerts "
    "(Telegram Bot, Mobile Browser Push, Email) fire automatically against Chennai historical "
    "disaster signatures. The system self-recalibrates every 6 hours via model.partial_fit().",
], C1x+PAD, y, C1w-PAD*2, 5.00, sz=FS_BODY, sp=SP_BODY); y += 5.10

SH("Need for the Study", C1x, y, C1w); y += SH_DY
ML([
    "Accurate local weather prediction is critical for communities and outdoor operations. "
    "Traditional forecasting relies on NWP models running on macro-scale supercomputers that "
    "divide the atmosphere into 15-25 km grids - consistently failing to capture sharp, localised "
    "microclimate changes such as afternoon convective cloudbursts or sudden humidity spikes.",

    "Modern connected weather stations depend entirely on third-party cloud platforms. During "
    "severe storms, broadband internet and cellular towers frequently experience outages - "
    "cloud-dependent systems become completely unusable precisely when needed most. An intelligent "
    "edge-server architecture ensures that ML inference and predictive alerts function reliably "
    "within the local network.",
], C1x+PAD, y, C1w-PAD*2, 2.75, sz=FS_BODY, sp=SP_BODY); y += 2.85

SH("Problem Statement", C1x, y, C1w); y += SH_DY
ML([
    "Traditional weather apps rely on generalised regional radars that fail to detect hyper-local "
    "storms. Modern smart weather gadgets depend completely on third-party cloud hosting, "
    "introducing latency, subscription fees, and catastrophic failures during stormy internet "
    "cutouts. Hobbyist weather stations measure only raw instantaneous temperature and humidity, "
    "completely ignoring barometric pressure trends - the primary physical indicators of "
    "approaching precipitation.",
], C1x+PAD, y, C1w-PAD*2, 1.70, sz=FS_BODY, sp=SP_BODY); y += 1.80

SH("Objectives", C1x, y, C1w); y += SH_DY
MIXED_LIST([
    ("Obj-1  Multi-Sensor Acquisition & Interfacing:",
     "Sample temperature, relative humidity, and barometric pressure at 1-min intervals via "
     "DHT11 (GPIO) and BMP280 (I2C, 16x oversampling, IIR filtering)."),
    ("Obj-2  ESP32 Gateway, NTP Sync & Offline Resilience:",
     "ESP32 receives JSON via UART (115200 baud); appends NTP IST timestamp + RSSI; "
     "HTTP POST to Django REST API (:8000); 120-record FIFO buffer auto-flushes on reconnect."),
    ("Obj-3  Django AI Engine, Self-Learning & Multi-Channel Alerts:",
     "SGDClassifier on 26,280 Open-Meteo samples; partial_fit() every 6 h; < 15 ms inference; "
     "Telegram Bot + Mobile Browser Push + Email hazard alert dispatch."),
], C1x+PAD, y, C1w-PAD*2, 2.25, sz=FS_BODY_SM, sp=SP_LIST); y += 2.35

SH("References", C1x, y, C1w); y += SH_DY
ML([
    "[1] Al-Absi et al., 'IoT-Based Weather Station Using ESP32,' IEEE Access, 8, 2020.",
    "[2] Kumar & Priya, 'Precipitation Prediction Using Atmospheric Pressure Differentials,' J. Atmos. Oceanic Tech., 38, 2021.",
    "[3] Warden & Situnayake, TinyML: Machine Learning with TensorFlow Lite, O'Reilly, 2021.",
    "[4] Zhang et al., 'Micro-Barometric Pressure Drops as Precursors to Convective Storms,' Weather & Forecasting, 37, 2022.",
    "[5] Roy et al., 'Edge-Computing Weather Stations for Micro-Climate Monitoring,' Comp. & Elec. in Ag., 204, 2023.",
    "[6] Nguyen et al., 'Real-Time Embedded Neural Network Inference on ESP32,' IEEE Embedded Sys. Letters, 16, 2024.",
    "[7] Farooq et al., 'TinyML-Based On-Chip Rainfall Nowcasting Without Internet,' Sensors, 25, 2025.",
    "[8] Open-Meteo Historical Archive API: https://open-meteo.com",
    "[9] Scikit-Learn Continual Learning & SGD Guide: https://scikit-learn.org",
], C1x+PAD, y, C1w-PAD*2, BOT - y - 0.06, sz=9.5, sp=Pt(4))

# ═══════════════════════════════════════════════════════════════════════════════
# COLUMN 2: Proposed Methodology | Control Parameters | System Architecture | Existing Systems
# ═══════════════════════════════════════════════════════════════════════════════
y = TOP + 0.05

SH("Proposed Methodology", C2x, y, C2w); y += SH_DY
MIXED_LIST([
    ("1. Sense:",
     "Arduino Uno reads DHT11 (temp, humidity) and BMP280 (barometric pressure via I2C, 16x "
     "oversampling, IIR filtering) every 60 s. Clean readings packaged into compact JSON."),
    ("2. Stream:",
     "JSON transmitted over direct UART: Arduino Uno HardwareSerial TX (Pin 1) to ESP32 "
     "HardwareSerial2 RX2 (GPIO 16) at 115200 baud. GPIO 17 TX2 to Uno Pin 0 RX; common GND. "
     "ESP32 appends NTP IST timestamp and Wi-Fi RSSI to every packet."),
    ("3. Forward:",
     "ESP32 issues HTTP POST to Django REST API (http://<SERVER_IP>:8000/api/sensors/readings/) "
     "every minute. If Wi-Fi is lost, readings buffer into a 120-record FIFO queue and "
     "auto-flush on reconnection - zero data loss during network drops."),
    ("4. Infer:",
     "Django backend computes fused temperature (avg BMP280+DHT11), NOAA Heat Index, "
     "Magnus-Tetens Dew Point, and 3-h pressure trend per reading. 24-h circular history "
     "(1,440 samples) feeds delta-P_3h, delta-P_6h, delta-RH_3h into SGDClassifier "
     "- forecasting Clear / Cloudy / Rain with calibrated probability in < 15 ms."),
    ("5. Alert:",
     "Storm, heatwave, or flood patterns trigger multi-channel hazard alerts: Telegram Bot "
     "(instant push with historical Chennai disaster pattern match), Mobile Browser Push "
     "(Web Notification API + audio chime + haptic vibration), and Email dispatch."),
    ("6. Re-Train:",
     "Every 6 hours the edge server verifies past forecasts against Open-Meteo ground truth "
     "and executes model.partial_fit() - recalibrating weights to track shifting seasonal "
     "weather patterns without manual retraining."),
], C2x+PAD, y, C2w-PAD*2, 5.60, sz=FS_BODY_SM, sp=SP_LIST); y += 5.70

SH("Control Parameters", C2x, y, C2w); y += SH_DY
R(C2x+PAD, y, C2w-PAD*2, ROW_H_HDR, fill=MIDBLUE)
T("Parameter",  C2x+PAD+0.05, y+0.04, 2.25, ROW_H_HDR-0.08, sz=FS_TBL_HDR, bold=True, col=WHITE)
T("Rule / Value", C2x+PAD+2.30, y+0.04, C2w-PAD*2-2.30, ROW_H_HDR-0.08, sz=FS_TBL_HDR, bold=True, col=WHITE)
y += ROW_H_HDR
params = [
    ("Sampling interval",  "Every 60 s; ADC values averaged"),
    ("Rain alert trigger", "Rain probability >= 60% -> alert JSON dispatch"),
    ("Offline resilience", "120-record FIFO queue; auto-flushed on Wi-Fi reconnect"),
    ("Model retraining",   "model.partial_fit() every 6 hours"),
    ("Inference latency",  "< 15 ms (Django REST server, port 8000)"),
    ("Buffer size",        "24-hour circular, 1,440 samples; < 50 MB RAM"),
]
for i, (p, v) in enumerate(params):
    bg = WHITE if i % 2 == 0 else LTBLUE
    R(C2x+PAD, y, C2w-PAD*2, ROW_H_BODY, fill=bg)
    T(p, C2x+PAD+0.05, y+0.03, 2.25, ROW_H_BODY-0.06, sz=FS_TBL_BODY, col=BLACK)
    T(v, C2x+PAD+2.30, y+0.03, C2w-PAD*2-2.30, ROW_H_BODY-0.06, sz=FS_TBL_BODY, col=BLACK)
    y += ROW_H_BODY
y += 0.12

SH("System Architecture", C2x, y, C2w); y += SH_DY
arch_h = 3.60
IMG(IMG_ARCH, C2x+PAD, y, C2w-PAD*2, arch_h)
T("Fig. 1 - Sensing layer (BMP280 + DHT11) -> Arduino Uno R3 (UART 115200 baud) "
  "-> ESP32 Gateway (NTP IST sync, 120-record offline FIFO, HTTP POST) "
  "-> Django REST AI Backend (SGD inference, partial_fit, Heat Index, Dew Point) "
  "-> Hazard Engine & Multi-Channel Alert Dispatch (Telegram Bot, Mobile Push, Email)",
  C2x+PAD, y+arch_h+0.02, C2w-PAD*2, 0.44,
  sz=FS_CAPTION, italic=True, col=NAVY, align=PP_ALIGN.CENTER)
y += arch_h + 0.50

SH("Review of Existing Systems", C2x, y, C2w); y += SH_DY
MIXED_LIST([
    ("Davis Vantage Pro2 (2017):",
     "Commercial AWS ($800-$1,500). Proprietary loggers; no on-premise ML prediction capability."),
    ("Ambient Weather WS-2902 (2019):",
     "Consumer cloud station - fails during storms when home internet drops; no offline fallback."),
    ("Smartphone Weather Apps (2021):",
     "Query regional radar over 15-25 km grids; cannot sense micro-pressure drops above a street."),
    ("Zambretti Barometric Rules (1915):",
     "Fully offline barometric formula, but ~64% accuracy; static rules; ignores humidity shifts."),
    ("Raspberry Pi Station (2020):",
     "High power draw (3-5W); cost $60-$80; prone to SD card filesystem corruption."),
], C2x+PAD, y, C2w-PAD*2, BOT - y - 0.06, sz=FS_BODY_SM, sp=SP_LIST)

# ═══════════════════════════════════════════════════════════════════════════════
# COLUMN 3: Hardware Components | Circuit Diagram | Subsystem Wiring | System Modules
# ═══════════════════════════════════════════════════════════════════════════════
y = TOP + 0.05

SH("Hardware Components", C3x, y, C3w); y += SH_DY
R(C3x+PAD, y, C3w-PAD*2, ROW_H_HDR, fill=MIDBLUE)
for txt, tx, tw in [
    ("Component",        C3x+PAD,        2.40),
    ("Role",             C3x+PAD + 2.40, 2.25),
    ("Interface / Spec", C3x+PAD + 4.65, C3w-PAD*2 - 4.65),
]:
    T(txt, tx+0.05, y+0.04, tw-0.10, ROW_H_HDR-0.08, sz=FS_TBL_HDR, bold=True, col=WHITE)
y += ROW_H_HDR

hw = [
    ("Arduino Uno Rev3",      "Sensor acquisition; JSON builder",        "ATmega328P - 5V - 16 MHz"),
    ("ESP32 DevKit V1",       "Wi-Fi gateway; UART2 RX; HTTP POST",      "Xtensa dual-core - 3.3V - 240 MHz"),
    ("DHT11 Sensor",          "Ambient temperature & relative humidity", "GPIO Pin 2 - +-2 deg C - +-5% RH"),
    ("Bosch BMP280",          "Barometric surface pressure (I2C)",       "A4/A5 - +-1 hPa - 16x oversamp."),
    ("Django REST Server",    "Edge API + AI engine + multi-ch alert",   "Python 3.13 - Django - Scikit-Learn"),
    ("SGDClassifier",         "Weather state prediction model",          "Log-loss - 6 features - <15 ms"),
    ("Open-Meteo Archive",    "Historical training dataset",             "26,280 samples - Chennai - 3 yrs"),
    ("Li-ion + Solar Panel",  "Off-grid power supply",                   "18650 cell - 5W panel - 5V boost"),
]
for i, (comp, role, spec) in enumerate(hw):
    bg = WHITE if i % 2 == 0 else LTBLUE
    R(C3x+PAD, y, C3w-PAD*2, ROW_H_BODY, fill=bg)
    for txt, tx, tw in [
        (comp, C3x+PAD,        2.40),
        (role, C3x+PAD + 2.40, 2.25),
        (spec, C3x+PAD + 4.65, C3w-PAD*2 - 4.65),
    ]:
        T(txt, tx+0.05, y+0.03, tw-0.10, ROW_H_BODY-0.06, sz=FS_TBL_BODY, col=BLACK)
    y += ROW_H_BODY
y += 0.12

SH("Circuit Diagram", C3x, y, C3w); y += SH_DY
ckt_h = 3.90
IMG(IMG_CIRCUIT, C3x+PAD, y, C3w-PAD*2, ckt_h)
T("Fig. 2 - Direct wiring: BMP280 (VCC->3.3V, SCL->A5, SDA->A4) + DHT11 (VCC->5V, DATA->Pin2) "
  "-> Arduino Uno R3 -> UART (Pin1 HW-TX -> GPIO16 RX2 | GPIO17 TX2 -> Pin0 RX | GND) @ 115200 baud "
  "-> ESP32 DevKit V1 -> HTTP POST -> Django REST Server :8000",
  C3x+PAD, y+ckt_h+0.02, C3w-PAD*2, 0.44,
  sz=FS_CAPTION, italic=True, col=NAVY, align=PP_ALIGN.CENTER)
y += ckt_h + 0.50

SH("Subsystem Wiring Breakdown", C3x, y, C3w); y += SH_DY
R(C3x+PAD, y, C3w-PAD*2, ROW_H_HDR, fill=MIDBLUE)
for txt, tx, tw in [
    ("Subsystem",         C3x+PAD,        2.40),
    ("Connection Detail", C3x+PAD + 2.40, 2.70),
    ("Interface",         C3x+PAD + 5.10, C3w-PAD*2 - 5.10),
]:
    T(txt, tx+0.05, y+0.04, tw-0.10, ROW_H_HDR-0.08, sz=FS_TBL_HDR, bold=True, col=WHITE)
y += ROW_H_HDR

wiring = [
    ("DHT11 -> Arduino Uno",   "VCC->5V  |  DATA->Pin 2  |  GND->GND",          "Digital 1-Wire"),
    ("BMP280 -> Arduino Uno",  "VCC->3.3V  |  SCL->A5  |  SDA->A4  |  GND->GND", "I2C - 16x oversamp."),
    ("Uno Pin 1 TX -> ESP32", "GPIO 16 RX2 - direct wire, no logic divider",   "HardwareSerial TX"),
    ("ESP32 GPIO 17 TX2->Uno", "Pin 0 RX - bidirectional feedback",            "UART 115200 baud"),
    ("Common GND Rail",       "Uno GND <-> ESP32 GND - common reference",      "Noise reference"),
    ("ESP32 -> Django Server", "HTTP POST /api/sensors/readings/ - 2.4 GHz",   "REST API - :8000"),
]
for i, (sub, det, note) in enumerate(wiring):
    bg = WHITE if i % 2 == 0 else LTBLUE
    R(C3x+PAD, y, C3w-PAD*2, ROW_H_BODY, fill=bg)
    for txt, tx, tw in [
        (sub,  C3x+PAD,        2.40),
        (det,  C3x+PAD + 2.40, 2.70),
        (note, C3x+PAD + 5.10, C3w-PAD*2 - 5.10),
    ]:
        T(txt, tx+0.05, y+0.03, tw-0.10, ROW_H_BODY-0.06, sz=FS_TBL_BODY, col=BLACK)
    y += ROW_H_BODY
y += 0.12

SH("System Modules", C3x, y, C3w); y += SH_DY
MIXED_LIST([
    ("Module 1 - Data Acquisition & Sensor Fusion:",
     "DHT11 captures humidity; BMP280 samples barometric pressure via I2C with 16x oversampling "
     "and IIR filtering. Fused temperature computed as clean arithmetic average (BMP280 + DHT11). "
     "Uno packages metrics into JSON every 60 s."),
    ("Module 2 - High-Speed Direct UART Telemetry:",
     "Arduino HardwareSerial TX (Pin 1) streams to ESP32 HardwareSerial2 RX2 (GPIO 16) at 115200 baud. "
     "GPIO 17 TX2 connects to Uno Pin 0 RX with common GND. Zero packet loss observed."),
    ("Module 3 - Gateway & Resilient Telemetry Queue:",
     "ESP32 syncs NTP IST time, appends Wi-Fi RSSI, and issues HTTP POST to Django REST API. "
     "Readings during outages buffer into a 120-record FIFO queue and flush on reconnection."),
    ("Module 4 - Edge AI Prediction Engine:",
     "24-h circular history computes delta-P_3h, delta-P_6h, delta-RH_3h. SGDClassifier (log-loss) "
     "evaluates scaled 6-D vector in < 15 ms, outputting Clear / Cloudy / Rain with calibrated probabilities."),
    ("Module 5 - Emergency Alerts & Live Dashboard:",
     "Multi-channel hazard alerts (Telegram Bot, Mobile Browser Push with sound chime, Email) "
     "dispatched on extreme conditions with historical Chennai disaster pattern match. "
     "Django dashboard (:8000) provides real-time gauges and future date forecasting."),
], C3x+PAD, y, C3w-PAD*2, BOT - y - 0.06, sz=FS_BODY_SM, sp=SP_LIST)

# ═══════════════════════════════════════════════════════════════════════════════
# COLUMN 4: Prototype Design | Results Graphs | Benchmark Comparison | Feature Weights
# ═══════════════════════════════════════════════════════════════════════════════
y = TOP + 0.05

SH("Prototype Design", C4x, y, C4w); y += SH_DY
proto_h = 3.90
IMG(IMG_PROTO, C4x+PAD, y, C4w-PAD*2, proto_h)
T("Fig. 3 - Prototype layout: (1) Stevenson louvered shelter  (2) Bosch BMP280 baro chamber  "
  "(3) DHT11 intake port  (4) Arduino Uno R3 A/D sampler  (5) ESP32 Wi-Fi gateway (UART)  "
  "(6) Poonamallee mounting mast  (7) Regulated power / USB bridge",
  C4x+PAD, y+proto_h+0.02, C4w-PAD*2, 0.44,
  sz=FS_CAPTION, italic=True, col=NAVY, align=PP_ALIGN.CENTER)
y += proto_h + 0.50

SH("Results & Performance Graphs", C4x, y, C4w); y += SH_DY
res_h = 4.80
IMG(IMG_RESULTS, C4x+PAD, y, C4w-PAD*2, res_h)
T("Fig. 4 - Top: 24-h Temperature & Humidity Forecast (P10-P90 uncertainty bounds, Poonamallee). "
  "Bottom: Barometric Pressure Tendency & Cyclone Hazard Trigger - Michaung analog validated at "
  "delta-P = -4.2 hPa / 3h, crossing severe cyclone threshold at 1000 hPa.",
  C4x+PAD, y+res_h+0.02, C4w-PAD*2, 0.44,
  sz=FS_CAPTION, italic=True, col=NAVY, align=PP_ALIGN.CENTER)
y += res_h + 0.50

SH("Comparison with Benchmark Systems (Report Table 5)", C4x, y, C4w); y += SH_DY
R(C4x+PAD, y, C4w-PAD*2, ROW_H_HDR, fill=MIDBLUE)
tbl_col_defs = [
    ("Metric / Parameter",    C4x+PAD,        2.25),
    ("Zambretti Rules",       C4x+PAD + 2.25, 1.25),
    ("Cloud-Based IoT",       C4x+PAD + 3.50, 1.45),
    ("This System (Edge ML)", C4x+PAD + 4.95, C4w-PAD*2 - 4.95),  # 1.85 in width
]
for txt, tx, tw in tbl_col_defs:
    T(txt, tx+0.04, y+0.04, tw-0.08, ROW_H_HDR-0.08, sz=FS_TBL_HDR, bold=True, col=WHITE)
y += ROW_H_HDR

cmp_rows = [
    ("Forecast Accuracy (Test)", "~64.0%",           "87.2%",              "86.4% - 90.8%"),
    ("Storm / Rain Recall",      "58.5%",            "88.0%",              "92.3%"),
    ("Inference Latency",        "< 1 ms",           "1,500 - 3,000 ms",   "14.2 ms"),
    ("Network Dependency",       "Offline (static)", "Requires 24/7 internet", "Local Wi-Fi - no cloud"),
    ("Monthly Cloud Cost",       "$0.00",            "$15-$40 / month",    "$0.00 - zero recurring"),
    ("Storm Survivability",      "High (mechanical)","Fails during outages","Complete local survival"),
    ("Continuous Model Updates", "None (static)",    "Manual retraining",  "Automated every 6 hours"),
]
for ri, (m, a, b, c) in enumerate(cmp_rows):
    bg = WHITE if ri % 2 == 0 else LTBLUE
    R(C4x+PAD, y, C4w-PAD*2, ROW_H_BODY, fill=bg)
    for txt, tx, tw in [
        (m, C4x+PAD,        2.25),
        (a, C4x+PAD + 2.25, 1.25),
        (b, C4x+PAD + 3.50, 1.45),
        (c, C4x+PAD + 4.95, C4w-PAD*2 - 4.95),
    ]:
        T(txt, tx+0.04, y+0.03, tw-0.08, ROW_H_BODY-0.06, sz=FS_TBL_BODY, col=BLACK)
    y += ROW_H_BODY
y += 0.12

SH("Learned SGD Feature Weights (Report Table 4)", C4x, y, C4w); y += SH_DY
R(C4x+PAD, y, C4w-PAD*2, ROW_H_HDR, fill=MIDBLUE)
wt_cols = [
    ("Class",    C4x+PAD,        0.85),
    ("Temp",     C4x+PAD + 0.85, 0.85),
    ("Humidity", C4x+PAD + 1.70, 1.05),
    ("Pressure", C4x+PAD + 2.75, 1.10),
    ("dP-3h",   C4x+PAD + 3.85, 0.95),
    ("dP-6h",   C4x+PAD + 4.80, 0.95),
    ("dRH-3h",  C4x+PAD + 5.75, C4w-PAD*2 - 5.75),
]
for txt, tx, tw in wt_cols:
    T(txt, tx+0.03, y+0.04, tw-0.06, ROW_H_HDR-0.08, sz=FS_TBL_HDR, bold=True, col=WHITE)
y += ROW_H_HDR

wt_rows = [
    ("Clear",  "+0.3136", "-0.2434", "+0.8960 *", "+0.0298", "-0.4206", "+0.3659"),
    ("Cloudy", "-0.6815", "-0.7338", "-0.5773",   "+0.0177", "+0.3214", "+0.2533"),
    ("Rain",   "+0.5290", "+1.1644 *","+0.0111",  "+0.0591", "-0.0657", "-0.2830"),
]
xs = [c[1] for c in wt_cols]
ws = [c[2] for c in wt_cols]
for ri, row in enumerate(wt_rows):
    bg = WHITE if ri % 2 == 0 else LTBLUE
    R(C4x+PAD, y, C4w-PAD*2, ROW_H_BODY, fill=bg)
    for j, (txt, tx, tw) in enumerate(zip(row, xs, ws)):
        star = "*" in txt
        T(txt.replace(" *",""), tx+0.03, y+0.03, tw-0.06, ROW_H_BODY-0.06,
          sz=FS_TBL_BODY, col=GREEN if star else BLACK, bold=star)
    y += ROW_H_BODY

T("* Strongest positive weight per class  |  "
  "Clear: high pressure -> stable skies  |  Rain: humidity saturation is primary driver",
  C4x+PAD, y+0.04, C4w-PAD*2, 0.28, sz=FS_CAPTION, italic=True, col=NAVY)

# ═══════════════════════════════════════════════════════════════════════════════
# COLUMN 5: Performance Analysis | Data Collection | Conclusion | Future Scope
# ═══════════════════════════════════════════════════════════════════════════════
y = TOP + 0.05

SH("Performance Analysis", C5x, y, C5w); y += SH_DY
ML([
    "Inference Latency: 14.2 ms average (Django REST server, port 8000) - 100x faster than commercial "
    "cloud APIs (1,500-3,000 ms) that also fail during internet outages.",

    "Training Convergence: Training accuracy begins at 58.8% and climbs steeply during the "
    "first 15 epochs, reaching 87.0% before stabilising at 89.8%-90.2%. Validation accuracy "
    "mirrors this trajectory, climbing from 56.1% to stabilise at 86.4% - a gap of only ~3.4%, "
    "confirming robust generalization without overfitting.",

    "3-Class Confusion Matrix (2,852 test events):",
    "  Clear:   915/1,000 TP - 91.5% recall. Misclassifications occur during evening radiation "
    "cooling where humidity temporarily spikes without rain.",
    "  Cloudy:  798/900 TP - 88.7% recall. Transitional cloud cover blurs the boundary between "
    "thick clouds and light drizzle.",
    "  Rain:    879/952 TP - 92.3% recall. Sharp pressure drops (delta-P3h < -1.5 hPa) and "
    "humidity surges (delta-RH > +12%) enable strong classification.",

    "Online Self-Learning: Injecting real-world ground truth via partial_fit() dynamically "
    "adjusts classification probabilities without requiring full retraining from scratch.",

    "Telemetry Resilience & Memory: 24-hour circular buffer uses < 50 MB RAM on edge server. "
    "120-record offline FIFO queue on ESP32 guarantees zero telemetry loss across network drops.",

    "Hazard Alert Channels: Telegram Bot (instant push with historical Chennai disaster "
    "pattern match), Mobile Browser Push (Web Notification API + audio chime + haptic "
    "vibration), and Email - triggered on storm, heatwave, or flood pattern detection.",
], C5x+PAD, y, C5w-PAD*2, 6.30, sz=FS_BODY, sp=SP_BODY); y += 6.40

SH("Data Collection", C5x, y, C5w); y += SH_DY
ML([
    "A download_data.py script curated 3 complete years of hourly meteorological data "
    "(26,280 samples) from the Open-Meteo Historical Archive for Chennai "
    "(Lat: 13.0827 N, Lon: 80.2707 E).",

    "Raw dataset: hourly temperature (deg C), relative humidity (%), surface pressure (hPa), "
    "precipitation (mm), and cloud cover. Features engineered for thermodynamic rate-of-change "
    "dynamics: delta_p_3h, delta_p_6h, delta_rh_3h.",

    "Target labels defined 6 hours ahead: 'Rain' (precipitation > 0.2 mm), "
    "'Cloudy' (cloud cover >= 60%), 'Clear' otherwise.",
], C5x+PAD, y, C5w-PAD*2, 2.10, sz=FS_BODY, sp=SP_BODY); y += 2.20

SH("Conclusion", C5x, y, C5w); y += SH_DY
ML([
    "The project demonstrates a complete, production-grade edge-server weather observatory: "
    "Arduino Uno sensor node, ESP32 gateway (NTP sync, offline FIFO resilience), and a "
    "Django REST AI backend with SGD-based nowcasting, auto-computed Heat Index and Dew Point, "
    "multi-channel hazard alerts (Telegram Bot, Mobile Browser Push, Email), and historical "
    "Chennai disaster pattern matching. Cloud dependency and 25 km grid averaging are "
    "eliminated; all inference runs locally in < 15 ms.",

    "1. High Predictive Accuracy: 86.4% on validation data (90.8% in testing) - significantly "
    "outperforming traditional Zambretti barometric equations (~64%).",
    "2. Effective Storm Detection: 92.3% recall in detecting incoming rainfall events, reliably "
    "identifying sharp pressure drops and humidity surges that precede local storms.",
    "3. Multi-Channel Alert Dispatch: Telegram Bot, Mobile Browser Push (audio + haptic), and "
    "Email triggered automatically with historical Chennai disaster analog context.",
    "4. Automated Continual Self-Learning: model.partial_fit() every 6 hours successfully adapts "
    "model weights to shifting seasonal weather patterns without manual intervention.",
], C5x+PAD, y, C5w-PAD*2, 3.80, sz=FS_BODY, sp=SP_BODY); y += 3.90

SH("Future Scope", C5x, y, C5w); y += SH_DY
MIXED_LIST([
    ("Solar-Powered Field Deployment:",
     "Pair with 18650 Li-ion + 5W solar panel; use ESP32 deep-sleep for continuous outdoor operation."),
    ("Weatherproof Stevenson Screen:",
     "3D-printed, double-louvered screen sheltering sensors from solar radiation while maintaining open airflow."),
    ("Wind Speed & Rain Gauge Expansion:",
     "Add tipping-bucket rain gauge and pulse anemometer for rainfall volume and wind vectors."),
    ("LoRa Long-Range Mesh Networking:",
     "Replace Wi-Fi with SX1278 LoRa radio to share forecasts across clusters spanning 5-10 km without cellular access."),
    ("Deep Learning Upgrade:",
     "Replace SGDClassifier with a quantised 1D-CNN or LSTM for improved temporal pattern recognition on-device."),
    ("OTA Updates & Mobile App:",
     "Over-the-air firmware updates via MQTT and dedicated mobile application for remote monitoring."),
], C5x+PAD, y, C5w-PAD*2, BOT - y - 0.06, sz=FS_BODY_SM, sp=SP_LIST)

# ── Footer ────────────────────────────────────────────────────────────────────
R(0, H - 0.44, W, 0.44, fill=NAVY)
T("Sri Ramachandra Faculty of Engineering & Technology, SRIHER, Porur, Chennai - 600116   "
  "|   Supervisor: Mr. Manoj Kumaran, Dept. of Cyber Security & IoT, SRET",
  0.30, H - 0.41, W * 0.60, 0.36, sz=FS_FOOTER, col=LTBLUE)
T("AI-Based Local Weather Forecasting & Prediction System  |  September, 2026",
  W * 0.55, H - 0.41, W * 0.45, 0.36, sz=FS_FOOTER, italic=True, col=WHITE,
  align=PP_ALIGN.RIGHT)

# ── Save ──────────────────────────────────────────────────────────────────────
out = r"e:\weather predection\AI_Weather_Poster_Final.pptx"
prs.save(out)
print("Saved: " + out)
print("Slides: " + str(len(prs.slides)))
