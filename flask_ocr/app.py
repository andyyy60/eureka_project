#!flask/bin/python
import os, random, string
from flask import Flask, request, jsonify
from backend import crop_and_recognize
from healthcheck import HealthCheck, EnvironmentDump

app = Flask(__name__)
ALLOWED_EXTENSIONS = set(['jpg'])

health = HealthCheck(app, "/healthcheck")
envdump = EnvironmentDump(app, "/environment")

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def run_script(num, filename):
    output = crop_and_recognize.main(int(num), filename)
    return output


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods= ['POST'])
def upload_file():
    f = request.files['files']
    filename = request.form['filename']
    pictype = request.form['pictype']
    if request.method == 'POST' and allowed_file(f.filename):
        f.save(filename)
    elif not allowed_file(f.filename):
        return "only .jpg extensions accepted"
    try:
        output = crop_and_recognize.main(int(pictype), filename)
    except:
        return "Please try with another camera digit (1-3)\n"
    os.remove(filename)
    return jsonify({'temperature': output})


if __name__ == '__main__':
    app.debug = False
    app.run(host='0.0.0.0')