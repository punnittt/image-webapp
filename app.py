from flask import Flask, render_template, request, send_from_directory, jsonify
from PIL import Image, ImageDraw, ImageFont
import os, uuid, zipfile, random

app = Flask(__name__)

GENERATED_DIR = "generated"
FONT_DIR = "fonts"   # store .ttf files here
os.makedirs(GENERATED_DIR, exist_ok=True)
os.makedirs(FONT_DIR, exist_ok=True)

# Default fallback fonts (system)
DEFAULT_FONTS = [
    "arial.ttf",
    "calibri.ttf",
    "times.ttf",
    "verdana.ttf"
]

def get_random_font(size):
    """Pick a random custom font OR fallback."""
    custom_fonts = [f for f in os.listdir(FONT_DIR) if f.endswith(".ttf")]

    if custom_fonts:
        font_file = os.path.join(FONT_DIR, random.choice(custom_fonts))
    else:
        font_file = random.choice(DEFAULT_FONTS)

    try:
        return ImageFont.truetype(font_file, size)
    except:
        return ImageFont.load_default()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    image = request.files["image"]
    text = request.form["text"]

    original = Image.open(image).convert("RGB")

    folder_name = uuid.uuid4().hex
    save_folder = os.path.join(GENERATED_DIR, folder_name)
    os.makedirs(save_folder)

    for i in range(1, 101):

        img = original.copy()
        draw = ImageDraw.Draw(img)

        # ===== RANDOM TEXT POSITION (with safe margins) =====
        safe_margin = 40
        x = random.randint(safe_margin, img.width - safe_margin - 200)
        y = random.randint(safe_margin, img.height - safe_margin - 100)

        # ===== RANDOM TEXT COLOR =====
        text_color = (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255)
        )

        # ===== DYNAMIC + RANDOM FONT SIZE =====
        min_size = int(img.width * 0.05)    # 5% of width
        max_size = int(img.width * 0.10)    # 10% of width
        font_size = random.randint(min_size, max_size)

        font = get_random_font(font_size)

        draw.text((x, y), text, fill=text_color, font=font)

        # ---------------------------------------------------
        #                 PREMIUM BORDER FRAME
        # ---------------------------------------------------

        # Beautiful aesthetic border colors
        border_colors = [
            (255, 99, 72),     # soft red
            (72, 154, 255),    # sky blue
            (255, 207, 72),    # warm yellow
            (144, 238, 144),   # light green
            (255, 182, 193),   # baby pink
            (186, 85, 211),    # purple
            (255, 165, 0),     # orange
            (135, 206, 250)    # baby blue
        ]

        border_color = random.choice(border_colors)

        # Thickness: 1% to 3% of width (clean aesthetic)
        border_thickness = random.randint(
            int(img.width * 0.01),
            int(img.width * 0.03)
        )

        # Create frame canvas
        framed = Image.new(
            "RGB",
            (img.width + border_thickness * 2, img.height + border_thickness * 2),
            border_color
        )

        # Paste image inside frame
        framed.paste(img, (border_thickness, border_thickness))

        # Save final image
        filename = f"Variation_{i}.jpg"
        framed.save(os.path.join(save_folder, filename))

    # Create ZIP
    zip_name = f"{folder_name}.zip"
    zip_path = os.path.join(GENERATED_DIR, zip_name)

    with zipfile.ZipFile(zip_path, "w") as zipf:
        for file in os.listdir(save_folder):
            zipf.write(os.path.join(save_folder, file), file)

    return jsonify({"zip_url": f"/download/{zip_name}"})


@app.route("/download/<filename>")
def download(filename):
    return send_from_directory(GENERATED_DIR, filename, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
