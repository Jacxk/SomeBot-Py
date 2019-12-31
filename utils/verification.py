import random
import string
from io import BytesIO

from PIL import Image, ImageDraw, ImageFont

letters = string.ascii_letters
numbers = "".join(list(map(str, range(10))))
num_let = letters + numbers


def generate_captcha_text():
    text = ''
    for i in range(5):
        text += random.choice(num_let)
    return text


def generate_captcha():
    captcha_text = generate_captcha_text()

    pil_font = ImageFont.truetype("./assets/fonts/Aller_Rg.ttf", size=100)
    text_size = ImageDraw.Draw(Image.new("RGBA", (500, 500))).textsize(captcha_text, font=pil_font)

    pil_image = Image.new("RGB", text_size, "black")

    pil_draw = ImageDraw.Draw(pil_image)
    pil_draw.text(xy=(0, 0), text=captcha_text, font=pil_font)
    for i in range(10):
        xy_1 = (random.randint(0, text_size[0]), random.randint(0, text_size[1]))
        xy_2 = (random.randint(0, text_size[0]), random.randint(0, text_size[1]))
        pil_draw.line(xy_1 + xy_2, fill="white", width=3)

    image_buffer = BytesIO()
    pil_image.save(image_buffer, format="JPEG", quality=1)
    image_buffer.seek(0)

    return [captcha_text, image_buffer]
