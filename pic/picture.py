from pathlib import Path
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

base_dir = "/data/img/"


def generata_pic(a, b, c, filename):
    abs_path = base_dir + filename + ".png"
    p_file = Path(abs_path)
    if p_file.is_file():
        return filename + ".png"
    # 设置字体，如果没有，也可以不设置
    font = ImageFont.truetype('/tmp/simsun.ttf', 30)

    # 打开底版图片
    imageFile = "/tmp/blank.jpg"
    tp = Image.open(imageFile)

    draw = ImageDraw.Draw(tp)
    draw.text((200, 100), "累计签到:\t%5d天" % a, (0, 0, 0), font=font)
    draw = ImageDraw.Draw(tp)
    draw.text((200, 150), "连续签到:\t%5d天" % b, (0, 0, 0), font=font)
    draw = ImageDraw.Draw(tp)
    draw.text((200, 200), "目前积分:\t%5d分" % c, (0, 0, 0), font=font)
    draw = ImageDraw.Draw(tp)
    draw.text((200, 300), "积分排名:\t%s名" % "你就是第一", (0, 0, 0), font=font)
    draw = ImageDraw.Draw(tp)

    # 保存
    tp.save(abs_path)
    return filename + ".png"
