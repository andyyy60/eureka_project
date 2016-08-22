from PIL import Image
import cv2, transparency
import numpy as np

def make_bg(width, height):
    blank_image = np.zeros((height, width, 3), np.uint8)
    blank_image[:width] = (0, 0, 0)  # (B, G, R)
    cv2.imwrite("out.png",blank_image)

def paste(image):
    foreground = Image.open(image)
    w, h = foreground.size
    make_bg(w,h)
    background = Image.open("/home/andy/PycharmProjects/animal_cropping/src/out.png")
    background.paste(foreground, (0,0), foreground)
    background.save("bear_black_bg.png")


def pixel_intensity(image):
    img = Image.open(image)
    img = img.convert("RGB")
    im2 = img.point(lambda p: p * .6)
    im2.save("out2.png")


pixel_intensity("/home/andy/PycharmProjects/animal_cropping/transparent2.png")

# paste("/home/andy/PycharmProjects/animal_cropping/tmp/out.png")4

def make_transparent(input_image, flip = True, transparent = False):
    if not transparent:
        img = Image.open(input_image)
        img = img.convert("RGBA")
        datas = img.getdata()

        newData = []
        for item in datas:
            if item[0] == 0 and item[1] == 0 and item[2] == 0:
                newData.append((255, 255, 255, 0))
            else:
                newData.append(item)

        img.putdata(newData)
        img.save("transparent1.png", "PNG")
    if transparent:
        img = Image.open(input_image)
        img.save("transparent1.png", "PNG")
        transparency.flip_h(input_image)
        img = Image.open("flipped_h.png")
        img.save("transparent2.png", "PNG")

    if flip:
        transparency.flip_h(input_image)
        if not transparent:
            img = Image.open("flipped_h.png")
            img = img.convert("RGBA")
            datas = img.getdata()

            newData = []
            for item in datas:
                # if item[0] >= 225 and item[1] >= 225 and item[2] >= 225:
                if item[0] == 0 and item[1] == 0 and item[2] == 0:
                    newData.append((255, 255, 255, 0))
                else:
                    newData.append(item)

            img.putdata(newData)
            img.save("transparent2.png", "PNG")

make_transparent("/home/andy/PycharmProjects/animal_cropping/src/out2.png", True, False)

# def test():
#     overlay = Image.open('/home/andy/PycharmProjects/animal_cropping/tmp/transparent1.png')
#     base = Image.open('/home/andy/images/master_training/empty/empty1.jpg')
#
#     bands = list(overlay.split())
#     if len(bands) == 4:
#         # Assuming alpha is the last band
#         bands[3] = bands[3].point(lambda x: x * 0.4)
#     overlay = Image.merge(overlay.mode, bands)
#
#     base.paste(overlay, (0, 0), mask =overlay)
#     base.save('result1.png')
#
# # test()