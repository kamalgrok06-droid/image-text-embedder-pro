from PIL import Image, ImageDraw, ImageFont
import os

def process_images(input_folder, output_folder, font_path, font_size, color, x, y):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for file in os.listdir(input_folder):
        if file.lower().endswith(('.png', '.jpg', '.jpeg')):
            img_path = os.path.join(input_folder, file)
            img = Image.open(img_path).convert("RGBA")

            draw = ImageDraw.Draw(img)
            font = ImageFont.truetype(font_path, font_size)

            text = os.path.splitext(file)[0]

            draw.text((x, y), text, font=font, fill=color)

            output_path = os.path.join(output_folder, file)
            img.convert("RGB").save(output_path)

    return "Processing complete!"
