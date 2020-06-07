import os
import re
import time
import pickle
import shutil
from flask import *
from werkzeug.utils import secure_filename
import cv2
from seam_carving import seam_carve
import numpy as np

UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg','mp4'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def is_image(filename):
    image_extensions={'png', 'jpg', 'jpeg'}
    return filename.rsplit('.', 1)[1].lower() in image_extensions


@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html', title='Seam Carving')

@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    print(request)
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file! Please choose a file for seam carving')
            return redirect(url_for('index'))
        if not allowed_file(file.filename):
            s=list(ALLOWED_EXTENSIONS)
            message='File Extension Not Supported! Supported Formats: '+', '.join(str(e) for e in s)
            flash(message)
            return redirect(url_for('index'))
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            dirname = str(filename.rsplit('.', 1)[0])
            dir_path = os.path.join(app.config['UPLOAD_FOLDER'], dirname)
            file_path = os.path.join(dir_path, filename)
            if os.path.exists(dir_path):
                shutil.rmtree(dir_path)
                os.makedirs(dir_path)
            file.save(file_path)
            if is_image(file_path):
                height, width=image_size(file_path)
                payload={
                    "filename": str(file_path),
                    "height": height,
                    "width": width
                }
                return render_template('seam_image.html', **payload)
            else:
                height,width,frames=video_size(file_path)
                payload={
                    "filename": str(file_path),
                    "height": height,
                    "width": width,
                    "frames": frames
                }
                return render_template('seam_video.html', **payload)
        print("unexpected error")
    print("method was not post")
    return redirect(url_for('index'))


@app.route('/seam_creator', methods=['GET', 'POST'])
def get_seams():
    """Get the seams from the image here"""
    # dW = int(np.ceil(height*16/9)) - width
    # width=request.file
    if request.method == 'POST':
        print("post method detected")
        file_path=request.form["filepath"]
        im=cv2.imread(file_path)
        height, width=image_size(file_path)
        output = seam_carve(im, height, width, file_path)
        payload={
            "filename": str(file_path),
            "height": height,
            "width": width
        }
        return render_template('edit_image.html', **payload)
    return render_template('seam_image.html', **payload)

@app.route('/resize_image', methods=['GET', 'POST'])
def resize_image():
    """Get the seams from the image here"""
    # dW = int(np.ceil(height*16/9)) - width
    # width=request.file
    if request.method == 'POST':
        print("post method detected")
        file_path=request.form["filepath"]
        im=cv2.imread(file_path)
        height, width=image_size(file_path)
        new_height=int(request.form["new_height"])
        new_width=int(request.form["new_width"])
        dy=new_height-height
        dx=new_width-width
        new_name=str(file_path.rsplit('.', 1)[0])+"resize."+str(file_path.rsplit('.', 1)[1])
        print(new_name)
        print(file_path)
        output = seam_carve(im, dy, dx, file_path)
        cv2.imwrite(new_name, output)
        print("new_name:",new_name)
        payload={
            "filename": str(file_path),
            "height": height,
            "width": width,
            "resize":str(new_name)
        }
        return render_template('edit_image.html', **payload)

def image_size(file_path):
    handle=cv2.imread(file_path)
    height, width = np.shape(handle)[:2]
    return height, width

def video_size(file_path):
    vid = cv2.VideoCapture(file_path)
    height = vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
    width = vid.get(cv2.CAP_PROP_FRAME_WIDTH)
    frames = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))
    return height,width,frames



if __name__ == '__main__':
    app.run(debug=True)
