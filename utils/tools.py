import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont


def read_image_bytes(bytes_data):
    image = None
    try:
        image = np.asarray(bytearray(bytes_data), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    except:
        pass
    return image


def read_image_file(file_name):
    img = cv2.imread(file_name)
    image = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    return image


def save_image_bytes(file_name, bytes_data):
    with open(file_name, "wb") as f:
        f.write(bytes_data)


def draw_image_with_boxes(image, bbox, score, pitch, yaw, roll):
    draw = ImageDraw.Draw(image)
    left, top, right, bottom = bbox
    color = (min([255, int(255 * score) + 100]), 0, 0)
    draw.rectangle([(left, top), (right, bottom)], width=2, outline=color)

    font_size = max(int((right - left) // 8), 10)
    font = ImageFont.truetype("./utils/msyh.ttc", font_size)
    text = "{:.3f},{:.0f},{:.0f},{:.0f}".format(score, pitch, yaw, roll)
    th = sum(font.getmetrics())
    tw = max(font.getsize(text)[0] + 1, right - left)
    start_y = max(0, top - th)
    draw.rectangle([(left, start_y), (left + tw, start_y + th)], fill=color, width=2)
    draw.text((left + 1, start_y), text, fill=(255, 255, 255), font=font, anchor="la")
    del draw
    return image
