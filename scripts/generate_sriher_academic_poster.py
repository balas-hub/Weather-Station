"""
Academic conference poster (single PPTX slide) matching the ESP32 agriculture
poster layout, using content and figures from
AI_Weather_Prediction_Project_Report.docx.
"""
from __future__ import annotations

import os

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from PIL import Image
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import nsmap, qn
from pptx.util import Emu, Inches, Pt
from lxml import etree

BASE = r"E:\weather predection"
ASSET = os.path.join(BASE, "poster_assets", "from_report")
DIAG = os.path.join(BASE, "poster_assets", "poster_diagrams")
os.makedirs(DIAG, exist_ok=True)

# ---------------------------------------------------------------------------
# Palette — matched to the agriculture poster
# ---------------------------------------------------------------------------
NAVY = RGBColor(0x1E, 0x5A, 0x96)
NAVY_DEEP = RGBColor(0x16, 0x4A, 0x7E)
HEADER_BLUE = RGBColor(0x1E, 0x6B, 0xB5)
SECTION = RGBColor(0x1E, 0x5A, 0x96)
BG = RGBColor(0xE6, 0xEE, 0xF6)
CARD = RGBColor(0xFF, 0xFF, 0xFF)
BORDER = RGBColor(0xB8, 0xC9, 0xDB)
TEXT = RGBColor(0x1A, 0x1A, 0x1A)
MUTED = RGBColor(0x4A, 0x55, 0x63)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
SUB = RGBColor(0xC5, 0xDE, 0xF5)
ROW_ALT = RGBColor(0xEE, 0xF4, 0xFA)
ACCENT = RGBColor(0x0F, 0x4C, 0x81)

W, H = 36.0, 24.0  # inches — standard landscape academic poster


def set_round(shape, adj=0.04):
    try:
        spPr = shape._element.spPr
        prst = spPr.find(qn("a:prstGeom"))
        if prst is None:
            return
        avLst = prst.find(qn("a:avLst"))
        if avLst is None:
            avLst = etree.SubElement(prst, qn("a:avLst"))
        gd = etree.SubElement(avLst, qn("a:gd"))
        gd.set("name", "adj")
        gd.set("fmla", f"val {int(adj * 100000)}")
    except Exception:
        pass


def generate_architecture():
    """Agriculture-style four-block architecture (Fig. 1)."""
    fig, ax = plt.subplots(figsize=(10.2, 4.35), dpi=220)
    fig.patch.set_facecolor("white")
    ax.set_xlim(0, 10.2)
    ax.set_ylim(0, 4.4)
    ax.axis("off")

    def box(x, y, w, h, fc, ec, title, lines, title_fc="#0F3D6E"):
        r = mpatches.FancyBboxPatch(
            (x, y), w, h, boxstyle="round,pad=0.04,rounding_size=0.12",
            facecolor=fc, edgecolor=ec, linewidth=1.6,
        )
        ax.add_patch(r)
        ax.text(x + w / 2, y + h - 0.28, title, ha="center", va="center",
                fontsize=10, fontweight="bold", color=title_fc)
        yy = y + h - 0.58
        for ln in lines:
            ax.text(x + w / 2, yy, ln, ha="center", va="top", fontsize=8.1, color="#1F2937")
            yy -= 0.28

    def arrow(x1, y1, x2, y2):
        ax.annotate(
            "", xy=(x2, y2), xytext=(x1, y1),
            arrowprops=dict(arrowstyle="-|>", color="#1E5A96", lw=1.8,
                            mutation_scale=12),
        )

    box(0.18, 1.55, 2.28, 2.15, "#DBEAFE", "#2563EB", "SENSING",
        ["DHT11  temp + humidity", "BMP280  pressure (I²C)", "1-minute sampling cycle"])
    box(2.78, 1.55, 2.28, 2.15, "#DCFCE7", "#059669", "BRAIN",
        ["Arduino Uno  MCU", "JSON telemetry pack", "UART 9600 baud"])
    box(5.38, 1.55, 2.28, 2.15, "#FEF3C7", "#D97706", "GATEWAY",
        ["ESP32 DevKit V1", "Wi-Fi HTTP POST", "Alert flag parse"])
    box(7.98, 1.55, 2.05, 2.15, "#EDE9FE", "#7C3AED", "EDGE + CLOUD",
        ["Flask server.py", "SGDClassifier ML", "Dashboard + alerts"])

    arrow(2.46, 2.62, 2.78, 2.62)
    arrow(5.06, 2.62, 5.38, 2.62)
    arrow(7.66, 2.62, 7.98, 2.62)

    box(0.18, 0.18, 4.88, 1.15, "#F1F5F9", "#64748B", "POWER / HOST",
        ["USB 5 V rail  ·  common GND  ·  laptop (i5 / 16 GB) Flask host  ·  local 2.4 GHz Wi-Fi"])
    box(5.22, 0.18, 4.80, 1.15, "#FEE2E2", "#DC2626", "ACTION",
        ["Rain probability ≥ 60%  →  JSON alert to ESP32  ·  web gauges  ·  6 h partial_fit()"])

    path = os.path.join(DIAG, "fig1_architecture.png")
    fig.savefig(path, bbox_inches="tight", pad_inches=0.08, facecolor="white")
    plt.close(fig)
    return path


def generate_prototype():
    """Labeled prototype layout in the style of agriculture Fig. 3."""
    fig, ax = plt.subplots(figsize=(10.2, 3.55), dpi=220)
    fig.patch.set_facecolor("#F8FAFC")
    ax.set_xlim(0, 10.2)
    ax.set_ylim(0, 3.6)
    ax.axis("off")

    items = [
        (0.25, "#93C5FD", "1  DHT11", "GPIO 2\nT + RH"),
        (2.25, "#A5B4FC", "2  BMP280", "I²C A4/A5\nPressure"),
        (4.25, "#86EFAC", "3  Arduino Uno", "Sensor MCU\nJSON @ 1 min"),
        (6.25, "#FCD34D", "4  ESP32", "Wi-Fi gateway\nGPIO 16/17"),
        (8.25, "#F9A8D4", "5  Laptop", "Flask ML\n:5000 dashboard"),
    ]
    for x, c, title, sub in items:
        r = mpatches.FancyBboxPatch(
            (x, 1.15), 1.72, 1.85, boxstyle="round,pad=0.04,rounding_size=0.1",
            facecolor=c, edgecolor="#334155", linewidth=1.2,
        )
        ax.add_patch(r)
        ax.text(x + 0.86, 2.55, title, ha="center", va="center", fontsize=9.5,
                fontweight="bold", color="#0F172A")
        ax.text(x + 0.86, 1.85, sub, ha="center", va="center", fontsize=8.0, color="#1E293B")

    for x in (1.97, 3.97, 5.97, 7.97):
        ax.annotate("", xy=(x + 0.28, 2.05), xytext=(x, 2.05),
                    arrowprops=dict(arrowstyle="-|>", color="#1E5A96", lw=1.6, mutation_scale=11))

    ax.text(5.1, 0.45,
            "Direct UART (Uno 11→ESP32 GPIO16, Uno 10←GPIO17)  ·  common GND  ·  local Wi-Fi HTTP POST",
            ha="center", va="center", fontsize=8.2, color="#334155")
    path = os.path.join(DIAG, "fig3_prototype.png")
    fig.savefig(path, bbox_inches="tight", pad_inches=0.08, facecolor="#F8FAFC")
    plt.close(fig)
    return path


def add_rect(slide, l, t, w, h, fill, line=None, rounded=False):
    shp = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE if rounded else MSO_SHAPE.RECTANGLE,
        Inches(l), Inches(t), Inches(w), Inches(h),
    )
    shp.fill.solid()
    shp.fill.fore_color.rgb = fill
    if line is None:
        shp.line.fill.background()
    else:
        shp.line.color.rgb = line
        shp.line.width = Pt(0.9)
    shp.shadow.inherit = False
    if rounded:
        set_round(shp, 0.045)
    return shp


def add_tb(slide, l, t, w, h, anchor=MSO_ANCHOR.TOP):
    tb = slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = Inches(0.06)
    tf.margin_right = Inches(0.06)
    tf.margin_top = Inches(0.03)
    tf.margin_bottom = Inches(0.03)
    return tf


def run(p, text, size=10, bold=False, color=TEXT, italic=False, name="Calibri"):
    r = p.add_run()
    r.text = text
    r.font.size = Pt(size)
    r.font.bold = bold
    r.font.italic = italic
    r.font.color.rgb = color
    r.font.name = name
    return r


def set_p(p, size, bold=False, color=TEXT, align=PP_ALIGN.LEFT,
          after=2.0, before=0.0, italic=False):
    p.alignment = align
    p.space_after = Pt(after)
    p.space_before = Pt(before)
    p.font.size = Pt(size)
    p.font.bold = bold
    p.font.italic = italic
    p.font.color.rgb = color
    p.font.name = "Calibri"


def card(slide, l, t, w, h, title):
    """White panel with navy section bar — agriculture poster look."""
    body = add_rect(slide, l, t, w, h, CARD, BORDER, rounded=True)
    hdr = add_rect(slide, l, t, w, 0.38, SECTION, rounded=True)
    set_round(hdr, 0.08)
    # square off bottom of header so it sits flush on the card
    add_rect(slide, l, t + 0.20, w, 0.18, SECTION, rounded=False)
    tf = add_tb(slide, l + 0.04, t + 0.02, w - 0.08, 0.34, MSO_ANCHOR.MIDDLE)
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.LEFT
    run(p, title, 13, bold=True, color=WHITE, name="Calibri")
    return body


def fit_picture(slide, path, l, t, max_w, max_h):
    img = Image.open(path)
    iw, ih = img.size
    ar = ih / float(iw)
    w = max_w
    h = w * ar
    if h > max_h:
        h = max_h
        w = h / ar
    left = l + (max_w - w) / 2.0
    top = t + (max_h - h) / 2.0
    return slide.shapes.add_picture(path, Inches(left), Inches(top), Inches(w), Inches(h))


def style_table(table, header=True):
    for ri, row in enumerate(table.rows):
        for cell in row.cells:
            cell.margin_left = Inches(0.05)
            cell.margin_right = Inches(0.05)
            cell.margin_top = Inches(0.03)
            cell.margin_bottom = Inches(0.03)
            for p in cell.text_frame.paragraphs:
                p.font.name = "Calibri"
                p.font.size = Pt(9.0 if ri else 9.5)
                p.font.bold = (ri == 0) or False
                p.font.color.rgb = WHITE if ri == 0 else TEXT
            fill = SECTION if ri == 0 else (ROW_ALT if ri % 2 else CARD)
            cell.fill.solid()
            cell.fill.fore_color.rgb = fill
            tc = cell._tc
            tcPr = tc.get_or_add_tcPr()
            ln = etree.SubElement(tcPr, qn("a:lnL"))
            ln.set("w", "6350")
            etree.SubElement(ln, qn("a:solidFill")).append(
                etree.Element(qn("a:srgbClr"), val="C5D4E3")
            )


def fill_cell(cell, text, size=9.0, bold=False, color=TEXT, align=PP_ALIGN.LEFT):
    cell.text_frame.clear()
    cell.text_frame.word_wrap = True
    p = cell.text_frame.paragraphs[0]
    p.alignment = align
    r = p.add_run()
    r.text = text
    r.font.size = Pt(size)
    r.font.bold = bold
    r.font.color.rgb = color
    r.font.name = "Calibri"


def build():
    arch = generate_architecture()
    proto = generate_prototype()
    flow = os.path.join(ASSET, "image4.png")
    circuit = os.path.join(ASSET, "image5.png")
    results = os.path.join(ASSET, "image6.png")

    prs = Presentation()
    prs.slide_width = Inches(W)
    prs.slide_height = Inches(H)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    add_rect(slide, 0, 0, W, H, BG)
    add_rect(slide, 0, 0, W, 1.72, HEADER_BLUE)
    add_rect(slide, 0, 1.72, W, 0.06, NAVY_DEEP)

    tf = add_tb(slide, 0.35, 0.08, 35.3, 0.72, MSO_ANCHOR.MIDDLE)
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    run(p, "AI-Based Local Weather Forecasting and Prediction System Using Arduino Uno and ESP32",
        28, bold=True, color=WHITE, name="Calibri")

    tf = add_tb(slide, 0.35, 0.78, 35.3, 0.38)
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    run(p, "Dual-MCU edge nowcasting with DHT11 + BMP280 sensing, Flask self-training ML, and local storm alerts",
        15, color=SUB, name="Calibri")

    tf = add_tb(slide, 0.35, 1.16, 35.3, 0.44)
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    run(p, "Balavignesh K  –  E0225002    |    Sudharsan N  –  E0225010    |    "
           "Sri Ramachandra Faculty of Engineering and Technology, SRIHER, Porur, Chennai – 600116    |    "
           "Supervisor: Mr. Manoj Kumaran",
        12, bold=True, color=RGBColor(0xE8, 0xF1, 0xFA), name="Calibri")

    m = 0.22
    gap = 0.16
    usable = W - 2 * m
    cw = (usable - 3 * gap) / 4.0
    xs = [m + i * (cw + gap) for i in range(4)]
    y0 = 1.92
    yb = 23.78
    # four columns of equal height
    col_h = yb - y0

    # =====================================================================
    # COLUMN 1  Abstract / Intro / Objectives
    # =====================================================================
    x = xs[0]
    h_abs, h_intro, h_obj = 4.55, 8.35, col_h - 4.55 - 8.35 - 0.20
    card(slide, x, y0, cw, h_abs, "Abstract")
    tf = add_tb(slide, x + 0.04, y0 + 0.42, cw - 0.08, h_abs - 0.48)
    p = tf.paragraphs[0]
    set_p(p, 10.5, after=5)
    run(p,
        "Generic weather apps miss localized microclimates and neighborhood storms, "
        "pulling data from regional airports 15–25 km away. Internet-reliant devices "
        "fail during storm outages. This work presents a low-cost, dual-microcontroller "
        "edge-server system: an Arduino Uno samples DHT11 temperature/humidity and "
        "Bosch BMP280 pressure every 60 s, an ESP32 forwards JSON over local Wi-Fi, "
        "and a Python Flask server with a self-training SGDClassifier forecasts "
        "Clear / Cloudy / Rain. Rain odds above 60% raise an instant alert; every "
        "6 hours the model verifies forecasts against outdoor truth and updates "
        "weights with partial_fit() — all on the local network, with zero cloud cost.")

    y = y0 + h_abs + 0.10
    card(slide, x, y, cw, h_intro, "Introduction & Problem")
    tf = add_tb(slide, x + 0.04, y + 0.42, cw - 0.08, h_intro - 0.48)
    bullets = [
        "NWP models use 15–25 km grids; they miss convective cloudbursts and street-scale humidity spikes.",
        "Cloud stations (Ambient Weather, Netatmo) stop updating when storms cut internet — exactly when forecasts are needed.",
        "Commercial AWS units (Davis Vantage Pro2) cost $800–$1500 and log data without predictive ML.",
        "Hobbyist stations read only instantaneous T/RH and ignore barometric tendency (ΔP/Δt), the primary rain precursor.",
        "Zambretti mechanical rules stay offline but achieve only ~64% real-world accuracy.",
        "Raspberry Pi weather nodes draw 2.5–5 W, self-heat the sensors, and risk SD-card corruption.",
    ]
    for i, b in enumerate(bullets):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        set_p(p, 10.2, after=5)
        run(p, "•  " + b)
    p = tf.add_paragraph()
    set_p(p, 10.5, bold=True, color=NAVY, after=3, before=7)
    run(p, "Problem statement:  ", bold=True, color=NAVY, size=10.5)
    run(p,
        "How can a low-cost, energy-local dual-MCU node sense temperature, humidity "
        "and pressure, forecast rain on a nearby Flask server, and keep learning "
        "from ground truth — without the internet?",
        size=10.5, color=NAVY)

    y = y + h_intro + 0.10
    card(slide, x, y, cw, h_obj, "Objectives")
    tf = add_tb(slide, x + 0.04, y + 0.42, cw - 0.08, h_obj - 0.48)
    objs = [
        "Sample temperature, relative humidity and barometric pressure at a steady 1-minute rate (DHT11 GPIO, BMP280 I²C 16× oversampling).",
        "Stream compact JSON from Arduino Uno to ESP32 over direct UART (Pins 10/11 ↔ GPIO 16/17, common GND) and POST to a local Flask host.",
        "Engineer ΔP_3h, ΔP_6h and ΔRH_3h from a 24-hour circular buffer (1 440 samples) and classify Clear / Cloudy / Rain with an SGDClassifier (log-loss).",
        "Raise a JSON alert when rain probability ≥ 60%, with end-to-end inference under 15 ms.",
        "Retrain automatically every 6 hours via model.partial_fit() against observed outdoor weather, preventing seasonal concept drift.",
    ]
    for i, o in enumerate(objs):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        set_p(p, 10.2, after=5)
        run(p, f"{i + 1}.  ", bold=True, color=NAVY, size=10.2)
        run(p, o, size=10.2)

    # =====================================================================
    # COLUMN 2  Methodology + Architecture
    # =====================================================================
    x = xs[1]
    h_meth, h_arch = 9.55, col_h - 9.55 - 0.10
    card(slide, x, y0, cw, h_meth, "Proposed Methodology")
    tf = add_tb(slide, x + 0.04, y0 + 0.40, cw - 0.08, 4.55)
    steps = [
        ("1. Sense: ",
         "Arduino Uno samples DHT11 (T, RH) and BMP280 (P, 16× OSR + IIR) every 60 s, fuses temperatures, and emits compact JSON."),
        ("2. Bridge: ",
         "SoftwareSerial TX Pin 11 → ESP32 GPIO 16 (RX2); Pin 10 ← GPIO 17; 9600 baud; shared ground. No extra level-shifter IC."),
        ("3. Dispatch: ",
         "ESP32 POSTs each packet to http://<laptop>:5000/api/weather over local 2.4 GHz Wi-Fi and parses prediction, rain odds and alert."),
        ("4. Infer: ",
         "Flask keeps a 24 h ring buffer, computes ΔP_3h / ΔP_6h / ΔRH_3h, scales a 6-D vector, and runs SGDClassifier in < 15 ms."),
        ("5. Learn: ",
         "Every 6 hours the server checks past forecasts against outdoor truth and calls partial_fit(), then joblib-dumps the updated weights."),
    ]
    for i, (lab, body) in enumerate(steps):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        set_p(p, 10.2, after=4)
        run(p, lab, bold=True, color=NAVY, size=10.2)
        run(p, body, size=10.2)

    # parameter table
    tbl_shape = slide.shapes.add_table(6, 2, Inches(x + 0.12), Inches(y0 + 5.05),
                                       Inches(cw - 0.24), Inches(4.28))
    tbl = tbl_shape.table
    tbl.columns[0].width = Inches((cw - 0.24) * 0.38)
    tbl.columns[1].width = Inches((cw - 0.24) * 0.62)
    rows = [
        ("Control parameter", "Rule / value"),
        ("Sampling", "Every 60 s on Uno (non-blocking millis())"),
        ("UART link", "9600 baud · Pins 10/11 ↔ GPIO 16/17"),
        ("HTTP POST", "Flask /api/weather on local Wi-Fi"),
        ("Rain alert", "Rain probability ≥ 60%"),
        ("Self-learning", "partial_fit() every 6 h vs ground truth"),
    ]
    for ri, (a, b) in enumerate(rows):
        fill_cell(tbl.cell(ri, 0), a, 9.2, bold=True, color=WHITE if ri == 0 else TEXT)
        fill_cell(tbl.cell(ri, 1), b, 9.2, bold=(ri == 0), color=WHITE if ri == 0 else TEXT)
    style_table(tbl)

    y = y0 + h_meth + 0.10
    card(slide, x, y, cw, h_arch, "System Architecture")
    img_h = h_arch - 1.05
    if os.path.exists(arch):
        fit_picture(slide, arch, x + 0.10, y + 0.44, cw - 0.20, img_h * 0.46)
    if os.path.exists(flow):
        fit_picture(slide, flow, x + 0.10, y + 0.44 + img_h * 0.46 + 0.04, cw - 0.20, img_h * 0.50)
    cap = add_tb(slide, x + 0.08, y + h_arch - 0.58, cw - 0.16, 0.52)
    p = cap.paragraphs[0]
    set_p(p, 8.6, italic=True, color=MUTED, after=0)
    run(p, "Fig. 1. Block diagram (sensing → Uno → ESP32 → Flask) and workflow: 1-minute cycle, ΔP features, rain-alert branch, 6-hour self-learning loop.",
        8.6, italic=True, color=MUTED)

    # =====================================================================
    # COLUMN 3  Hardware + Circuit
    # =====================================================================
    x = xs[2]
    h_hw, h_ckt = 7.05, col_h - 7.05 - 0.10
    card(slide, x, y0, cw, h_hw, "Hardware Components")
    hw = slide.shapes.add_table(8, 3, Inches(x + 0.10), Inches(y0 + 0.48),
                                Inches(cw - 0.20), Inches(6.42))
    ht = hw.table
    ht.columns[0].width = Inches((cw - 0.20) * 0.32)
    ht.columns[1].width = Inches((cw - 0.20) * 0.40)
    ht.columns[2].width = Inches((cw - 0.20) * 0.28)
    hw_rows = [
        ("Component", "Role", "Interface"),
        ("Arduino Uno Rev3", "Sensor node; JSON pack", "UART + I²C"),
        ("ESP32 DevKit V1", "Wi-Fi gateway; alert parse", "UART + Wi-Fi"),
        ("DHT11", "Temperature + humidity", "Digital GPIO 2"),
        ("Bosch BMP280", "Barometric pressure ±0.12 hPa", "I²C A4 SDA / A5 SCL"),
        ("Laptop i5 / 16 GB", "Flask edge ML + dashboard", "HTTP :5000"),
        ("UART pair 10/11", "Inter-MCU telemetry", "9600 baud, common GND"),
        ("Local 2.4 GHz AP", "Edge LAN, no cloud", "Wi-Fi STA"),
    ]
    for ri, row in enumerate(hw_rows):
        for ci, val in enumerate(row):
            fill_cell(ht.cell(ri, ci), val, 9.0, bold=(ri == 0 or ci == 0),
                      color=WHITE if ri == 0 else TEXT)
    style_table(ht)

    y = y0 + h_hw + 0.10
    card(slide, x, y, cw, h_ckt, "Circuit Diagram")
    if os.path.exists(circuit):
        fit_picture(slide, circuit, x + 0.10, y + 0.44, cw - 0.20, h_ckt - 1.22)
    cap = add_tb(slide, x + 0.08, y + h_ckt - 0.74, cw - 0.16, 0.68)
    p = cap.paragraphs[0]
    set_p(p, 8.5, italic=True, color=MUTED, after=1)
    run(p, "Fig. 2. Direct wiring. DHT11: 5 V, DATA→D2, GND. BMP280: 3.3 V, SCL→A5, SDA→A4. "
           "Uno Pin 11 → ESP32 GPIO 16; Pin 10 ← GPIO 17; shared GND. Analog sensors stay on 5 V/3.3 V rails.",
        8.5, italic=True, color=MUTED)

    # =====================================================================
    # COLUMN 4  Prototype / Results / Analysis / Close
    # =====================================================================
    x = xs[3]
    h_proto, h_res, h_perf, h_conc, h_fut, h_ref = 3.55, 4.85, 3.55, 2.55, 2.35, 0
    h_ref = col_h - (h_proto + h_res + h_perf + h_conc + h_fut) - 0.50

    card(slide, x, y0, cw, h_proto, "Prototype Design")
    if os.path.exists(proto):
        fit_picture(slide, proto, x + 0.08, y0 + 0.42, cw - 0.16, h_proto - 0.92)
    cap = add_tb(slide, x + 0.08, y0 + h_proto - 0.48, cw - 0.16, 0.42)
    p = cap.paragraphs[0]
    set_p(p, 8.4, italic=True, color=MUTED, after=0)
    run(p, "Fig. 3. Prototype chain: 1 DHT11, 2 BMP280, 3 Uno, 4 ESP32, 5 Flask laptop. UART + local Wi-Fi only.",
        8.4, italic=True, color=MUTED)

    y = y0 + h_proto + 0.10
    card(slide, x, y, cw, h_res, "Results & Performance")
    if os.path.exists(results):
        fit_picture(slide, results, x + 0.08, y + 0.42, cw - 0.16, h_res - 0.92)
    cap = add_tb(slide, x + 0.08, y + h_res - 0.48, cw - 0.16, 0.42)
    p = cap.paragraphs[0]
    set_p(p, 8.4, italic=True, color=MUTED, after=0)
    run(p, "Fig. 4. (left) SGD convergence to 86.4% validation; (right) test confusion, 2 852 events, rain recall 92.3%.",
        8.4, italic=True, color=MUTED)

    y = y + h_res + 0.10
    card(slide, x, y, cw, h_perf, "Performance Analysis")
    tf = add_tb(slide, x + 0.04, y + 0.40, cw - 0.08, h_perf - 0.46)
    perfs = [
        "Accuracy 86.4% validation / 90.8% test vs Zambretti ~64% and cloud IoT 87.2%.",
        "Rain recall 92.3% (879 / 952 events); Clear 91.5%; Cloudy 88.7%.",
        "Inference 14.2 ms; round-trip to ESP32 < 50 ms vs cloud APIs 1.5–3.0 s.",
        "24 h buffer stays under 50 MB; local Wi-Fi, $0 / month, survives ISP outages.",
        "Rain class weight on humidity +1.16; Clear class on pressure +0.90 — matches meteorology.",
        "Live partial_fit() moved a rain probability from 40.3% to 46.3% without a full retrain.",
    ]
    for i, b in enumerate(perfs):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        set_p(p, 9.8, after=3)
        run(p, "•  " + b)

    y = y + h_perf + 0.10
    card(slide, x, y, cw, h_conc, "Conclusion")
    tf = add_tb(slide, x + 0.04, y + 0.40, cw - 0.08, h_conc - 0.46)
    p = tf.paragraphs[0]
    set_p(p, 10.0, after=0)
    run(p,
        "The dual-MCU edge server (Arduino Uno + ESP32 + Flask) delivers hyper-local "
        "nowcasting that coarse 25 km grids and cloud gadgets cannot. 86.4% accuracy, "
        "92.3% storm recall, < 15 ms inference and 6-hour self-learning give a "
        "storm-survivable station for farms, campuses and homes — with no subscription.")

    y = y + h_conc + 0.10
    card(slide, x, y, cw, h_fut, "Future Scope")
    tf = add_tb(slide, x + 0.04, y + 0.40, cw - 0.08, h_fut - 0.46)
    futs = [
        "Solar field node: 18650 pack + 5 W panel, ESP32 deep sleep.",
        "3D-printed double-louvered Stevenson screen for the sensors.",
        "Tipping-bucket rain gauge and pulse anemometer for severity.",
        "SX1278 LoRa mesh across 5–10 km farm clusters, no cellular.",
    ]
    for i, b in enumerate(futs):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        set_p(p, 9.7, after=2)
        run(p, "•  " + b)

    y = y + h_fut + 0.10
    card(slide, x, y, cw, h_ref, "References")
    tf = add_tb(slide, x + 0.04, y + 0.38, cw - 0.08, h_ref - 0.42)
    refs = [
        "[1] Al-Absi et al., IoT Weather Station ESP32, IEEE Access, 2020.",
        "[2] Warden & Situnayake, TinyML, O’Reilly, 2021.",
        "[3] Roy et al., Edge-Computing Weather Stations, Comput. Electron. Agric., 2023.",
        "[4] Patel & Mehta, Solar Dual-MCU Logger, SETA, 2024.",
        "[5] Farooq et al., TinyML Rainfall Nowcasting, Sensors, 2025.",
        "[6] Bosch Sensortec, BMP280 Datasheet; Arduino / Espressif TRMs.",
    ]
    for i, b in enumerate(refs):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        set_p(p, 8.4, after=1.2, color=MUTED)
        run(p, b, size=8.4, color=MUTED)

    out = os.path.join(BASE, "AI_Weather_Prediction_Poster.pptx")
    prs.save(out)
    print("Saved", out)
    return out


if __name__ == "__main__":
    build()
