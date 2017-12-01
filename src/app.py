from io import BytesIO
from flask import Flask, request, flash, redirect, render_template, send_file

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

app.secret_key = b'\\\xb8\x83\xcd\xb1\xda\x8a\x8fP\xf6+\xb0\xcd\xe7\xd2-\x947\xf1s\t\x99U,'


# Check if an extension is valid
def allowed_file(filename):
    try:
        value = '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
        return value
    except ValueError:
        return False


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'photo' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['photo']

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):

            # Save file in-memory
            file_obj = BytesIO()
            file.save(file_obj)

            # Head back to the beginning of the file
            file_obj.seek(0)

            return send_file(file_obj, mimetype=file.content_type)

        else:
            flash('Invalid file format')
            return redirect(request.url)

    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
