import os, sys, random, time, cv2, exifread, string, numpy as np
from crop import *

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def make_bg(width, height):
    blank_image = np.zeros((height, width, 3), np.uint8)
    blank_image[:width] = (0, 0, 0)  # (B, G, R)
    cv2.imwrite("out.png",blank_image)

def paste(image, output=os.curdir):
    foreground = Image.open(image)
    w, h = foreground.size
    make_bg(w,h)
    background = Image.open("out.png")
    background.paste(foreground, (0,0), foreground)
    background.save(output+"/transparent1.png")
    os.remove("out.png")

# paste("/home/andy/PycharmProjects/animal_cropping/bear/bear_5.png")

def flip_h(image):
    img = Image.open(image)
    img.transpose(Image.FLIP_LEFT_RIGHT).save('flipped_h.png')

# flip_h("/home/andy/PycharmProjects/animal_cropping/coyote/coyote_5.png")

def make_transparent(input_image, output_path = os.curdir, flip = True, transparent = False):
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
        img.save(output_path+"/transparent1.png", "PNG")
    if transparent:
        img = Image.open(input_image)
        img.save(output_path+"/transparent1.png", "PNG")
        flip_h(input_image)
        img = Image.open("flipped_h.png")
        img.save(output_path+"/transparent1.png", "PNG")

    if flip:
        flip_h(input_image)
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
            img.save(output_path+"/transparent2.png", "PNG")
            os.remove("flipped_h.png")

# make_transparent("/home/andy/PycharmProjects/animal_cropping/bear/bear_5/tmp/out_bear.png", "/home/andy/images/test")

def pixel_intensity(background, path):
    """RETURNS: Path of image. tmp folder will be returned if image was darkened"""
    img = Image.open(background)
    f = open(background)
    tags = exifread.process_file(f)
    for tag in tags.keys():
        if tag not in ('JPEGThumbnail', 'TIFFThumbnail'):  # these are not printable
            dt_value = str(tags['Image DateTime']).split()
    time = dt_value[1].split(':')
    hour = int(time[0])
    if (hour > 5 and hour <= 7) or (hour >= 18 and hour < 22):
        if not os.path.exists(path+"/tmp/"):
            os.makedirs(path+"/tmp/")
        paste(path+"/transparent1.png", path+"/tmp/")
        im = Image.open(path+"/tmp/transparent1.png")
        im2 = im.point(lambda p: p * .6)
        im2.save(path+"/tmp/transparent1.png")
        make_transparent(path+"/tmp/transparent1.png", path+"/tmp/")
        path = path+"/tmp/"
    elif (hour >= 22 or hour <= 5):
        if not os.path.exists(path+"/tmp/"):
            os.makedirs(path+"/tmp/")
        paste(path+"/transparent1.png", path+"/tmp/")
        im = Image.open(path+"/tmp/transparent1.png")
        im2 = im.point(lambda p: p * .4)
        im2.save(path+"/tmp/transparent1.png")
        make_transparent(path+"/tmp/transparent1.png", path+"/tmp/")
        path = path+"/tmp/"
    return path

# pixel_intensity("/home/andy/training/ocr_knn/master_training/empty/236.jpg", "/home/andy/PycharmProjects/animal_cropping/bear/bear_5")



# make_transparent("/home/andy/PycharmProjects/animal_cropping/bear/Bear_6.png")

def resize(infile):

    im = Image.open(infile)
    w, h = im.size
    size = 722, 497
    if w >700 and h >500:
        im.thumbnail(size, Image.ANTIALIAS)
        im.save(infile, "PNG")

# resize("/home/andy/PycharmProjects/animal_cropping/bear/Bear_6.png")

def animal_placement(path, empty_background, save_path):
    background = Image.open(empty_background)
    bg_w, bg_h = background.size
    bg_h -=120
    path = pixel_intensity(empty_background, path)
    for i in range(1,3):
        for n in range(1, bg_w, bg_w / 10):
            vertical_pos = random.randint(1,3)
            if vertical_pos == 1:
                bg_middle = bg_h - (bg_h / 4)
                cropped_image = path+"/transparent1.png"
                cropped_image_f = path+"/transparent2.png"
            elif vertical_pos == 2:
                bg_middle = bg_h - (bg_h/3)
                cropped_image = path+"/transparent1.png"
                cropped_image_f = path+"/transparent2.png"
            elif vertical_pos == 3:
                bg_middle = bg_h -(bg_h / 2)
                cropped_image = path+"/transparent1.png"
                cropped_image_f = path+"/transparent2.png"
            background = Image.open(empty_background)
            if i == 1:
                foreground = Image.open(cropped_image)
            else:
                foreground = Image.open(cropped_image_f)
            background.paste(foreground, (n, bg_middle), foreground)
            id_gen = id_generator()
            background.save(save_path+id_gen+".jpg")
            crop_ratio(save_path+id_gen+".jpg", save_path+id_gen+".jpg")



# animal_placement("/home/andy/PycharmProjects/animal_cropping/bear/bear_3/", "/home/andy/images/empty/1.jpg")

def main(bg_folder, animal_folder, output):
    for image in os.listdir(bg_folder):
        full_path = bg_folder+image
        animal_placement(animal_folder, full_path, output)

# main("/home/andy/images/empty/", "/home/andy/PycharmProjects/animal_cropping/deer/deer_5", "/home/andy/images/test/")

def DEMO_animal_placement(root, empty_background, animal):
    background = Image.open(empty_background)
    bg_w, bg_h = background.size
    for n in range(1, bg_w, bg_w / 10):
        randomizer1 = random.randint(1,2)
        vertical_pos = random.randint(1,4)

        print vertical_pos
        if vertical_pos == 1:
            bg_middle = bg_h / 3
            cropped_image = root+"/{}/{}_{}/transparent1.png".format(animal, animal, vertical_pos)
            cropped_image_f = root+"{}/{}_{}/transparent2.png".format(animal, animal, vertical_pos)
        elif vertical_pos == 2:
            bg_middle = bg_h - (bg_h / 3)
            cropped_image = root+"/{}/{}_{}/transparent1.png".format(animal, animal, vertical_pos)
            cropped_image_f = root+"{}/{}_{}/transparent2.png".format(animal, animal, vertical_pos)
        elif vertical_pos == 3:
            bg_middle = bg_h -(bg_h / 3)
            cropped_image = root+"/{}/{}_{}/transparent1.png".format(animal, animal, vertical_pos)
            cropped_image_f = root+"{}/{}_{}/transparent2.png".format(animal, animal, vertical_pos)
        elif vertical_pos == 4:
            bg_middle = bg_h / 3
            cropped_image = root+"/{}/{}_{}/transparent1.png".format(animal, animal, vertical_pos)
            cropped_image_f = root+"{}/{}_{}/transparent2.png".format(animal, animal, vertical_pos)
        background = Image.open(empty_background)
        if randomizer1 == 1:
            foreground = Image.open(cropped_image)
        else:
            foreground = Image.open(cropped_image_f)
        background.paste(foreground, (n,bg_middle), foreground)
        background.show()

        time.sleep(1)




# DEMO_animal_placement("/home/andy/PycharmProjects/animal_cropping/", "/home/andy/images/master_training/empty/empty43.jpg", "coyote")
