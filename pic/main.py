import os
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw


if __name__ == "__main__":
    print("deal picture")
    # 设置字体，如果没有，也可以不设置
    font = ImageFont.truetype('./template/simsun.ttf', 30)

    # 打开底版图片
    imageFile = "./template/blank.jpg"
    tp = Image.open(imageFile)

    draw = ImageDraw.Draw(tp)
    draw.text((200, 100), "累计签到:\t%5d天" % 110, (0, 0, 0), font=font)
    draw = ImageDraw.Draw(tp)
    draw.text((200, 150), "连续签到:\t%5d天" % 10, (0, 0, 0), font=font)
    draw = ImageDraw.Draw(tp)
    draw.text((200, 200), "目前积分:\t%5d分" % 1120, (0, 0, 0), font=font)
    draw = ImageDraw.Draw(tp)
    draw.text((200, 300), "积分排名:\t%5d+名" % 100, (0, 0, 0), font=font)
    draw = ImageDraw.Draw(tp)

    # 保存
    tp.save("./output/x.png")
