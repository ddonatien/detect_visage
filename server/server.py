from lib.rpc import Rpc
import os

from flask import Flask, render_template, request
from flask_uploads import IMAGES, UploadSet, configure_uploads

app = Flask(__name__)

photos = UploadSet('photos', IMAGES)

app.config['UPLOADED_PHOTOS_DEST'] = 'static/img'
configure_uploads(app, photos)


@app.route('/upload', methods=['POST'])
def upload():
    # detector = DetectVisage()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        rpc = Rpc()
        return rpc.call(
            os.path.dirname(os.path.realpath(__file__)) + "/static/img/" +
            filename)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
