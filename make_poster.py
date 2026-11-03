from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from PIL import Image
import os

# ---------- Palette ----------
BLUE_HEADER = RGBColor(0x2E, 0x5A, 0x88)
SECTION_BLUE= RGBColor(0x3A, 0x6E, 0x9E)
LIGHT_PANEL = RGBColor(0xF2, 0xF5, 0xF8)
WHITE       = RGBColor(0xFF, 0xFF, 0xFF)
DARK_TEXT   = RGBColor(0x20, 0x20, 0x20)
GREY_TEXT   = RGBColor(0x55, 0x55, 0x55)
ACCENT_RED  = RGBColor(0xC0, 0x39, 0x2B)
GREEN_OK    = RGBColor(0x2E, 0x7D, 0x32)
BLUE_DARK   = RGBColor(0x1F, 0x4A, 0x70)
METRIC_BLUE = RGBColor(0xE8, 0xF0, 0xF8)

ASSETS = r"E:\weather predection\poster_assets"

prs = Presentation()
prs.slide_width  = Inches(13.333)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]
s = prs.slides.add_slide(BLANK)

# ---------- Helpers ----------
def rect(left, top, width, height, fill, line=None, shape=MSO_SHAPE.RECTANGLE):
    shp = s.shapes.add_shape(shape, left, top, width, height)
    shp.fill.solid()
    shp.fill.fore_color.rgb = fill
    if line is None:
        shp.line.fill.background()
    else:
        shp.line.color.rgb = line
        shp.line.width = Pt(0.75)
    shp.shadow.inherit = False
    return shp

def textbox(left, top, width, height, anchor=MSO_ANCHOR.TOP):
    tb = s.shapes.add_textbox(left, top, width, height)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = Inches(0.04)
    tf.margin_right = Inches(0.04)
    tf.margin_top = Inches(0.02)
    tf.margin_bottom = Inches(0.02)
    return tb, tf

def para(tf, text, size, bold=False, color=DARK_TEXT, align=PP_ALIGN.LEFT,
         space_after=Pt(2), space_before=Pt(0), first=False, font='Calibri', italic=False):
    p = tf.paragraphs[0] if first and not tf.paragraphs[0].runs else tf.add_paragraph()
    p.alignment = align
    p.space_after = space_after
    p.space_before = space_before
    run = p.add_run()
    run.text = text
    f = run.font
    f.size = Pt(size)
    f.bold = bold
    f.italic = italic
    f.color.rgb = color
    f.name = font
    return p

def bullet(tf, text, size=8.5, level=0, bold=False, color=DARK_TEXT,
           space_after=Pt(1.5), first=False, bullet_char='\u2022'):
    if first and not tf.paragraphs[0].runs:
        p = tf.paragraphs[0]
    else:
        p = tf.add_paragraph()
    p.level = level
    p.space_after = space_after
    prefix = (bullet_char + '  ' if level == 0 else '-   ')
    run = p.add_run()
    run.text = prefix + text
    f = run.font
    f.size = Pt(size)
    f.bold = bold
    f.color.rgb = color
    f.name = 'Calibri'
    return p

def section_bar(left, top, width, title, fill=SECTION_BLUE, h=Inches(0.34)):
    rect(left, top, width, h, fill)
    _, tf = textbox(left + Inches(0.05), top + Inches(0.018), width - Inches(0.1), h - Inches(0.036),
                    anchor=MSO_ANCHOR.MIDDLE)
    para(tf, title, 11, bold=True, color=WHITE, first=True, space_after=Pt(0))

def content_panel(left, top, width, height, fill=LIGHT_PANEL, line=RGBColor(0xB9, 0xC6, 0xD4)):
    return rect(left, top, width, height, fill, line=line)

def metric_card(left, top, width, height, label, value, sub=None, fill=METRIC_BLUE, val_color=BLUE_DARK):
    rect(left, top, width, height, fill, line=RGBColor(0xB9, 0xC6, 0xD4))
    _, tf = textbox(left + Inches(0.04), top + Inches(0.03), width - Inches(0.08), height - Inches(0.06), anchor=MSO_ANCHOR.MIDDLE)
    para(tf, label, 7.5, bold=True, color=ACCENT_RED, first=True, space_after=Pt(1), align=PP_ALIGN.CENTER)
    para(tf, value, 13, bold=True, color=val_color, space_after=Pt(0), align=PP_ALIGN.CENTER)
    if sub:
        para(tf, sub, 7, color=GREY_TEXT, space_after=Pt(0), align=PP_ALIGN.CENTER)

def add_image_fit(path, left, top, max_w, max_h, align_center=True):
    """Add image fitting within max_w x max_h, preserving aspect ratio."""
    img = Image.open(path)
    iw, ih = img.size
    ar = ih / iw
    w = max_w
    h = Emu(int(w * ar))
    if h > max_h:
        h = max_h
        w = Emu(int(h / ar))
    l = left
    if align_center and w < max_w:
        l = Emu(int(left + (max_w - w) / 2))
    t = top
    if h < max_h:
        t = Emu(int(top + (max_h - h) / 2))
    return s.shapes.add_picture(path, l, t, w, h)

# ---------- Layout constants ----------
ML = Inches(0.5)        # left margin
GAP = Inches(0.12)
START_Y = Inches(1.18)
CONTENT_BOTTOM = Inches(7.05)
CONTENT_H = CONTENT_BOTTOM - START_Y  # 5.87 inches

# 5 columns (centered block)
COL_W = [Inches(2.55), Inches(2.20), Inches(2.20), Inches(2.45), Inches(2.45)]
col_x = [ML]
x = ML
for w in COL_W[:-1]:
    x = x + w + GAP
    col_x.append(x)

# ---------- HEADER ----------
rect(0, 0, prs.slide_width, Inches(1.06), BLUE_HEADER)
_, tf = textbox(Inches(0.3), Inches(0.06), Inches(12.73), Inches(0.5))
para(tf, 'AI-Based Local Weather Forecasting and Prediction System Using Arduino Uno and ESP32',
     20, bold=True, color=WHITE, first=True, space_after=Pt(0))
_, tf = textbox(Inches(0.3), Inches(0.54), Inches(12.73), Inches(0.26))
para(tf, 'Localized microclimate monitoring with DHT11 + BMP280 sensing, dual-MCU UART telemetry, and a self-training Flask edge-ML server',
     11, color=RGBColor(0xDE, 0xEA, 0xF5), first=True, space_after=Pt(0))
_, tf = textbox(Inches(0.3), Inches(0.79), Inches(12.73), Inches(0.24))
para(tf, 'Balavignesh K \u2013 E0225002  |  Sudharsan N \u2013 E0225010  |  Sri Ramachandra Faculty of Engineering and Technology, SRIHER, Porur, Chennai - 600116',
     10, bold=True, color=RGBColor(0xE8, 0xF0, 0xF8), first=True, space_after=Pt(0))

# ================= COLUMN 1 =================
cx = col_x[0]; cw = COL_W[0]
y = START_Y
section_bar(cx, y, cw, 'Abstract')
y = y + Inches(0.38)
content_panel(cx, y, cw, Inches(1.62))
_, tf = textbox(cx + Inches(0.06), y + Inches(0.04), cw - Inches(0.12), Inches(1.54))
para(tf, 'Generic weather apps miss localized microclimates and neighborhood storms, pulling data from regional airports 15\u201325 km away. Internet-reliant devices fail during storm outages. This work presents a modular dual-microcontroller edge-server system: an Arduino Uno sensor node, an ESP32 Wi-Fi gateway, and a Python Flask server with a self-training SGDClassifier that forecasts Clear / Cloudy / Rain with real-time alerts\u2014all on the local network.',
     7.8, color=DARK_TEXT, first=True, space_after=Pt(0))
y = y + Inches(1.68)
section_bar(cx, y, cw, 'Introduction & Need')
y = y + Inches(0.38)
content_panel(cx, y, cw, Inches(1.5))
_, tf = textbox(cx + Inches(0.06), y + Inches(0.04), cw - Inches(0.12), Inches(1.42))
bullet(tf, 'NWP models use 15\u201325 km grids; miss microclimates.', size=7.6, first=True)
bullet(tf, 'Cloud stations fail when storm cuts internet.', size=7.6)
bullet(tf, 'Hobbyist stations ignore barometric pressure trends.', size=7.6)
y = y + Inches(1.56)
section_bar(cx, y, cw, 'Objectives')
y = y + Inches(0.38)
content_panel(cx, y, cw, Inches(1.32))
_, tf = textbox(cx + Inches(0.06), y + Inches(0.04), cw - Inches(0.12), Inches(1.24))
objs = ['1. Sample T, RH, pressure at 1-min via DHT11 + BMP280.',
        '2. UART Uno\u2192ESP32; HTTP POST to local Flask server.',
        '3. SGDClassifier edge ML; online self-learning every 6 h.']
for i, o in enumerate(objs):
    bullet(tf, o, size=7.8, first=(i == 0))

# ================= COLUMN 2 =================
cx = col_x[1]; cw = COL_W[1]
y = START_Y
section_bar(cx, y, cw, 'Proposed Methodology')
y = y + Inches(0.38)
content_panel(cx, y, cw, Inches(1.98))
_, tf = textbox(cx + Inches(0.06), y + Inches(0.04), cw - Inches(0.12), Inches(1.9))
meth = ['Dual-MCU edge-server: Uno (sensor) \u2192 ESP32 (gateway) \u2192 Flask server.',
        'Uno samples DHT11 + BMP280 every 60 s; JSON telemetry.',
        'Uno SoftwareSerial (Pin 11 TX) \u2192 ESP32 HardwareSerial2 (GPIO 16 RX2).',
        'ESP32 posts JSON over local 2.4 GHz Wi-Fi (HTTP POST).',
        'Flask buffers 24 h (1440 samples); computes \u0394P_3h, \u0394P_6h, \u0394RH_3h.',
        'SGDClassifier predicts Clear / Cloudy / Rain; rain >60% alerts.',
        'Self-train every 6 h: model.partial_fit() vs ground truth.']
for i, m in enumerate(meth):
    bullet(tf, m, size=7.4, first=(i == 0), space_after=Pt(1.1))
y = y + Inches(2.04)
section_bar(cx, y, cw, 'System Architecture')
y = y + Inches(0.38)
arch_h = Inches(1.62)
content_panel(cx, y, cw, arch_h)
_, tf = textbox(cx + Inches(0.06), y + Inches(0.04), cw - Inches(0.12), arch_h - Inches(0.08))
para(tf, 'ARDUINO UNO', 7.8, bold=True, color=BLUE_DARK, first=True, space_after=Pt(1))
bullet(tf, 'DHT11 (Pin 2) + BMP280 (I2C A4/A5)', size=7.2, level=1)
para(tf, 'ESP32 GATEWAY', 7.8, bold=True, color=BLUE_DARK, space_before=Pt(2), space_after=Pt(1))
bullet(tf, 'UART GPIO16/17 \u2192 Wi-Fi HTTP POST', size=7.2, level=1)
para(tf, 'FLASK EDGE SERVER', 7.8, bold=True, color=ACCENT_RED, space_before=Pt(2), space_after=Pt(1))
bullet(tf, 'SGDClassifier <15 ms inference', size=7.2, level=1)
bullet(tf, 'Online partial_fit() every 6 h', size=7.2, level=1)
y = y + arch_h + Inches(0.06)
img_h = Inches(1.72)
content_panel(cx, y, cw, img_h, fill=WHITE)
try:
    add_image_fit(f'{ASSETS}\\image3.png', cx + Inches(0.03), y + Inches(0.03), cw - Inches(0.06), img_h - Inches(0.06))
except Exception:
    _, tf = textbox(cx + Inches(0.05), y + Inches(0.05), cw - Inches(0.1), img_h - Inches(0.1))
    para(tf, '[Workflow flowchart]', 7.5, italic=True, color=GREY_TEXT, align=PP_ALIGN.CENTER, first=True)

# ================= COLUMN 3 =================
cx = col_x[2]; cw = COL_W[2]
y = START_Y
section_bar(cx, y, cw, 'Hardware Components')
y = y + Inches(0.38)
content_panel(cx, y, cw, Inches(1.72))
from pptx.util import Inches as IN
gfx = s.shapes.add_table(6, 3, cx + Inches(0.03), y + Inches(0.03), cw - Inches(0.06), Inches(1.66))
tbl = s.shapes[-1].table
tbl.columns[0].width = IN(0.62)
tbl.columns[1].width = IN(0.62)
tbl.columns[2].width = IN(0.62)
hdrs = ['Component', 'Role', 'Interface']
for j, htxt in enumerate(hdrs):
    cell = tbl.cell(0, j)
    cell.fill.solid(); cell.fill.fore_color.rgb = BLUE_DARK
    tf = cell.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.LEFT
    r = p.add_run(); r.text = htxt
    r.font.size = Pt(7); r.font.bold = True; r.font.color.rgb = WHITE; r.font.name = 'Calibri'
    cell.margin_left = IN(0.02); cell.margin_right = IN(0.02); cell.margin_top = IN(0.008); cell.margin_bottom = IN(0.008)
rows = [('Arduino Uno Rev3', 'Sensor node T/RH/P', 'UART + I2C'),
        ('ESP32 DevKit V1', 'Wi-Fi gateway', 'UART + Wi-Fi'),
        ('DHT11 sensor', 'Temp + humidity', 'Digital GPIO 2'),
        ('BMP280 sensor', 'Barometric pressure', 'I2C (A4/A5)'),
        ('Laptop i5/16GB', 'Flask edge ML server', 'Local Wi-Fi HTTP')]
for i, (a, b, c) in enumerate(rows, 1):
    for j, val in enumerate((a, b, c)):
        cell = tbl.cell(i, j)
        cell.fill.solid(); cell.fill.fore_color.rgb = WHITE if i % 2 else LIGHT_PANEL
        tf = cell.text_frame; tf.word_wrap = True
        p = tf.paragraphs[0]; p.alignment = PP_ALIGN.LEFT
        r = p.add_run(); r.text = val
        r.font.size = Pt(6.8); r.font.bold = (j == 0); r.font.color.rgb = DARK_TEXT; r.font.name = 'Calibri'
        cell.margin_left = IN(0.02); cell.margin_right = IN(0.02); cell.margin_top = IN(0.004); cell.margin_bottom = IN(0.004)
y = y + Inches(1.78)
section_bar(cx, y, cw, 'Circuit Diagram')
y = y + Inches(0.38)
circ_h = Inches(3.36)
content_panel(cx, y, cw, circ_h, fill=WHITE)
try:
    add_image_fit(f'{ASSETS}\\image4.png', cx + Inches(0.03), y + Inches(0.03), cw - Inches(0.06), circ_h - Inches(0.06))
except Exception:
    _, tf = textbox(cx + Inches(0.05), y + Inches(0.05), cw - Inches(0.1), circ_h - Inches(0.1))
    para(tf, '[Circuit diagram]', 7.5, italic=True, color=GREY_TEXT, align=PP_ALIGN.CENTER, first=True)

# ================= COLUMN 4 =================
cx = col_x[3]; cw = COL_W[3]
y = START_Y
section_bar(cx, y, cw, 'Prototype Design')
y = y + Inches(0.38)
proto_h = Inches(1.78)
content_panel(cx, y, cw, proto_h, fill=WHITE)
try:
    add_image_fit(f'{ASSETS}\\image5.png', cx + Inches(0.03), y + Inches(0.03), cw - Inches(0.06), proto_h - Inches(0.06))
except Exception:
    _, tf = textbox(cx + Inches(0.05), y + Inches(0.05), cw - Inches(0.1), proto_h - Inches(0.1))
    para(tf, '[Prototype photo]', 7.5, italic=True, color=GREY_TEXT, align=PP_ALIGN.CENTER, first=True)
y = y + proto_h + Inches(0.06)

# ---- Results & Performance (enhanced) ----
section_bar(cx, y, cw, 'Results & Performance')
y = y + Inches(0.38)
# Metric cards row (3 cards)
mw = (cw - Inches(0.12)) / 3
metric_card(cx + Inches(0.06), y, mw - Inches(0.06), Inches(0.52), 'Accuracy', '86.4%', 'test 90.8%')
metric_card(cx + Inches(0.06) + mw, y, mw - Inches(0.06), Inches(0.52), 'Rain Recall', '92.3%', 'storm detection')
metric_card(cx + Inches(0.06) + mw * 2, y, mw - Inches(0.06), Inches(0.52), 'Latency', '14.2 ms', 'edge inference')
y = y + Inches(0.58)
# Two graph panels stacked
g_h = Inches(1.02)
content_panel(cx, y, cw, g_h, fill=WHITE)
try:
    add_image_fit(f'{ASSETS}\\image1.png', cx + Inches(0.03), y + Inches(0.03), cw - Inches(0.06), g_h - Inches(0.06))
except Exception:
    _, tf = textbox(cx + Inches(0.05), y + Inches(0.04), cw - Inches(0.1), g_h - Inches(0.08))
    para(tf, '[ML convergence curve]', 7.5, italic=True, color=GREY_TEXT, align=PP_ALIGN.CENTER, first=True)
y = y + g_h + Inches(0.05)
content_panel(cx, y, cw, g_h, fill=WHITE)
try:
    add_image_fit(f'{ASSETS}\\image2.png', cx + Inches(0.03), y + Inches(0.03), cw - Inches(0.06), g_h - Inches(0.06))
except Exception:
    _, tf = textbox(cx + Inches(0.05), y + Inches(0.04), cw - Inches(0.1), g_h - Inches(0.08))
    para(tf, '[Confusion matrix]', 7.5, italic=True, color=GREY_TEXT, align=PP_ALIGN.CENTER, first=True)
y = y + g_h + Inches(0.05)
_, tf = textbox(cx + Inches(0.06), y, cw - Inches(0.12), Inches(0.42))
para(tf, 'Inference <15 ms \u2022 24-h buffer <50 MB \u2022 3 classes \u2022 self-trains every 6 h',
     7.2, italic=True, color=GREY_TEXT, first=True, space_after=Pt(0), align=PP_ALIGN.CENTER)

# ================= COLUMN 5 =================
cx = col_x[4]; cw = COL_W[4]
y = START_Y
section_bar(cx, y, cw, 'Performance Analysis')
y = y + Inches(0.38)
content_panel(cx, y, cw, Inches(1.42))
_, tf = textbox(cx + Inches(0.06), y + Inches(0.04), cw - Inches(0.12), Inches(1.34))
bullet(tf, '86.4% accuracy (90.8% test) vs Zambretti ~64%.', size=7.6, first=True)
bullet(tf, 'Rain recall 92.3% via \u0394P & \u0394RH signatures.', size=7.6)
bullet(tf, 'Edge latency 14.2 ms vs cloud 1500\u20133000 ms.', size=7.6)
bullet(tf, 'Local Wi-Fi; zero cloud cost; storm-survivable.', size=7.6)
y = y + Inches(1.48)
section_bar(cx, y, cw, 'Conclusion')
y = y + Inches(0.38)
content_panel(cx, y, cw, Inches(0.98))
_, tf = textbox(cx + Inches(0.06), y + Inches(0.04), cw - Inches(0.12), Inches(0.9))
para(tf, 'Edge-server architecture (Arduino Uno + ESP32 + Flask) enables localized forecasting. Overcomes 25 km satellite grids and internet cutouts. 86.4% accuracy, 92.3% storm recall, <15 ms inference, automated self-learning every 6 h.',
     7.4, color=DARK_TEXT, first=True, space_after=Pt(0))
y = y + Inches(1.04)
section_bar(cx, y, cw, 'Future Scope')
y = y + Inches(0.38)
content_panel(cx, y, cw, Inches(1.0))
_, tf = textbox(cx + Inches(0.06), y + Inches(0.04), cw - Inches(0.12), Inches(0.92))
bullet(tf, 'Solar field deployment (18650 + 5W panel, deep sleep).', size=7.6, first=True)
bullet(tf, '3D-printed Stevenson screen enclosure.', size=7.6)
bullet(tf, 'Tipping-bucket rain gauge + anemometer.', size=7.6)
bullet(tf, 'LoRa mesh (5\u201310 km, no cellular).', size=7.6)
y = y + Inches(1.06)
section_bar(cx, y, cw, 'References')
y = y + Inches(0.38)
content_panel(cx, y, cw, Inches(1.32))
_, tf = textbox(cx + Inches(0.06), y + Inches(0.04), cw - Inches(0.12), Inches(1.24))
refs = ['[1] Al-Absi et al., IoT Weather Station ESP32, IEEE Access, 2020.',
        '[2] Warden & Situnayake, TinyML, O\u2019Reilly, 2021.',
        '[3] Roy et al., Edge-Computing Weather Stations, 2023.',
        '[4] Patel & Mehta, Solar Dual-MCU Logger, SETA, 2024.',
        '[5] Farooq et al., TinyML Rainfall Nowcasting, Sensors, 2025.']
for i, r in enumerate(refs):
    bullet(tf, r, size=6.9, first=(i == 0), space_after=Pt(1))

# ---------- Save ----------
out = r'E:\weather predection\AI_Weather_Prediction_Poster.pptx'
prs.save(out)
print('Saved:', out)
print('Slides:', len(prs.slides._sldIdLst))
