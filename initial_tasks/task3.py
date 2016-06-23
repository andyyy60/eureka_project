import Image

def crop_image(input_image, output_image, start_x, start_y, width, height):
    #temperature is at crop_image("img.JPG","output", 1750, 0, 150, 40)
    input_img = Image.open(input_image)
    box = (start_x, start_y, start_x + width, start_y + height)
    output_img = input_img.crop(box)
    output_img.save(output_image +".JPG")


def main():
    crop_image("img.JPG","output", 1750, 0, 150, 40)

if __name__ == '__main__': main()