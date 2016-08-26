#!flask/bin/python
import os, json, random, string
from flask import Flask, request, render_template, jsonify
from backend import crop_and_recognize

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def run_script(num, filename):
    output = crop_and_recognize.main(int(num), filename)
    return output


app = Flask(__name__)
ALLOWED_EXTENSIONS = set(['jpg'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods= ['POST'])
def upload_file():
    f = request.files['files']
    if request.method == 'POST' and allowed_file(f.filename):
        f.save("temperature.jpg")
        return '200'
    else:
        return "only .jpg extensions accepted"

@app.route('/api/<int:task_id>', methods=['GET'])
def get_task(task_id):
    try:
        output = crop_and_recognize.main(int(task_id), "temperature.jpg")
    except:
        return "Please try with another camera digit (1-3)\n"
    print output
    return jsonify({'temperature': output})


if __name__ == '__main__':
    app.debug = True
    app.run()