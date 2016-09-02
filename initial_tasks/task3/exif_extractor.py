import pyexifinfo as exif

def test(image):
    e = exif.get_xml(image)
    json = exif.get_json(image)
    print json[0]['MakerNotes:AmbientTemperatureFahrenheit']
#SG565FV-8M

test("/home/andy/ocr_knn/initial_tasks/task3/testimages/bonehole0609.JPG")