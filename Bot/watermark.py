from PIL import Image
from io import BytesIO
from config import WATERMARK, COLOR
from morse import Morse


def apply_watermark(file) -> bytes:
    with Image.open(BytesIO(file)) as img:
        length = img.width // len(WATERMARK)
        px = img.load()

        for index, value in enumerate(WATERMARK):
            if value == Morse.DOT:
                px[index * length + length // 2, img.height - 1] = COLOR
            elif value == Morse.DASH:
                px[index * length + length // 2, 0] = COLOR

        result = BytesIO()
        img.save(result, format=img.format)
        return result.getvalue()
