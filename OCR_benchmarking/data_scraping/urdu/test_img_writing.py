# smoke_dejavu.py
from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display
from glob import glob 
import os
from tqdm import tqdm

out_folder = "test_fonts"
os.makedirs(out_folder, exist_ok=True)
FONT_CANDIDATES = glob("/usr/share/fonts/truetype/**/*.ttf")
for font in tqdm(FONT_CANDIDATES):
    font = ImageFont.truetype(font, 56)

    sample = "یہ ایک سادہ اردو جملہ ہے۔ پاکستان، اُردو، کتاب"
    txt = get_display(arabic_reshaper.reshape(sample))

    img = Image.new("RGB", (1800, 240), "white")
    ImageDraw.Draw(img).text((40, 80), txt, fill="black", font=font)
    path = f"dejavu_smoke_test_{font.getname()[0]}.png"
    img.save(path)
