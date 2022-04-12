import random, os

from flask import Flask, render_template, flash, redirect, request, url_for, send_from_directory
from werkzeug.utils import secure_filename

# cloud preparation
UPLOAD_FOLDER = 'F:/Dokumente/Dokumente/Jakob/Gaylian Net/Code/project/venv/cloud/files'
# ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}     === for securing cross site scripting with php/simliar

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

##### REDIRECTS #####
# school docs

@app.route("/school/<docName>")
def schoolDoc(docName):
    rand = random.randint(1,100)
    if rand == 1:
        return render_template('progressbar.html')
    else:
        with open('./venv/markdowns/'+docName+'.md', 'r', encoding='utf-8') as f:
            lines = f.read()
        return render_template('markdown.html', content=lines)

@app.route("/school")
def schoolSearch():
    return render_template('school.html')

# cloud
#def allowed_file(filename):
#    return '.' in filename and \
#           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/cloud/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if request.form['authCode'] == 'Giss':
            # check if the post request has the file part
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']
            # If the user does not select a file, the browser submits an
            # empty file without a filename.
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file: # and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                return redirect(url_for('download_file', name=filename))
        else:
            return render_template('file_upload.html', msg="Code ungültig!")
    return render_template('file_upload.html')

@app.route('/cloud/files/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)



