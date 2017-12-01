import os
import base64
import jinja2
from flask import Flask, request, flash, redirect, render_template, url_for, send_from_directory, make_response, send_file
from jinja2 import Environment
from werkzeug.utils import secure_filename

from io import BytesIO
from PIL import Image

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

app.secret_key = b'\\\xb8\x83\xcd\xb1\xda\x8a\x8fP\xf6+\xb0\xcd\xe7\xd2-\x947\xf1s\t\x99U,'


# Check if an extension is valid
def allowed_file(filename):
    try:
        value = '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
        return value
    except ValueError:
        return False


# environment = Environment()
# environment.filters['b64decode'] = base64.b64decode

jinja2.filters.FILTERS['b64decode'] = base64.b64decode


@app.route("/", methods=['GET', 'POST'])
def index(context=None):
    if request.method == 'POST':
        if 'photo' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['photo']

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            # filename = secure_filename(file.filename)
            # # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            #
            # # return redirect(url_for('uploaded_image', filename=filename))
            # # return render(request, 'index.html', context)
            # # return render_template('index.html', context=context)
            # resp = make_response(render_template('index.html', context=context))
            # print('respo: ', resp)
            # print(dir(resp))
            # return resp
            # print('file: ', file)
            print('dir: ', dir(file))

            # return render_template('index.html', encoded_image=file)

            # file_encode = base64.b64encode(file.read()).decode()
            # print('file_encode: ', file_encode)
            # return render_template('index.html', encoded_image=file)
            # saved_image = {}

            # filename = secure_filename(file.filename)
            # file.save(file)
            # file.close()
            # return render_template('index.html', encoded_image=file)

            # Saving file in-memory
            file_obj = BytesIO()
            file.save(file_obj)

            # Head back to the beginning of the file
            file_obj.seek(0)

            # img = Image.open(BytesIO(file.read()))
            return send_file(file_obj, mimetype=file.content_type)
            # return render_template('index.html', encoded_image=img)

        else:
            flash('Invalid file format')
            return redirect(request.url)

    return render_template('index.html')


@app.route('/images/')
def uploaded_image(context):
    # return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
