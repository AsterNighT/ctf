from flask import Flask, request, send_file, session
from exiftool import ExifToolHelper
import os
import base64

HOST = '0.0.0.0' if os.environ.get('NODEBUG') else '127.0.0.1'
PORT = 5000

app = Flask(__name__)
app.secret_key = 'ZJUCTF{SESE_IS_NOT_PERMITED}'

EXIFTOOL_PATH = None

def parse_img(img):
    et = ExifToolHelper(executable=EXIFTOOL_PATH)
    d = et.get_metadata(img)[0]
    d.pop('File:FilePermissions')
    return d

def edit_img(img, tags):
    et = ExifToolHelper(executable=EXIFTOOL_PATH)
    res = et.set_tags([img], tags, params=["-P", "-overwrite_original"])
    return res


@app.route('/')
def index():
    return send_file('static/index.html')

@app.route('/upload', methods=['POST'])
def upload():
    img = request.files.get('img')
    if not img:
        return "no image specified", 403
    print(img.filename)
    session['img'] = img.filename
    img_path = os.path.join('upload', img.filename)
    img.save(img_path)
    return parse_img(img_path)

@app.route('/edit', methods=['POST'])
def edit():
    if not session.get('img'):
        return 'no image uploaded yet!', 403
    data = request.json
    print(data)
    img_path = os.path.join('upload', session['img'])
    return { 
        'msg': edit_img(img_path, data).strip(),
        'data': base64.b64encode(open(img_path, 'rb').read()).decode(),
        'type': 'image/' + session['img'].split('.')[-1]
    }


if __name__ == '__main__':
    app.run(HOST, PORT)