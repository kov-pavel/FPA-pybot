from PIL import Image
from io import BytesIO
from config import WATERMARK0, WATERMARK1, HEIGHT_THRESHOLD, WIDTH_THRESHOLD, OVERALL_THRESHOLD


def apply_watermark(file, watermark_type) -> bytes:
    if watermark_type == 0:
        WATERMARK = WATERMARK0
    else:
        WATERMARK = WATERMARK1
    print(WATERMARK)
    with Image.open(BytesIO(file)) as img:
        chunk_width = img.width // len(WATERMARK)
        chunk_height = img.height // len(WATERMARK)
        # Точки не должны быть слишком маленькие, чтобы они не затерлись
        dot_size_height = img.height // HEIGHT_THRESHOLD + 1
        dot_size_width = img.width // WIDTH_THRESHOLD + 1
        dot_size_middle = img.width * img.height // OVERALL_THRESHOLD + 1
        px = img.load()

        for index, value in enumerate(WATERMARK):
            if value == '•':
                # Точки по главной диагонали
                create_dot(px, index * chunk_width + chunk_width // 2,
                           0 + index * chunk_height, dot_size_middle)
                # Точки снизу
                # create_dot(px, index * chunk_width + chunk_width // 2, img.height - dot_size_width, dot_size_width)
                # горизонтальные точки посередине ближе к верху
                create_dot(px, index * chunk_width + chunk_width // 2, img.height // 2 + img.height // 5,
                           dot_size_middle)
                # Вертикальные точки посередине ближе к левому краю
                create_dot(px, img.width // 2 - img.width // 3, index * chunk_height + chunk_height // 2,
                           dot_size_middle)
                # Точки слева
                # create_dot(px, 0, index * chunk_height + chunk_height // 2, dot_size_height)
                # px[index * length + length // 2, img.height - 1] = COLOR
            elif value == '−':
                # Точки по побочной диагонали
                create_dot(px, index * chunk_width + chunk_width // 2,
                           img.height - index * chunk_height - dot_size_middle, dot_size_middle)
                # Точки справа
                # create_dot(px, img.width - dot_size_height, index * chunk_height + chunk_height // 2, dot_size_height)
                # горизонтальные точки посередине ближе к низу
                create_dot(px, index * chunk_width + chunk_width // 2, img.height // 2 - img.height // 5,
                           dot_size_middle)
                # Вертикальные точки посередине ближе к правому краю
                create_dot(px, img.width // 2 + img.width // 3, index * chunk_height + chunk_height // 2,
                           dot_size_middle)
                # Точки сверху
                # create_dot(px, index * chunk_width + chunk_width // 2, 0, dot_size_width)
                # px[index * length + length // 2, 0] = COLOR

        result = BytesIO()
        img.save(result, format=img.format)
        return result.getvalue()


def create_dot(px, x, y, size):
    color = determine_color(px[x, y])
    for i in range(size):
        for j in range(size):
            px[x + i, y + j] = color


def determine_color(px):
    color = [0, 0, 0]
    for i in range(3):
        if px[i] > 128:
            color[i] = px[i] - 128
        else:
            color[i] = px[i] + 128
    return color[0], color[1], color[2]
