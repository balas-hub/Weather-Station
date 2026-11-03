from pptx import Presentation

prs = Presentation('E:\\weather predection\\AI_Weather_Prediction_Poster.pptx')
s = prs.slides[0]
print(f"Slide: {prs.slide_width.inches:.2f} x {prs.slide_height.inches:.2f} in")
print(f"Total shapes: {len(s.shapes)}")

pics = [sh for sh in s.shapes if sh.shape_type == 13]
print(f"\nImages embedded: {len(pics)}")
for i, pic in enumerate(pics):
    print(f"  Img {i+1}: {pic.width.inches:.2f}in x {pic.height.inches:.2f}in at L={pic.left.inches:.2f}, T={pic.top.inches:.2f}")

# Check section bars alignment
bars = [sh for sh in s.shapes if sh.shape_type == 1 and sh.fill.fore_color.rgb and str(sh.fill.fore_color.rgb) == '3A6E9E']
print(f"\nSection bars: {len(bars)}")
for i, bar in enumerate(bars):
    print(f"  Bar {i+1}: L={bar.left.inches:.2f}, W={bar.width.inches:.2f}, T={bar.top.inches:.2f}")

# Check tables
tables = [sh for sh in s.shapes if sh.has_table]
print(f"\nTables: {len(tables)}")

PYEOF
