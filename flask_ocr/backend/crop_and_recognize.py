''''Author: Andy Rosales Elias, EUREKA! 2016, Univeristy of California, Santa Barbara | andy00@umail.ucsb.edu'''
import crop, ocr_contour, os, time, cv2, argparse, sys, random, string
import pyexifinfo as exif
from PIL import Image

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
   return ''.join(random.choice(chars) for _ in range(size))

def check(base):
    im = Image.open(base)
    width, height = im.size
    widths = [3264,1920,3776, 2688]
    heights = [2448,1080,2124, 1512]
    exif_json = exif.get_json(base)
    try:
        temp = exif_json[0]['MakerNotes:AmbientTemperatureFahrenheit']
        return [int(temp[:-2]), [width, height], exif_json]
    except:
        pass
    if (width not in widths) or (height not in heights): #If the image is not from one of the cameras
        return [int(-9999), [width, height], exif_json]
    elif (widths.index(width) != heights.index(height)): #if its not the right w x h combination
        return [int(-9999), [width, height], exif_json]
    try:
        model = exif_json[0]['EXIF:Model']
        if model == "SG565FV-8M": #HCO ScoutGuard (no temp)
            return [int(-9999), [width, height], exif_json]
    except:
        pass
    return [None, [width, height], exif_json]

def run_c2(image, training_path):
    '''Reads temperature values from HC500/HC600 Hyperfire cameras
        Writes any found mismatches on task3/mismatches/ in a .txt file
        w/ a randomly generated filename'''
    info = check(image)
    valid = check(image)[0]
    width, height = info[1][0], info[1][1]
    valid_widths = [1920, 2048]  # pictype 2 heights
    valid_heights = [1080, 1536]  # pictype 2 widths
    if width not in valid_widths or height not in valid_heights:
        return int(-9999)
    if not os.path.exists(os.getcwd() + '/temp/'):  # if temp folder doesnt exis, create one
        os.makedirs(os.getcwd() + '/temp/')
    if height == valid_heights[0] and width == valid_widths[0]: #1920x2040
        crop.crop_image(image, "temp/digits.jpg", 1710, 0, 115, 30)  # crops digits
    elif height == valid_heights[1] and width == valid_widths[1]: #2048x1536
        crop.crop_image(image, "temp/digits.jpg", 1850, 0, 105, 30)
    temperature = ocr_contour.recognize(os.getcwd() + '/temp/digits.jpg', training_path)  # recognize right digit
    # os.remove(os.getcwd()+'/temp/digits.jpg') #clean up temp dir
    ocr_temp = ''
    for digit in temperature:
        ocr_temp += digit
    if valid != None:
        exif_temp = int(valid)
    ocr_temp = int(ocr_temp)
    try:
        if ocr_temp != exif_temp:
            if not os.path.exists(os.getcwd() + '/mismatches/'):  # if temp folder doesnt exis, create one
                os.makedirs(os.getcwd() + '/mismatches/')
            f = open("mismatches/{0}.jpg".format(id_generator()), "w")
            f.write("exif temp: {0}, ocr temp: {1}, filename: {2}".format(exif_temp,ocr_temp,image))
        return int(ocr_temp)
    except:
        return int(-9999)

def run_c1(image, training_path):
    '''reads temperature of images in a directory. CAMERA 1 ONLY'''
    info = check(image)
    valid = info[0]
    width, height = info[1][0], info[1][1]
    exif_json = info[2]
    valid_heights = [2448] #pictype 3 heights
    valid_widths = [3264] #pictype 3 widths
    if width not in valid_widths or height not in valid_heights:
        return int(-9999)
    if valid != None:
        return valid
    if not os.path.exists(os.getcwd() + '/temp/'):  # if temp folder doesnt exis, create one
        os.makedirs(os.getcwd() + '/temp/')
    crop.crop_image(image,'temp/digits.jpg',  790, 2355, 375, 70)
    crop.invert(os.getcwd() + '/temp/digits.jpg')
    info = ocr_contour.recognize(os.getcwd() + '/temp/digits.jpg', training_path, True)
    temp = []
    for item in info:
        if item[0] == '45':
            x1,y1 = item[1][0], item[1][1]
    for item in info:
        if item[1][0] < x1:
            temp.append((item[0], item[1][0]))
    final = sorted(temp, key = lambda x: x[1])
    temperature = ''
    for i in final:
        temperature += i[0]
    try:
        return int(temperature)
    except:
        return int(-9999)

def run_c3(image, training_path):
    """reads temperature for a single image"""
    #FOR CAMERA 3 ONLY
    info = check(image)
    valid = info[0]
    if valid != None:
        return valid
    width, height = info[1][0], info[1][1]
    exif_json = info[2]
    valid_heights = [2124] #pictype 3 heights
    valid_widths = [3776] #pictype 3 widths
    if width not in valid_widths or height not in valid_heights:
        return int(-9999)
    if not os.path.exists(os.getcwd()+'/temp/'): #if temp folder doesnt exis, create one
        os.makedirs(os.getcwd()+'/temp/')
    crop.crop_image(image, "temp/digits.jpg", 435, 0, 70, 30) #crops digits
    temperature = ocr_contour.recognize('temp/digits.jpg', training_path) #recognize digit
    os.remove(os.getcwd()+'/temp/digits.jpg') #clean up temp dir
    temp = ''
    for i in temperature:
        temp +=i
    try:
        return int(temp)
    except:
        return int(-9999)

def run_c4(image, training_path):
    """reads temperature for a single image"""
    #FOR CAMERA 4 ONLY
    info = check(image)
    valid = info[0]
    if valid != None:
        return valid
    width, height = info[1][0], info[1][1]
    exif_json = info[2]
    valid_heights = [1512] #pictype 4 heights
    valid_widths = [2688] #pictype 4 widths
    if width not in valid_widths or height not in valid_heights:
        return int(-9999)
    if not os.path.exists(os.getcwd()+'/temp/'): #if temp folder doesnt exis, create one
        os.makedirs(os.getcwd()+'/temp/')
    crop.crop_image(image, "temp/digits.jpg",  825, 1445, 145, 70)
    temperature = ocr_contour.recognize('temp/digits.jpg', training_path, True) #recognize digits
    # im = cv2.imread('temp/digits.jpg') ##debugging
    # cv2.imshow('img', im) ##debugging
    # cv2.waitKey(0) ##debugging
    final = sorted(temperature, key = lambda x: x[1][0]) #sort from left to right
    os.remove(os.getcwd()+'/temp/digits.jpg') #clean up temp dir
    temp = ''
    for digit in final:
        temp += digit[0]
    try:
        return int(temp)
    except:
        return int(-9999)

def loop(type, path, debug = False):
    """Select camera 1,2 or 3"""
    if type == 4:
        for image in os.listdir(path):
            temp = run_c4(path+image, 'data/data_files/camera_1/')
            print int(temp), image
    if type == 2:
        for image in os.listdir(path):
            temp = run_c2(path+image, 'data/data_files/camera_2/')
            print int(temp)
            if debug == True:
                img = cv2.imread(path+image)
                cv2.imshow(image, img)
                key  = cv2.waitKey(0)
                print key
                cv2.destroyAllWindows()

    if type == 1:
        for image in os.listdir(path):
            temp = run_c1(path + image, 'data/data_files/camera_1/')
            print int(temp)


def main(pictype, base):
    # parser = argparse.ArgumentParser(description='OCR Recognition tool for Sedgwick Reserve photos')
    # parser.add_argument('pictype', action='store', type=int, help='1,2,3')
    # parser.add_argument('base', action='store', help='JPEG image')
    # # optional arguments
    # # parser.add_argument('--blur','-b',action='store',default=False,type=bool,help='day threshold')
    # args = parser.parse_args()
    # if args.pictype < -1 and args.pictype > 3:
    #     # 0 is hidden and used for testing
    #     print 'pictype must be 1,2, or 3'
    #     sys.exit(1)
    if str(base[-4:]).lower() != '.jpg':
        return int(-9999)
    try:
        if pictype == 3:
            temp = run_c3(base, 'backend/data/data_files/camera_3/')
            return int(temp)
        if pictype == 2:
            temp = run_c2(base, 'backend/data/data_files/camera_2/')
            return int(temp)
        if pictype == 1:
            temp = run_c1(base, 'backend/data/data_files/camera_1/')
            return int(temp)
        if pictype == 4:
            temp = run_c4(base, 'backend/data/data_files/camera_1/')
            return int(temp)
    except:
        return int(-9999)



######################################
if __name__ == "__main__":
    print main()
######################################