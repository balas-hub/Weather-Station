from PIL import Image
import os

out_dir = r"E:\weather predection\static\poster_assets"
p1 = os.path.join(out_dir, "fig4a_temperature_humidity.png")
p2 = os.path.join(out_dir, "fig4b_barometric_pressure_hazard.png")

im1 = Image.open(p1)
im2 = Image.open(p2)

# Make them same width
target_w = max(im1.width, im2.width)
h1 = int(im1.height * (target_w / im1.width))
h2 = int(im2.height * (target_w / im2.width))

im1_resized = im1.resize((target_w, h1), Image.Resampling.LANCZOS)
im2_resized = im2.resize((target_w, h2), Image.Resampling.LANCZOS)

combined = Image.new('RGB', (target_w, h1 + h2 + 15), color='#FFFFFF')
combined.paste(im1_resized, (0, 0))
combined.paste(im2_resized, (0, h1 + 15))

out_path = os.path.join(out_dir, "fig4_results_combined.png")
combined.save(out_path, dpi=(300, 300))
print("Saved combined Fig 4 to:", out_path)
