import pyexifinfo as exif

def test(image):
    e = exif.get_xml(image)
    json = exif.get_json(image)
    print json[0]
#SG565FV-8M

test("/home/andy/images/vulture.JPG")