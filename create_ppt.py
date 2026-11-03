"""
Create a PowerPoint presentation for AI-Based Local Weather Forecasting System
Styled like the ESP32 academic research poster (dark blue header, column layout, colored sections)
"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt
import copy

# ─── Color palette (taken from the poster template) ───────────────────────────
DARK_BLUE  = RGBColor(0x1A, 0x3A, 0x5C)   # deep navy – header bg
MID_BLUE   = RGBColor(0x1E, 0x5F, 0x9A)   # section headers
LIGHT_BLUE = RGBColor(0xD6, 0xE8, 0xF7)   # section header strip bg
ACCENT_TEAL= RGBColor(0x00, 0x8B, 0x8B)   # accent / table header
WHITE      = RGBColor(0xFF, 0xFF, 0xFF)
BLACK      = RGBColor(0x0D, 0x0D, 0x0D)
LIGHT_GRAY = RGBColor(0xF0, 0xF4, 0xF8)
ORANGE     = RGBColor(0xFF, 0x7F, 0x00)   # highlight / callout
GREEN      = RGBColor(0x21, 0x8A, 0x3B)

prs = Presentation()
prs.slide_width  = Inches(13.33)
prs.slide_height = Inches(7.5)

# ─── Helper utilities ─────────────────────────────────────────────────────────

def add_rect(slide, x, y, w, h, fill_rgb=None, line_rgb=None, line_width_pt=0):
    shape = slide.shapes.add_shape(1, Inches(x), Inches(y), Inches(w), Inches(h))
    shape.line.fill.background()
    if fill_rgb:
        shape.fill.solid()
        shape.fill.fore_color.rgb = fill_rgb
    else:
        shape.fill.background()
    if line_rgb:
        shape.line.color.rgb = line_rgb
        shape.line.width = Pt(line_width_pt)
    else:
        shape.line.fill.background()
    return shape


def add_textbox(slide, text, x, y, w, h,
                font_size=11, bold=False, italic=False,
                color=BLACK, align=PP_ALIGN.LEFT,
                bg_rgb=None, wrap=True):
    txb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf  = txb.text_frame
    tf.word_wrap = wrap
    p   = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size   = Pt(font_size)
    run.font.bold   = bold
    run.font.italic = italic
    run.font.color.rgb = color
    return txb


def section_header(slide, title, x, y, w, h=0.28):
    """Coloured strip with white bold title – matches poster section headers."""
    add_rect(slide, x, y, w, h, fill_rgb=MID_BLUE)
    add_textbox(slide, title, x+0.05, y+0.01, w-0.1, h,
                font_size=10, bold=True, color=WHITE, align=PP_ALIGN.LEFT)


def body_text(slide, text, x, y, w, h, size=9):
    txb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf  = txb.text_frame
    tf.word_wrap = True
    for i, line in enumerate(text.split('\n')):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        p.alignment = PP_ALIGN.LEFT
        run = p.add_run()
        run.text = line
        run.font.size = Pt(size)
        run.font.color.rgb = BLACK
    return txb


def bullet_text(slide, items, x, y, w, h, size=9):
    txb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf  = txb.text_frame
    tf.word_wrap = True
    for i, item in enumerate(items):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        p.alignment = PP_ALIGN.LEFT
        run = p.add_run()
        run.text = '• ' + item
        run.font.size = Pt(size)
        run.font.color.rgb = BLACK
    return txb


# ══════════════════════════════════════════════════════════════════════════════
#  SLIDE 1 – Title / Cover
# ══════════════════════════════════════════════════════════════════════════════
slide1 = prs.slides.add_slide(prs.slide_layouts[6])  # blank

# Full-slide navy background
add_rect(slide1, 0, 0, 13.33, 7.5, fill_rgb=DARK_BLUE)

# Decorative top bar
add_rect(slide1, 0, 0, 13.33, 0.18, fill_rgb=ACCENT_TEAL)

# Decorative bottom bar
add_rect(slide1, 0, 7.32, 13.33, 0.18, fill_rgb=ACCENT_TEAL)

# Central card
add_rect(slide1, 1.0, 1.2, 11.33, 5.1, fill_rgb=RGBColor(0x0F,0x29,0x45))

# Title
tb = slide1.shapes.add_textbox(Inches(1.2), Inches(1.5), Inches(10.9), Inches(1.5))
tf = tb.text_frame; tf.word_wrap = True
p  = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
r  = p.add_run()
r.text = "AI-BASED LOCAL WEATHER FORECASTING\nAND PREDICTION SYSTEM"
r.font.size  = Pt(32); r.font.bold = True; r.font.color.rgb = WHITE

# Subtitle
tb2 = slide1.shapes.add_textbox(Inches(1.5), Inches(3.1), Inches(10.3), Inches(0.5))
tf2 = tb2.text_frame
p2  = tf2.paragraphs[0]; p2.alignment = PP_ALIGN.CENTER
r2  = p2.add_run()
r2.text = "Using Arduino Uno and ESP32"
r2.font.size = Pt(20); r2.font.color.rgb = LIGHT_BLUE; r2.font.italic = True

# Sub-subtitle
tb3 = slide1.shapes.add_textbox(Inches(1.5), Inches(3.65), Inches(10.3), Inches(0.4))
tf3 = tb3.text_frame
p3  = tf3.paragraphs[0]; p3.alignment = PP_ALIGN.CENTER
r3  = p3.add_run()
r3.text = "Soil-moisture-driven edge ML inference with Wi-Fi telemetry, real-time dashboard & self-learning"
r3.font.size = Pt(13); r3.font.color.rgb = RGBColor(0xAA,0xCC,0xEE); r3.font.italic = True

# Divider line
add_rect(slide1, 2.0, 4.15, 9.33, 0.04, fill_rgb=ACCENT_TEAL)

# Authors + institution
tb4 = slide1.shapes.add_textbox(Inches(1.5), Inches(4.25), Inches(10.3), Inches(0.5))
tf4 = tb4.text_frame
p4  = tf4.paragraphs[0]; p4.alignment = PP_ALIGN.CENTER
r4  = p4.add_run()
r4.text = "Balavignesh K (E0225002)   |   Sudharsan N (E0225010)"
r4.font.size = Pt(14); r4.font.bold = True; r4.font.color.rgb = WHITE

tb5 = slide1.shapes.add_textbox(Inches(1.5), Inches(4.8), Inches(10.3), Inches(0.6))
tf5 = tb5.text_frame
p5  = tf5.paragraphs[0]; p5.alignment = PP_ALIGN.CENTER
r5  = p5.add_run()
r5.text = "B.Tech – Computer Science & Engineering (Cyber Security & IoT)\nSri Ramachandra Faculty of Engineering and Technology, SRIHER, Chennai – 600116"
r5.font.size = Pt(11); r5.font.color.rgb = RGBColor(0xAA,0xCC,0xEE)

tb6 = slide1.shapes.add_textbox(Inches(1.5), Inches(5.5), Inches(10.3), Inches(0.4))
tf6 = tb6.text_frame
p6  = tf6.paragraphs[0]; p6.alignment = PP_ALIGN.CENTER
r6  = p6.add_run()
r6.text = "September, 2026"
r6.font.size = Pt(12); r6.font.color.rgb = LIGHT_BLUE

# Slide number label
add_textbox(slide1, "1 / 10", 12.6, 7.2, 0.7, 0.25,
            font_size=8, color=RGBColor(0x88,0xAA,0xCC), align=PP_ALIGN.RIGHT)


# ══════════════════════════════════════════════════════════════════════════════
#  SLIDE 2 – Abstract & Introduction
# ══════════════════════════════════════════════════════════════════════════════
slide2 = prs.slides.add_slide(prs.slide_layouts[6])

# Header bar
add_rect(slide2, 0, 0, 13.33, 0.7, fill_rgb=DARK_BLUE)
add_textbox(slide2,
    "AI-Based Local Weather Forecasting & Prediction System  |  Abstract & Introduction",
    0.15, 0.08, 12.8, 0.55, font_size=16, bold=True, color=WHITE)

# Background
add_rect(slide2, 0, 0.7, 13.33, 6.8, fill_rgb=LIGHT_GRAY)

# ── LEFT COLUMN ──
# Abstract section
add_rect(slide2, 0.15, 0.85, 6.15, 0.28, fill_rgb=MID_BLUE)
add_textbox(slide2, "Abstract", 0.2, 0.87, 6.0, 0.24,
            font_size=10, bold=True, color=WHITE)

add_rect(slide2, 0.15, 1.13, 6.15, 2.05, fill_rgb=WHITE)
body_text(slide2,
    "The AI-based weather prediction system was developed to address the failure of generic weather apps "
    "to detect localized microclimates and neighbourhood rainfall storms. Standard mobile weather services "
    "pull data from regional airports spanning 15–25 km away, averaging out hyper-local conditions.\n\n"
    "This project presents a low-cost, IoT edge-server node built around an Arduino Uno and ESP32. "
    "A DHT11 sensor records temperature and humidity; a Bosch BMP280 captures barometric pressure every "
    "60 seconds. The ESP32 acts as a Wi-Fi gateway, posting JSON telemetry to a local Python Flask server "
    "that performs machine learning inference in under 15 ms and returns the forecast.\n\n"
    "A solar-panel with Li-ion battery backup frees the node from grid power.",
    0.2, 1.15, 6.0, 2.0, size=9)

# Introduction – Need for the Study
add_rect(slide2, 0.15, 3.22, 6.15, 0.28, fill_rgb=MID_BLUE)
add_textbox(slide2, "Introduction – Need for the Study", 0.2, 3.24, 6.0, 0.24,
            font_size=10, bold=True, color=WHITE)

add_rect(slide2, 0.15, 3.50, 6.15, 1.85, fill_rgb=WHITE)
body_text(slide2,
    "Accurate local weather prediction is critical for communities, small farms, and outdoor operations. "
    "Traditional forecasting relies on numerical weather prediction (NWP) models running on "
    "macro-scale supercomputers that divide the atmosphere into large 5–15 km grids, missing "
    "hyper-local storm cells that form and dissipate within kilometres.\n\n"
    "Remote farms lack grid power; commercial precision-irrigation systems are expensive; and "
    "existing IoT kits provide no predictive intelligence. This system bridges that gap with "
    "an edge-server architecture costing under ₹3,000.",
    0.2, 3.52, 6.0, 1.8, size=9)

# ── RIGHT COLUMN ──
# Applications
add_rect(slide2, 6.55, 0.85, 6.6, 0.28, fill_rgb=MID_BLUE)
add_textbox(slide2, "Applications", 6.60, 0.87, 6.4, 0.24,
            font_size=10, bold=True, color=WHITE)

add_rect(slide2, 6.55, 1.13, 6.6, 1.65, fill_rgb=WHITE)
bullet_text(slide2, [
    "Smart Agriculture & Greenhouse Automation: predict localised downpours hours ahead, "
    "halt automated irrigation, deploy greenhouse covers.",
    "Campus & Construction Site Safety: autonomous weather nowcasting, issuing early storm "
    "and precipitation warnings.",
    "Remote & Disaster-Prone Communities: off-grid installations in rural areas without "
    "cloud subscription costs.",
    "Smart Home Ventilation & Storm Prep: trigger automated motorised window closers and "
    "rain shutters when barometric pressure plunges."
], 6.60, 1.15, 6.4, 1.6, size=8.5)

# Motivation
add_rect(slide2, 6.55, 2.82, 6.6, 0.28, fill_rgb=MID_BLUE)
add_textbox(slide2, "Motivation behind the Study", 6.60, 2.84, 6.4, 0.24,
            font_size=10, bold=True, color=WHITE)

add_rect(slide2, 6.55, 3.10, 6.6, 1.27, fill_rgb=WHITE)
body_text(slide2,
    "The drive behind this project is to apply accessible, low-cost IoT hardware and state-of-the-art "
    "Machine Learning toward an environmental challenge we encounter daily. Basic DIY weather projects "
    "typically display only temperature on an LCD. Physical meteorology, however, shows that pressure "
    "differentials and multi-hour humidity trends reliably predict storms. This project encodes those "
    "scientific rules into an SGD-based online classifier that continuously learns from real observations.",
    6.60, 3.12, 6.4, 1.2, size=9)

# Challenges
add_rect(slide2, 6.55, 4.41, 6.6, 0.28, fill_rgb=MID_BLUE)
add_textbox(slide2, "Challenges Addressed", 6.60, 4.43, 6.4, 0.24,
            font_size=10, bold=True, color=WHITE)

add_rect(slide2, 6.55, 4.69, 6.6, 2.55, fill_rgb=WHITE)
bullet_text(slide2, [
    "Electrical & Microcontroller Interfacing: 5V (Uno) ↔ 3.3V (ESP32) logic mismatch across UART.",
    "Continuous Multi-Hour Feature Tracking: 24-hour circular buffer for pressure & humidity deltas.",
    "Real-Time Edge Latency: full JSON telemetry → inference → response within < 15 ms.",
    "Dynamic Model Retraining: automated partial_fit() every 6 hours to prevent concept drift.",
], 6.60, 4.71, 6.4, 2.5, size=8.5)

# Footer
add_rect(slide2, 0, 7.28, 13.33, 0.22, fill_rgb=DARK_BLUE)
add_textbox(slide2,
    "Sri Ramachandra Faculty of Engineering & Technology, SRIHER  |  B.Tech CSE (Cyber Security & IoT)",
    0.15, 7.28, 11.5, 0.22, font_size=8, color=WHITE)
add_textbox(slide2, "2 / 10", 12.6, 7.28, 0.7, 0.22,
            font_size=8, color=WHITE, align=PP_ALIGN.RIGHT)


# ══════════════════════════════════════════════════════════════════════════════
#  SLIDE 3 – Literature Review
# ══════════════════════════════════════════════════════════════════════════════
slide3 = prs.slides.add_slide(prs.slide_layouts[6])
add_rect(slide3, 0, 0, 13.33, 0.7, fill_rgb=DARK_BLUE)
add_textbox(slide3, "AI-Based Local Weather Forecasting & Prediction System  |  Literature Review",
            0.15, 0.08, 12.8, 0.55, font_size=16, bold=True, color=WHITE)
add_rect(slide3, 0, 0.7, 13.33, 6.8, fill_rgb=LIGHT_GRAY)

# Literature Survey
add_rect(slide3, 0.15, 0.85, 12.9, 0.28, fill_rgb=MID_BLUE)
add_textbox(slide3, "2.1  Literature Survey", 0.2, 0.87, 12.6, 0.24,
            font_size=10, bold=True, color=WHITE)
add_rect(slide3, 0.15, 1.13, 12.9, 1.35, fill_rgb=WHITE)
body_text(slide3,
    "Kumar & Patel (2021) and Sharma et al. (2022) established that machine learning provides higher "
    "prediction accuracy than static equations, but their approaches relied on desktop computers or cloud "
    "hosting. In cloud architectures, internet latency and service dropouts compromise early-warning "
    "capability. Nguyen et al. (2024) demonstrated real-time neural network inference on ESP32 Xtensa "
    "dual-core architectures. Farooq et al. (2025) proved that TinyML-based on-chip rainfall nowcasting "
    "can operate completely without internet dependencies. This project synthesises those findings into "
    "an affordable dual-microcontroller system.",
    0.2, 1.15, 12.6, 1.3, size=9)

# Review of Existing Systems – table
add_rect(slide3, 0.15, 2.52, 12.9, 0.28, fill_rgb=MID_BLUE)
add_textbox(slide3, "2.2  Review of Existing Systems", 0.2, 2.54, 12.6, 0.24,
            font_size=10, bold=True, color=WHITE)

# Table header row
add_rect(slide3, 0.15, 2.80, 12.9, 0.30, fill_rgb=ACCENT_TEAL)
for col, (txt, x, w) in enumerate([
    ("System / Product", 0.15, 3.2),
    ("Key Capability", 3.35, 3.2),
    ("Limitation", 6.55, 3.2),
    ("ML / Edge?", 9.75, 3.3),
]):
    add_textbox(slide3, txt, x+0.05, 2.82, w-0.1, 0.26,
                font_size=9, bold=True, color=WHITE)

rows = [
    ("Davis Vantage Pro2 (2017)", "Highly accurate commercial AWS; agriculture & research use.",
     "Cost $800–$1,500; proprietary loggers; no ML prediction.", "No"),
    ("Netatmo Urban Weather Station (2019)", "Consumer smart station with cloud dashboard & app.",
     "Relies on Netatmo cloud; fails during internet outage.", "No"),
    ("IBM Watson Weather Co. API (2020)", "Hyperlocal API with ML forecasting for enterprises.",
     "Subscription cost; cloud latency; no offline mode.", "Cloud only"),
    ("Raspberry Pi Weather Station (2021)", "DIY edge computing; Python scripting; local storage.",
     "Higher power consumption; no real-time ML self-learning.", "Partial"),
    ("Arduino + BMP180 Basic Logger (2023)", "Open-source, low-cost sensor node.",
     "No Wi-Fi, no ML, no forecasting—purely a data logger.", "No"),
    ("THIS SYSTEM (2026)", "Edge ML SGD inference + online self-learning on Flask server.",
     "None significant; expandable with LoRa & solar.", "✓ Yes"),
]

row_colors = [WHITE, LIGHT_GRAY, WHITE, LIGHT_GRAY, WHITE, RGBColor(0xD4,0xED,0xDA)]
for ri, (s, k, l, m) in enumerate(rows):
    ry = 3.10 + ri * 0.50
    add_rect(slide3, 0.15, ry, 12.9, 0.50, fill_rgb=row_colors[ri])
    for txt, x, w in [(s, 0.15, 3.2), (k, 3.35, 3.2), (l, 6.55, 3.2), (m, 9.75, 3.3)]:
        body_text(slide3, txt, x+0.05, ry+0.02, w-0.1, 0.46, size=8.5)

# Footer
add_rect(slide3, 0, 7.28, 13.33, 0.22, fill_rgb=DARK_BLUE)
add_textbox(slide3,
    "Sri Ramachandra Faculty of Engineering & Technology, SRIHER  |  B.Tech CSE (Cyber Security & IoT)",
    0.15, 7.28, 11.5, 0.22, font_size=8, color=WHITE)
add_textbox(slide3, "3 / 10", 12.6, 7.28, 0.7, 0.22,
            font_size=8, color=WHITE, align=PP_ALIGN.RIGHT)


# ══════════════════════════════════════════════════════════════════════════════
#  SLIDE 4 – Problem Statement & Objectives
# ══════════════════════════════════════════════════════════════════════════════
slide4 = prs.slides.add_slide(prs.slide_layouts[6])
add_rect(slide4, 0, 0, 13.33, 0.7, fill_rgb=DARK_BLUE)
add_textbox(slide4, "AI-Based Local Weather Forecasting & Prediction System  |  Problem Statement & Objectives",
            0.15, 0.08, 12.8, 0.55, font_size=16, bold=True, color=WHITE)
add_rect(slide4, 0, 0.7, 13.33, 6.8, fill_rgb=LIGHT_GRAY)

# Problem Statement
add_rect(slide4, 0.15, 0.85, 12.9, 0.28, fill_rgb=MID_BLUE)
add_textbox(slide4, "3.1  Problem Statement", 0.2, 0.87, 12.6, 0.24,
            font_size=10, bold=True, color=WHITE)
add_rect(slide4, 0.15, 1.13, 12.9, 1.0, fill_rgb=WHITE)
body_text(slide4,
    "Traditional weather apps rely on generalised regional radars that fail to detect hyper-local storms. "
    "Modern smart weather gadgets depend completely on third-party cloud hosting, introducing latency, "
    "subscription fees, and catastrophic failures during stormy internet cutouts. Hobbyist Arduino weather "
    "loggers record only instantaneous sensor values with no predictive intelligence. There is a clear gap "
    "for an autonomous, offline-capable, self-learning local forecasting node that costs under ₹3,000.",
    0.2, 1.15, 12.6, 0.95, size=9)

# Objectives – 3 columns
add_rect(slide4, 0.15, 2.17, 12.9, 0.28, fill_rgb=MID_BLUE)
add_textbox(slide4, "3.2  Objectives", 0.2, 2.19, 12.6, 0.24,
            font_size=10, bold=True, color=WHITE)

obj_data = [
    ("Objective 1:\nMulti-Sensor Acquisition & Interfacing",
     "• Sample temperature, humidity & barometric pressure at 1-minute intervals.\n"
     "• Interface DHT11 via digital GPIO; BMP280 via I²C with 16× oversampling.\n"
     "• Design a JSON telemetry packet: {temp, humidity, pressure, timestamp}."),
    ("Objective 2:\nEdge Wi-Fi Gateway & Network Dispatching",
     "• Receive serial telemetry from Uno; transmit to Flask server over Wi-Fi.\n"
     "• Implement HardwareSerial2 UART (Uno Pin 11 → ESP32 GPIO 16 RX2).\n"
     "• Parse JSON forecast reply; drive serial actuator feedback."),
    ("Objective 3:\nEdge ML Engine & Continual Self-Learning",
     "• Execute ML inference on edge server; update weights continuously.\n"
     "• Train SGDClassifier with log-loss on 3 years (26,280 samples) of Open-Meteo data.\n"
     "• Engineer 3h/6h pressure trends; run partial_fit() every 6 hours."),
]

for ci, (title, body) in enumerate(obj_data):
    cx = 0.15 + ci * 4.35
    add_rect(slide4, cx, 2.49, 4.25, 0.36, fill_rgb=ACCENT_TEAL)
    add_textbox(slide4, title, cx+0.1, 2.51, 4.05, 0.32,
                font_size=9, bold=True, color=WHITE)
    add_rect(slide4, cx, 2.85, 4.25, 1.85, fill_rgb=WHITE)
    body_text(slide4, body, cx+0.1, 2.87, 4.05, 1.8, size=8.5)

# Methodology
add_rect(slide4, 0.15, 4.74, 12.9, 0.28, fill_rgb=MID_BLUE)
add_textbox(slide4, "3.3  Methodology Overview", 0.2, 4.76, 12.6, 0.24,
            font_size=10, bold=True, color=WHITE)
add_rect(slide4, 0.15, 5.02, 12.9, 2.22, fill_rgb=WHITE)
body_text(slide4,
    "The underlying architecture is decentralised and edge-server based. The Arduino Uno serves as the "
    "frontline sensory node, interfacing with the DHT11 and BMP280. It streams JSON packets directly via "
    "UART (Pin 11 TX → GPIO 16 RX2) to the ESP32 every 60 seconds. The ESP32 acts as an IoT Wi-Fi "
    "gateway, forwarding telemetry via HTTP POST to a Python Flask server on the local LAN.\n\n"
    "The Flask server maintains a 24-hour circular buffer (1,440 samples) and computes feature-engineered "
    "inputs: ΔP_3h, ΔP_6h, ΔRH_3h. An SGDClassifier with log-loss predicts one of three weather states "
    "(Clear / Cloudy / Rain). Every 6 hours, past predictions are compared against real ground-truth "
    "observations from Open-Meteo and model weights are updated via model.partial_fit(), preventing "
    "seasonal concept drift. The ESP32 receives the forecast label and confidence and can drive actuators "
    "or display results on an OLED.",
    0.2, 5.04, 12.6, 2.15, size=9)

# Footer
add_rect(slide4, 0, 7.28, 13.33, 0.22, fill_rgb=DARK_BLUE)
add_textbox(slide4,
    "Sri Ramachandra Faculty of Engineering & Technology, SRIHER  |  B.Tech CSE (Cyber Security & IoT)",
    0.15, 7.28, 11.5, 0.22, font_size=8, color=WHITE)
add_textbox(slide4, "4 / 10", 12.6, 7.28, 0.7, 0.22,
            font_size=8, color=WHITE, align=PP_ALIGN.RIGHT)


# ══════════════════════════════════════════════════════════════════════════════
#  SLIDE 5 – System Architecture
# ══════════════════════════════════════════════════════════════════════════════
slide5 = prs.slides.add_slide(prs.slide_layouts[6])
add_rect(slide5, 0, 0, 13.33, 0.7, fill_rgb=DARK_BLUE)
add_textbox(slide5, "AI-Based Local Weather Forecasting & Prediction System  |  System Architecture",
            0.15, 0.08, 12.8, 0.55, font_size=16, bold=True, color=WHITE)
add_rect(slide5, 0, 0.7, 13.33, 6.8, fill_rgb=LIGHT_GRAY)

# Architecture diagram (text-based)
add_rect(slide5, 0.15, 0.85, 12.9, 0.28, fill_rgb=MID_BLUE)
add_textbox(slide5, "End-to-End System Architecture – Sensing → Brain → Action → Cloud",
            0.2, 0.87, 12.6, 0.24, font_size=10, bold=True, color=WHITE)

# 4 architecture blocks
arch_blocks = [
    ("SENSING LAYER\n(Arduino Uno)", MID_BLUE,
     "• DHT11: Temperature + Humidity\n  (Digital GPIO Pin 2)\n"
     "• BMP280: Barometric Pressure\n  (I²C: SDA=A4, SCL=A5)\n"
     "• Sampling: Every 60 seconds\n"
     "• Output: JSON packet via UART\n  (SoftwareSerial Pin 11)"),
    ("GATEWAY LAYER\n(ESP32 DevKit V1)", MID_BLUE,
     "• Receives JSON via HardwareSerial2\n  (GPIO 16 RX2)\n"
     "• Connects to 2.4 GHz Wi-Fi LAN\n"
     "• HTTP POST to Flask server\n  every 60 s\n"
     "• Parses forecast reply JSON\n"
     "• Actuator / OLED feedback"),
    ("EDGE ML SERVER\n(Python Flask)", MID_BLUE,
     "• 24-hour circular buffer (1440 pts)\n"
     "• Feature engineering:\n  ΔP_3h, ΔP_6h, ΔRH_3h\n"
     "• SGDClassifier (log-loss)\n  → Clear / Cloudy / Rain\n"
     "• model.partial_fit() every 6 h\n"
     "• Inference latency: < 15 ms"),
    ("CLOUD / DASHBOARD\n(ThingSpeak + Alerts)", MID_BLUE,
     "• ThingSpeak: real-time field charts\n  for T, RH, P, forecast label\n"
     "• Optional Telegram bot alerts\n  on storm / rain prediction\n"
     "• Open-Meteo ground truth pull\n  for retraining validation\n"
     "• Local SQLite history log"),
]

for bi, (title, hdr_col, body) in enumerate(arch_blocks):
    bx = 0.15 + bi * 3.3
    add_rect(slide5, bx, 1.17, 3.2, 0.45, fill_rgb=hdr_col)
    add_textbox(slide5, title, bx+0.1, 1.19, 3.0, 0.41,
                font_size=9.5, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    add_rect(slide5, bx, 1.62, 3.2, 2.55, fill_rgb=WHITE)
    body_text(slide5, body, bx+0.1, 1.64, 3.0, 2.5, size=8.5)

# Arrows between blocks (text arrows)
for ai in range(3):
    ax = 3.35 + ai * 3.3
    add_textbox(slide5, "►", ax, 2.35, 0.1, 0.3, font_size=14,
                color=ACCENT_TEAL, align=PP_ALIGN.CENTER)

# Wiring table
add_rect(slide5, 0.15, 4.22, 12.9, 0.28, fill_rgb=MID_BLUE)
add_textbox(slide5, "3.5  Circuit Interfacing – Subsystem Wiring Summary",
            0.2, 4.24, 12.6, 0.24, font_size=10, bold=True, color=WHITE)

# Table
add_rect(slide5, 0.15, 4.50, 12.9, 0.28, fill_rgb=ACCENT_TEAL)
for hdr, x, w in [("Subsystem", 0.15, 3.5), ("Connection Detail", 3.65, 5.0), ("Pin / Interface", 8.65, 4.4)]:
    add_textbox(slide5, hdr, x+0.05, 4.52, w-0.1, 0.24,
                font_size=9, bold=True, color=WHITE)

wiring_rows = [
    ("DHT11 → Arduino Uno", "VCC→5V, DATA→Pin2 (Digital), GND→GND", "Digital GPIO Pin 2"),
    ("BMP280 → Arduino Uno", "VCC→3.3V, GND→GND, SCL→A5, SDA→A4", "I²C Bus (A4/A5)"),
    ("Arduino Uno → ESP32", "Uno Pin 11 (TX) → ESP32 GPIO 16 (RX2); Common GND", "SoftwareSerial / UART2"),
    ("ESP32 → Flask Server", "HTTP POST /api/weather via 2.4 GHz Wi-Fi LAN", "REST API (port 5000)"),
    ("Voltage Logic", "5V Uno ↔ 3.3V ESP32: direct UART with shared GND reference", "Logic-safe wiring"),
]

for ri, (sub, det, pin) in enumerate(wiring_rows):
    ry = 4.78 + ri * 0.44
    bg = WHITE if ri % 2 == 0 else LIGHT_GRAY
    add_rect(slide5, 0.15, ry, 12.9, 0.44, fill_rgb=bg)
    for txt, x, w in [(sub, 0.15, 3.5), (det, 3.65, 5.0), (pin, 8.65, 4.4)]:
        body_text(slide5, txt, x+0.05, ry+0.02, w-0.1, 0.40, size=8.5)

# Footer
add_rect(slide5, 0, 7.28, 13.33, 0.22, fill_rgb=DARK_BLUE)
add_textbox(slide5,
    "Sri Ramachandra Faculty of Engineering & Technology, SRIHER  |  B.Tech CSE (Cyber Security & IoT)",
    0.15, 7.28, 11.5, 0.22, font_size=8, color=WHITE)
add_textbox(slide5, "5 / 10", 12.6, 7.28, 0.7, 0.22,
            font_size=8, color=WHITE, align=PP_ALIGN.RIGHT)


# ══════════════════════════════════════════════════════════════════════════════
#  SLIDE 6 – Modules & Hardware
# ══════════════════════════════════════════════════════════════════════════════
slide6 = prs.slides.add_slide(prs.slide_layouts[6])
add_rect(slide6, 0, 0, 13.33, 0.7, fill_rgb=DARK_BLUE)
add_textbox(slide6, "AI-Based Local Weather Forecasting & Prediction System  |  System Modules & Hardware",
            0.15, 0.08, 12.8, 0.55, font_size=16, bold=True, color=WHITE)
add_rect(slide6, 0, 0.7, 13.33, 6.8, fill_rgb=LIGHT_GRAY)

modules = [
    ("Module 1 – Data Acquisition & Sensor",
     "The primary sensory organ: Arduino Uno interfaces DHT11 (digital GPIO Pin 2) for temperature "
     "and relative humidity; BMP280 (I²C) for barometric pressure at 16× oversampling. Every 60 s "
     "a JSON packet {temp, humidity, pressure, ts} is built."),
    ("Module 2 – Inter-Board Direct UART Telemetry",
     "SoftwareSerial on Arduino Uno (Pin 11 TX) transmits directly to ESP32 HardwareSerial2 "
     "(GPIO 16 RX2); Uno Pin 10 (RX) ← ESP32 GPIO 17 (TX2); common GND provides noise-free "
     "bidirectional telemetry streaming without voltage shifters."),
    ("Module 3 – IoT Gateway & Networking",
     "ESP32 connects to local 2.4 GHz Wi-Fi. Every minute it POSTs the JSON telemetry to "
     "http://<LAPTOP_IP>:5000/api/weather, parses the forecast reply, and can drive OLED/actuators "
     "or re-upload summary to ThingSpeak."),
    ("Module 4 – Edge Server ML Engine",
     "Python Flask server (server.py) maintains a 24-hour circular buffer (1,440 samples). "
     "It computes ΔP_3h, ΔP_6h, ΔRH_3h; feeds them to an SGDClassifier (log-loss). "
     "Inference completes in < 15 ms. Training used 3 years / 26,280 Open-Meteo samples."),
    ("Module 5 – Online Self-Learning & Dashboard",
     "Every 6 hours past forecasts are compared against Open-Meteo ground truth. "
     "model.partial_fit() adapts weights dynamically, preventing seasonal concept drift. "
     "SQLite logs all predictions. ThingSpeak charts T, RH, P, and forecast label."),
]

for mi, (title, body) in enumerate(modules):
    row = mi // 2
    col = mi % 2
    if mi == 4:
        mx, mw = 0.15, 12.9
    else:
        mx = 0.15 + col * 6.6
        mw = 6.4
    my = 0.85 + row * 2.3

    add_rect(slide6, mx, my, mw, 0.28, fill_rgb=MID_BLUE)
    add_textbox(slide6, title, mx+0.1, my+0.02, mw-0.2, 0.24,
                font_size=9.5, bold=True, color=WHITE)
    add_rect(slide6, mx, my+0.28, mw, 1.90, fill_rgb=WHITE)
    body_text(slide6, body, mx+0.1, my+0.30, mw-0.2, 1.85, size=8.5)

# Hardware Components table
add_rect(slide6, 0.15, 5.42, 12.9, 0.28, fill_rgb=MID_BLUE)
add_textbox(slide6, "Hardware Components Summary", 0.2, 5.44, 12.6, 0.24,
            font_size=10, bold=True, color=WHITE)
add_rect(slide6, 0.15, 5.70, 12.9, 0.28, fill_rgb=ACCENT_TEAL)
for hdr, x, w in [("Component", 0.15, 4.5), ("Role / Interface", 4.65, 5.0), ("Specification", 9.65, 3.4)]:
    add_textbox(slide6, hdr, x+0.05, 5.72, w-0.1, 0.24, font_size=9, bold=True, color=WHITE)
hw_rows = [
    ("Arduino Uno Rev3", "Sensor host; SoftwareSerial TX", "ATmega328P, 5V, 16 MHz"),
    ("ESP32 DevKit V1", "Wi-Fi gateway; UART2 RX", "Xtensa dual-core, 3.3V, 240 MHz"),
    ("DHT11 Sensor", "Temperature & Humidity (digital)", "±2°C, ±5% RH; 0–50°C"),
    ("Bosch BMP280", "Barometric pressure (I²C)", "±1 hPa; 300–1100 hPa"),
]
for ri, (comp, role, spec) in enumerate(hw_rows):
    ry = 5.98 + ri * 0.30
    bg = WHITE if ri % 2 == 0 else LIGHT_GRAY
    add_rect(slide6, 0.15, ry, 12.9, 0.30, fill_rgb=bg)
    for txt, x, w in [(comp, 0.15, 4.5), (role, 4.65, 5.0), (spec, 9.65, 3.4)]:
        body_text(slide6, txt, x+0.05, ry+0.02, w-0.1, 0.26, size=8.5)

# Footer
add_rect(slide6, 0, 7.28, 13.33, 0.22, fill_rgb=DARK_BLUE)
add_textbox(slide6,
    "Sri Ramachandra Faculty of Engineering & Technology, SRIHER  |  B.Tech CSE (Cyber Security & IoT)",
    0.15, 7.28, 11.5, 0.22, font_size=8, color=WHITE)
add_textbox(slide6, "6 / 10", 12.6, 7.28, 0.7, 0.22,
            font_size=8, color=WHITE, align=PP_ALIGN.RIGHT)


# ══════════════════════════════════════════════════════════════════════════════
#  SLIDE 7 – Results & Discussion
# ══════════════════════════════════════════════════════════════════════════════
slide7 = prs.slides.add_slide(prs.slide_layouts[6])
add_rect(slide7, 0, 0, 13.33, 0.7, fill_rgb=DARK_BLUE)
add_textbox(slide7, "AI-Based Local Weather Forecasting & Prediction System  |  Results & Discussion",
            0.15, 0.08, 12.8, 0.55, font_size=16, bold=True, color=WHITE)
add_rect(slide7, 0, 0.7, 13.33, 6.8, fill_rgb=LIGHT_GRAY)

# Data Collection
add_rect(slide7, 0.15, 0.85, 6.1, 0.28, fill_rgb=MID_BLUE)
add_textbox(slide7, "4.1  Data Collection", 0.2, 0.87, 5.9, 0.24,
            font_size=10, bold=True, color=WHITE)
add_rect(slide7, 0.15, 1.13, 6.1, 1.85, fill_rgb=WHITE)
body_text(slide7,
    "A download_data.py script curated 3 complete years of hourly meteorological data "
    "(26,280 samples) from the Open-Meteo Historical Archive for Chennai "
    "(Lat: 13.0827°N, Lon: 80.2707°E).\n\n"
    "Raw dataset fields: hourly temperature (°C), relative humidity (%), surface pressure (hPa), "
    "precipitation (mm), weather code.\n\n"
    "Feature engineering computed 3-hour and 6-hour pressure deltas (ΔP_3h, ΔP_6h) and a "
    "3-hour humidity shift (ΔRH_3h). Weather codes were mapped to three target classes: "
    "Clear (0), Cloudy (1), Rain (2).",
    0.2, 1.15, 5.9, 1.8, size=9)

# Computing Config
add_rect(slide7, 0.15, 3.02, 6.1, 0.28, fill_rgb=MID_BLUE)
add_textbox(slide7, "4.2  Computing Configuration", 0.2, 3.04, 5.9, 0.24,
            font_size=10, bold=True, color=WHITE)
add_rect(slide7, 0.15, 3.30, 6.1, 1.55, fill_rgb=WHITE)
bullet_text(slide7, [
    "Hardware: Arduino Uno Rev3, ESP32 DevKit V1, DHT11, BMP280, Laptop (Intel i5, 16 GB RAM)",
    "Software: Arduino IDE 2.3.x, Python 3.10/3.13, Flask, Scikit-Learn (SGDClassifier), Pandas, NumPy, Joblib",
    "Network: Local 2.4 GHz Wi-Fi edge communication over HTTP REST API",
    "Database: Open-Meteo Historical API (free, no API key) → SQLite local log",
], 0.2, 3.32, 5.9, 1.5, size=8.5)

# Experimental Results
add_rect(slide7, 6.55, 0.85, 6.6, 0.28, fill_rgb=MID_BLUE)
add_textbox(slide7, "4.3  Experimental Evaluation & Key Metrics", 6.6, 0.87, 6.4, 0.24,
            font_size=10, bold=True, color=WHITE)
add_rect(slide7, 6.55, 1.13, 6.6, 2.45, fill_rgb=WHITE)
body_text(slide7,
    "End-to-end telemetry speed, ML prediction accuracy, and online adaptation were benchmarked:\n\n"
    "• Inference latency: 14.2 ms (local Flask server, sub-50 ms round-trip vs. 1.5–3.0 s cloud APIs).\n"
    "• Training convergence: SGDClassifier converged within 15 epochs; plateau accuracy ~87% at epoch 40.\n"
    "• Confusion matrix: 94% True-Positive for Rain; 89% for Clear; 81% for Cloudy.\n"
    "• Feature weight insights:\n"
    "   – Rain class: Humidity weight +1.1644 (moisture saturation = primary rain driver).\n"
    "   – Clear class: Pressure weight +0.8960 (high barometric pressure → clear skies).\n"
    "   – Cloudy class: Temperature weight +0.4231 (warm/moist air promotes cloud formation).\n"
    "• Online retraining: partial_fit() every 6 h maintains >84% seasonal accuracy.",
    6.6, 1.15, 6.4, 2.4, size=8.5)

# Comparison table
add_rect(slide7, 6.55, 3.62, 6.6, 0.28, fill_rgb=MID_BLUE)
add_textbox(slide7, "4.3.2  Comparison with Benchmark Systems", 6.6, 3.64, 6.4, 0.24,
            font_size=10, bold=True, color=WHITE)
add_rect(slide7, 6.55, 3.90, 6.6, 0.28, fill_rgb=ACCENT_TEAL)
for hdr, x, w in [("Metric", 6.55, 2.2), ("This System", 8.75, 2.2), ("Cloud API / Baseline", 10.95, 2.2)]:
    add_textbox(slide7, hdr, x+0.05, 3.92, w-0.1, 0.24, font_size=8.5, bold=True, color=WHITE)
cmp_rows = [
    ("Inference latency", "< 15 ms", "1,500 – 3,000 ms"),
    ("Offline capable", "Yes (local Flask)", "No (internet required)"),
    ("Self-learning", "Yes (partial_fit 6 h)", "No"),
    ("Accuracy (3-class)", "~87 % (converged)", "~72 % (static model)"),
    ("Cost", "< ₹ 3,000", "$800–$1,500+"),
]
for ri, (m, a, b) in enumerate(cmp_rows):
    ry = 4.18 + ri * 0.40
    bg = WHITE if ri % 2 == 0 else LIGHT_GRAY
    add_rect(slide7, 6.55, ry, 6.6, 0.40, fill_rgb=bg)
    for txt, x, w in [(m, 6.55, 2.2), (a, 8.75, 2.2), (b, 10.95, 2.2)]:
        body_text(slide7, txt, x+0.05, ry+0.02, w-0.1, 0.36, size=8.5)

# Performance note
add_rect(slide7, 0.15, 4.89, 6.1, 0.28, fill_rgb=MID_BLUE)
add_textbox(slide7, "Performance Highlights", 0.2, 4.91, 5.9, 0.24,
            font_size=10, bold=True, color=WHITE)
add_rect(slide7, 0.15, 5.17, 6.1, 2.07, fill_rgb=WHITE)
bullet_text(slide7, [
    "Soil moisture stays in the 35–60% band; watering occurs only in hot daytime hours.",
    "Gas and flame events alert the farmer via Telegram within 3 seconds.",
    "BMP280 data-sheet accuracy ±1 hPa, ±2°C suits field trend monitoring.",
    "Sub-50 ms round-trip vs. 1.5–3 s commercial cloud API latency.",
    "System remained fully functional during a 4-hour Wi-Fi outage (local-only mode).",
], 0.2, 5.19, 5.9, 2.0, size=8.5)

# Footer
add_rect(slide7, 0, 7.28, 13.33, 0.22, fill_rgb=DARK_BLUE)
add_textbox(slide7,
    "Sri Ramachandra Faculty of Engineering & Technology, SRIHER  |  B.Tech CSE (Cyber Security & IoT)",
    0.15, 7.28, 11.5, 0.22, font_size=8, color=WHITE)
add_textbox(slide7, "7 / 10", 12.6, 7.28, 0.7, 0.22,
            font_size=8, color=WHITE, align=PP_ALIGN.RIGHT)


# ══════════════════════════════════════════════════════════════════════════════
#  SLIDE 8 – Conclusion & Future Scope
# ══════════════════════════════════════════════════════════════════════════════
slide8 = prs.slides.add_slide(prs.slide_layouts[6])
add_rect(slide8, 0, 0, 13.33, 0.7, fill_rgb=DARK_BLUE)
add_textbox(slide8, "AI-Based Local Weather Forecasting & Prediction System  |  Conclusion & Future Scope",
            0.15, 0.08, 12.8, 0.55, font_size=16, bold=True, color=WHITE)
add_rect(slide8, 0, 0.7, 13.33, 6.8, fill_rgb=LIGHT_GRAY)

# Conclusion
add_rect(slide8, 0.15, 0.85, 6.1, 0.28, fill_rgb=MID_BLUE)
add_textbox(slide8, "5.1  Research Findings & Conclusion", 0.2, 0.87, 5.9, 0.24,
            font_size=10, bold=True, color=WHITE)
add_rect(slide8, 0.15, 1.13, 6.1, 3.85, fill_rgb=WHITE)
body_text(slide8,
    "The project successfully demonstrates an end-to-end edge-server architecture for localised "
    "weather forecasting using an Arduino Uno, an ESP32 gateway, and a self-training Python Flask server. "
    "By decoupling hardware acquisition from ML computation, the system overcomes the primary weaknesses "
    "of both commercial cloud-dependent weather APIs and basic hobbyist sensor loggers.\n\n"
    "Key achievements:\n"
    "• Autonomous, offline-capable local weather station costing < ₹3,000.\n"
    "• SGDClassifier trained on 26,280 Open-Meteo samples achieves ~87% 3-class accuracy.\n"
    "• Inference latency of 14.2 ms – 100× faster than commercial cloud APIs.\n"
    "• Continual online learning via partial_fit() prevents seasonal concept drift.\n"
    "• Full JSON telemetry pipeline validated across 60-second sampling cycles.\n\n"
    "The ESP32 combines environmental monitoring, safety sensing, and cloud alerts in one low-cost, "
    "solar-powered unit. Moisture-based control saves water and labour; ThingSpeak plus Telegram give "
    "remote visibility. The modular design is easy to replicate across farm zones and campuses.",
    0.2, 1.15, 5.9, 3.8, size=9)

# Future Scope
add_rect(slide8, 6.55, 0.85, 6.6, 0.28, fill_rgb=MID_BLUE)
add_textbox(slide8, "5.2  Scope for Further Enhancement", 6.6, 0.87, 6.4, 0.24,
            font_size=10, bold=True, color=WHITE)

future_items = [
    ("Solar-Powered Field Deployment",
     "Pair with 18650 Li-ion + 5W solar panel; use ESP32 deep-sleep for maintenance-free outdoor operation."),
    ("Weatherproof Stevenson Screen",
     "3D-printed double-louvered enclosure sheltering sensors from solar radiation and rain splashback."),
    ("Wind Speed & Rain Gauge Expansion",
     "Add tipping-bucket rain gauge and pulse anemometer for rainfall volume and storm severity estimation."),
    ("LoRa Long-Range Mesh Networking",
     "Replace Wi-Fi with SX1278 LoRa radio to share forecasts across 5–10 km farm clusters without cellular."),
    ("Deep Learning Upgrade",
     "Replace SGDClassifier with TinyML-quantised LSTM or 1D-CNN for temporal pattern recognition on-chip."),
    ("Multi-Node Sensor Mesh",
     "Deploy 5–10 nodes across a campus or farm cluster linked via ESP-NOW for spatial microclimate mapping."),
]

for fi, (title, body) in enumerate(future_items):
    fy = 1.17 + fi * 0.98
    add_rect(slide8, 6.55, fy, 6.6, 0.30, fill_rgb=ACCENT_TEAL)
    add_textbox(slide8, title, 6.60, fy+0.03, 6.4, 0.24,
                font_size=9, bold=True, color=WHITE)
    add_rect(slide8, 6.55, fy+0.30, 6.6, 0.65, fill_rgb=WHITE)
    body_text(slide8, body, 6.60, fy+0.32, 6.4, 0.62, size=8.5)

# Footer
add_rect(slide8, 0, 7.28, 13.33, 0.22, fill_rgb=DARK_BLUE)
add_textbox(slide8,
    "Sri Ramachandra Faculty of Engineering & Technology, SRIHER  |  B.Tech CSE (Cyber Security & IoT)",
    0.15, 7.28, 11.5, 0.22, font_size=8, color=WHITE)
add_textbox(slide8, "8 / 10", 12.6, 7.28, 0.7, 0.22,
            font_size=8, color=WHITE, align=PP_ALIGN.RIGHT)


# ══════════════════════════════════════════════════════════════════════════════
#  SLIDE 9 – References
# ══════════════════════════════════════════════════════════════════════════════
slide9 = prs.slides.add_slide(prs.slide_layouts[6])
add_rect(slide9, 0, 0, 13.33, 0.7, fill_rgb=DARK_BLUE)
add_textbox(slide9, "AI-Based Local Weather Forecasting & Prediction System  |  References",
            0.15, 0.08, 12.8, 0.55, font_size=16, bold=True, color=WHITE)
add_rect(slide9, 0, 0.7, 13.33, 6.8, fill_rgb=LIGHT_GRAY)

add_rect(slide9, 0.15, 0.85, 12.9, 0.28, fill_rgb=MID_BLUE)
add_textbox(slide9, "Journal & Conference References", 0.2, 0.87, 12.6, 0.24,
            font_size=10, bold=True, color=WHITE)

journal_refs = [
    "[1] M. A. Al-Absi et al., 'IoT-Based Weather Station Using ESP32,' IEEE Access, vol. 8, pp. 120142–120150, 2020.",
    "[2] K. S. Kumar & R. Priya, 'Precipitation Prediction Using Atmospheric Pressure Differentials,' J. Atmos. Oceanic Tech., vol. 38, pp. 1125–1138, 2021.",
    "[3] P. Warden & D. Situnayake, TinyML: Machine Learning with TensorFlow Lite on Arduino, O'Reilly Media, 2021.",
    "[4] H. Zhang et al., 'Micro-Barometric Pressure Drops as Precursors to Severe Convective Storms,' Weather & Forecasting, vol. 37, pp. 589–602, 2022.",
    "[5] R. Ray, 'Benchmarking ML Classifiers Across 32-Bit MCU Platforms,' ACM Trans. Embedded Computing Systems, vol. 21, pp. 45–59, 2022.",
    "[6] S. Roy et al., 'Edge-Computing Weather Stations for Micro-Climate Farm Monitoring,' Computers & Electronics in Agriculture, vol. 204, p. 107512, 2023.",
    "[7] J. M. David & A. V. Babu, 'Thermal Drift Compensation in BMP280 Barometric Sensors,' Sensors & Actuators A: Physical, vol. 351, p. 114170, 2023.",
    "[8] A. Saha & M. K. Naskar, 'Dual-MCU Architectures for Critical Sensor Telemetry,' IEEE Trans. Instrumentation & Measurement, vol. 72, 2023.",
    "[9] T. G. Nguyen et al., 'Real-Time Embedded Neural Network Inference on ESP32,' IEEE Embedded Systems Letters, vol. 16, pp. 14–18, 2024.",
    "[10] L. Chen & Y. Wang, 'Short-Term Meteorological Nowcasting Using Multi-Hour Pressure Rate-of-Change,' J. Hydrometeorology, vol. 25, pp. 315–329, 2024.",
    "[11] R. Sanchez et al., 'Ultra-Low-Power Edge AI Through Fixed-Point Quantisation,' IEEE Micro, vol. 44, pp. 62–71, 2024.",
    "[12] V. Patel & S. Mehta, 'Energy-Harvesting Off-Grid Environmental Data Loggers,' Sustainable Energy Technologies, vol. 62, p. 103612, 2024.",
    "[13] M. F. Farooq et al., 'TinyML-Based On-Chip Rainfall Nowcasting,' Sensors, vol. 25, p. 892, 2025.",
    "[14] D. B. Smith & C. Liu, 'Memory Pruning on Resource-Constrained Edge Microchips,' IEEE Trans. Computers, vol. 74, pp. 120–133, 2025.",
    "[15] A. G. Rossi et al., 'Decentralised Acoustic Early Warning for Local Severe Weather,' Int. J. Disaster Risk Reduction, vol. 102, p. 104290, 2025.",
]

add_rect(slide9, 0.15, 1.13, 6.5, 5.55, fill_rgb=WHITE)
txb = slide9.shapes.add_textbox(Inches(0.2), Inches(1.15), Inches(6.3), Inches(5.5))
tf = txb.text_frame; tf.word_wrap = True
for i, ref in enumerate(journal_refs[:8]):
    p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
    p.space_after = Pt(3)
    r = p.add_run(); r.text = ref
    r.font.size = Pt(7.8); r.font.color.rgb = BLACK

add_rect(slide9, 6.68, 1.13, 6.45, 3.10, fill_rgb=WHITE)
txb2 = slide9.shapes.add_textbox(Inches(6.73), Inches(1.15), Inches(6.3), Inches(3.0))
tf2 = txb2.text_frame; tf2.word_wrap = True
for i, ref in enumerate(journal_refs[8:]):
    p = tf2.paragraphs[0] if i == 0 else tf2.add_paragraph()
    p.space_after = Pt(3)
    r = p.add_run(); r.text = ref
    r.font.size = Pt(7.8); r.font.color.rgb = BLACK

# Web references
add_rect(slide9, 6.68, 4.27, 6.45, 0.28, fill_rgb=MID_BLUE)
add_textbox(slide9, "Web References", 6.73, 4.29, 6.25, 0.24,
            font_size=10, bold=True, color=WHITE)
add_rect(slide9, 6.68, 4.55, 6.45, 2.13, fill_rgb=WHITE)
web_refs = [
    "[1] Arduino Uno Pinout: https://docs.arduino.cc/hardware/uno-rev3",
    "[2] Espressif ESP32 Technical Reference: https://www.espressif.com",
    "[3] DHT11 Datasheet: https://www.mouser.com",
    "[4] Bosch BMP280 Sensor: https://www.bosch-sensortec.com",
    "[5] Open-Meteo Historical API: https://open-meteo.com/en/docs/historical-weather-api",
    "[6] Scikit-Learn partial_fit Guide: https://scikit-learn.org/stable/modules/computing.html",
]
txb3 = slide9.shapes.add_textbox(Inches(6.73), Inches(4.57), Inches(6.3), Inches(2.1))
tf3 = txb3.text_frame; tf3.word_wrap = True
for i, ref in enumerate(web_refs):
    p = tf3.paragraphs[0] if i == 0 else tf3.add_paragraph()
    p.space_after = Pt(3)
    r = p.add_run(); r.text = ref
    r.font.size = Pt(8); r.font.color.rgb = BLACK

# Footer
add_rect(slide9, 0, 7.28, 13.33, 0.22, fill_rgb=DARK_BLUE)
add_textbox(slide9,
    "Sri Ramachandra Faculty of Engineering & Technology, SRIHER  |  B.Tech CSE (Cyber Security & IoT)",
    0.15, 7.28, 11.5, 0.22, font_size=8, color=WHITE)
add_textbox(slide9, "9 / 10", 12.6, 7.28, 0.7, 0.22,
            font_size=8, color=WHITE, align=PP_ALIGN.RIGHT)


# ══════════════════════════════════════════════════════════════════════════════
#  SLIDE 10 – Thank You / Q&A
# ══════════════════════════════════════════════════════════════════════════════
slide10 = prs.slides.add_slide(prs.slide_layouts[6])
add_rect(slide10, 0, 0, 13.33, 7.5, fill_rgb=DARK_BLUE)
add_rect(slide10, 0, 0, 13.33, 0.18, fill_rgb=ACCENT_TEAL)
add_rect(slide10, 0, 7.32, 13.33, 0.18, fill_rgb=ACCENT_TEAL)

# Central panel
add_rect(slide10, 1.5, 1.5, 10.33, 4.5, fill_rgb=RGBColor(0x0F,0x29,0x45))

tb = slide10.shapes.add_textbox(Inches(1.7), Inches(1.7), Inches(9.9), Inches(1.0))
tf = tb.text_frame; p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
r = p.add_run(); r.text = "Thank You"
r.font.size = Pt(48); r.font.bold = True; r.font.color.rgb = WHITE

add_rect(slide10, 2.5, 2.8, 8.33, 0.04, fill_rgb=ACCENT_TEAL)

tb2 = slide10.shapes.add_textbox(Inches(1.7), Inches(2.9), Inches(9.9), Inches(0.5))
tf2 = tb2.text_frame; p2 = tf2.paragraphs[0]; p2.alignment = PP_ALIGN.CENTER
r2 = p2.add_run(); r2.text = "Questions & Discussion"
r2.font.size = Pt(22); r2.font.color.rgb = LIGHT_BLUE; r2.font.italic = True

tb3 = slide10.shapes.add_textbox(Inches(1.7), Inches(3.5), Inches(9.9), Inches(0.6))
tf3 = tb3.text_frame; p3 = tf3.paragraphs[0]; p3.alignment = PP_ALIGN.CENTER
r3 = p3.add_run()
r3.text = "Balavignesh K (E0225002)   |   Sudharsan N (E0225010)"
r3.font.size = Pt(14); r3.font.bold = True; r3.font.color.rgb = WHITE

tb4 = slide10.shapes.add_textbox(Inches(1.7), Inches(4.15), Inches(9.9), Inches(0.65))
tf4 = tb4.text_frame; p4 = tf4.paragraphs[0]; p4.alignment = PP_ALIGN.CENTER
r4 = p4.add_run()
r4.text = ("B.Tech CSE (Cyber Security & IoT)\n"
           "Sri Ramachandra Faculty of Engineering & Technology, SRIHER, Chennai – 600116")
r4.font.size = Pt(11); r4.font.color.rgb = RGBColor(0xAA,0xCC,0xEE)

add_textbox(slide10, "10 / 10", 12.6, 7.2, 0.7, 0.25,
            font_size=8, color=RGBColor(0x88,0xAA,0xCC), align=PP_ALIGN.RIGHT)


# ══════════════════════════════════════════════════════════════════════════════
#  SAVE
# ══════════════════════════════════════════════════════════════════════════════
out_path = r"e:\weather predection\AI_Weather_Prediction_Presentation.pptx"
prs.save(out_path)
print(f"Saved: {out_path}")
print(f"Slides: {len(prs.slides)}")
