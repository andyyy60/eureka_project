''''Author: Andy Rosales Elias, EUREKA! 2016, Univeristy of California, Santa Barbara | andy00@umail.ucsb.edu'''
import crop, ocr_contour, os, time, cv2, argparse, sys
import pyexifinfo as exif
from PIL import Image

def check(base):
    im = Image.open(base)
    width, height = im.size
    widths = [3264,1920,3776]
    heights = [2448,1080,2124]
    exif_json = exif.get_json(base)
    try:
        temp = exif_json[0]['MakerNotes:AmbientTemperatureFahrenheit']
        return [int(temp[:-2]), [width, height], exif_json]
    except:
        pass
    if (width not in widths) or (height not in heights): #If the image is not from one of the cameras
        return [-9999, [width, height], exif_json]
    elif (widths.index(width) != heights.index(height)): #if its not the right w x h combination
        return [-9999, [width, height], exif_json]
    try:
        model = exif_json[0]['EXIF:Model']
        if model == "SG565FV-8M": #HCO ScoutGuard (no temp)
            return [-9999, [width, height], exif_json]
    except:
        pass
    return [None, [width, height], exif_json]

def run_c2(image, training_path):
    '''reads temperature of images in a directory'''
    info = check(image)
    valid = check(image)[0]
    if valid != None:
        return valid
    width, height = info[1][0], info[1][1]
    exif_json = info[2]
    valid_heights = [3776, 1920, 2048] #pictype 3 heights
    valid_widths = [2124, 1080, 1536] #pictype 3 widths
    if width not in valid_widths or height not in valid_heights:
        return -9999
    if not os.path.exists(os.getcwd()+'/temp/'): #if temp folder doesnt exis, create one
        os.makedirs(os.getcwd()+'/temp/')
    crop.crop_image(image, "temp/digits.jpg", 1710, 0, 115, 30) #crops digits
    temperature = ocr_contour.recognize(os.getcwd()+'/temp/digits.jpg', training_path) #recognize right digit
    os.remove(os.getcwd()+'/temp/digits.jpg') #clean up temp dir
    temp = ''
    for digit in temperature:
        temp += digit
    try:
        return int(temp)
    except:
        return -9999

def run_c1(image, training_path):
    '''reads temperature of images in a directory. CAMERA 1 ONLY'''
    info = check(image)
    valid = info[0]
    if valid != None:
        return valid
    width, height = info[1][0], info[1][1]
    exif_json = info[2]
    valid_heights = [2448] #pictype 3 heights
    valid_widths = [3264] #pictype 3 widths
    if width not in valid_widths or height not in valid_heights:
        return -9999
    if not os.path.exists(os.getcwd() + '/temp/'):  # if temp folder doesnt exis, create one
        os.makedirs(os.getcwd() + '/temp/')
    crop.crop_image(image,'temp/digits.jpg',  800, 2350, 100, 95)
    crop.invert(os.getcwd() + '/temp/digits.jpg')
    digits = len(ocr_contour.recognize(os.getcwd() + '/temp/digits.jpg', training_path))
    temperature = ''
    if digits == 1:  # crop rightmost digit
        crop.crop_image(image, "temp/1.jpg", 795 + 35, 2350 + 15, 35, 55)
        crop.invert(os.getcwd() + '/temp/1.jpg')
        temperature = ocr_contour.recognize(os.getcwd() + '/temp/1.jpg', training_path)
        os.remove(os.getcwd() + '/temp/1.jpg')  # clean up temp dir
    if digits == 2:#If there's two digits, crop them to get them in order
        crop.crop_image(image, "temp/1.jpg", 795 + 35, 2350 + 15, 35, 55)
        crop.crop_image(image, "temp/2.jpg", 795, 2350 + 15, 38, 55)
        crop.invert(os.getcwd() + '/temp/1.jpg')
        crop.invert(os.getcwd() + '/temp/2.jpg')
        right = ocr_contour.recognize(os.getcwd() + '/temp/1.jpg', training_path)
        left = ocr_contour.recognize(os.getcwd() + '/temp/2.jpg', training_path)
        temperature = left[0] + right[0]
        os.remove(os.getcwd() + '/temp/1.jpg')  # clean up temp dir
        os.remove(os.getcwd() + '/temp/2.jpg')  # clean up temp dir
    elif digits == 3:#Edge case, crop 3 numbers and ignore any other symbols
        crop.crop_image(image, "temp/1.jpg", 795 + 35, 2350 + 15, 35, 55)
        crop.crop_image(image, "temp/2.jpg", 795, 2350 + 15, 38, 55)
        crop.crop_image(image, "temp/3.jpg", 800+64, 2365, 100-57, 55)
        crop.invert(os.getcwd() + '/temp/1.jpg')
        crop.invert(os.getcwd() + '/temp/2.jpg')
        crop.invert(os.getcwd() + '/temp/3.jpg')
        right = ocr_contour.recognize(os.getcwd() + '/temp/1.jpg', training_path)
        left = ocr_contour.recognize(os.getcwd() + '/temp/2.jpg', training_path)
        extra = ocr_contour.recognize(os.getcwd() + '/temp/3.jpg', training_path)
        temperature = left[0]+extra[0] + right[0]
    try:
        return int(temperature)
    except:
        return -9999

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
        return -9999
    if not os.path.exists(os.getcwd()+'/temp/'): #if temp folder doesnt exis, create one
        os.makedirs(os.getcwd()+'/temp/')
    crop.crop_image(image, "temp/digits.jpg", 435, 0, 70, 30) #crops digits
    temperature = ocr_contour.recognize('temp/digits.jpg', training_path) #recognize right digit
    os.remove(os.getcwd()+'/temp/digits.jpg') #clean up temp dir
    temp = ''
    for digit in temperature:
        temp += digit
    try:
        return int(temp)
    except:
        return -9999


def loop(type, path, debug = False):
    """Select camera 1,2 or 3"""
    if type == 3:
        for image in os.listdir(path):
            temp = run_c3(path+image, 'data/data_files/camera_3/')
            print "Temp is: {0}".format(temp)
    if type == 2:
        for image in os.listdir(path):
            temp = run_c2(path+image, 'data/data_files/camera_2/')
            print "Temp is: {0}".format(temp)
            if debug == True:
                img = cv2.imread(path+image)
                cv2.imshow(image, img)
                key  = cv2.waitKey(0)
                print key
                cv2.destroyAllWindows()

    if type == 1:
        for image in os.listdir(path):
            temp = run_c1(path + image, 'data/data_files/camera_1/')
            print "Temp is: {0}".format(temp)


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
        return -9999
    if pictype == 3:
        temp = run_c3(base, 'backend/data/data_files/camera_3/')
        return int(temp)
    if pictype == 2:
        temp = run_c2(base, 'backend/data/data_files/camera_2/')
        return int(temp)
    if pictype == 1:
        temp = run_c1(base, 'backend/data/data_files/camera_1/')
        return int(temp)

# crop.crop_image('/home/andy/Downloads/BoneH_2015-08-27_16-03-05_7659.JPG', "digits", 435, 0, 70, 30)  # crops digits

# print main(3,'/home/andy/Downloads/BoneH_2015-08-27_09-27-31_7589.JPG')