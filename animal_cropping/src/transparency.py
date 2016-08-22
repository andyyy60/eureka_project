from PIL import Image
import os, sys, random, time, cv2, exifread, string

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def flip_h(image):
    img = Image.open(image)
    img.transpose(Image.FLIP_LEFT_RIGHT).save('flipped_h.png')

# flip_h("/home/andy/PycharmProjects/animal_cropping/coyote/coyote_5.png")

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
        flip_h(input_image)
        img = Image.open("flipped_h.png")
        img.save("transparent2.png", "PNG")

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
            img.save("transparent2.png", "PNG")
            os.remove("flipped_h.png")

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
        im = Image.open(path+"/transparent1.png")
        img = im.convert("RGB")
        im2 = img.point(lambda p: p * .6)
        im2.save(path+"/tmp/transparent1.png")
        os.chdir(path+'/tmp')
        make_transparent(path+"/tmp/transparent1.png", True, False)
        path = path+"/tmp/"
    elif (hour >= 22 or hour <= 5):
        im = Image.open(path+"/transparent1.png")
        img = im.convert("RGB")
        im2 = img.point(lambda p: p * .4)
        im2.save(path+"/tmp/transparent1.png")
        os.chdir(path+'/tmp')
        make_transparent(path+"/tmp/transparent1.png", True, False)
        path = path+"/tmp/"
    return path

# pixel_intensity("/home/andy/images/empty/Main_2016-03-16_07:06:20_0006.JPG", "/home/andy/PycharmProjects/animal_cropping/coyote/coyote_1")



# make_transparent("/home/andy/PycharmProjects/animal_cropping/coyote/coyote_5.png", True, True)

def resize(infile):

    im = Image.open(infile)
    w, h = im.size
    size = 722, 497
    if w >700 and h >500:
        im.thumbnail(size, Image.ANTIALIAS)
        im.save(infile, "PNG")


def animal_placement(path, empty_background, save_path):
    background = Image.open(empty_background)
    bg_w, bg_h = background.size
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
            background.save(save_path+id_generator()+".jpg")


# animal_placement("/home/andy/PycharmProjects/animal_cropping/", "/home/andy/images/empty/1.jpg")

def main(folder):
    for image in os.listdir(folder):
        full_path = folder+image
        animal_placement("/home/andy/PycharmProjects/animal_cropping/coyote/coyote_1", full_path, "/home/andy/images/test/")

main("/home/andy/images/empty/")

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
