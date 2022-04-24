from enum import auto
import numbers
import random, os 
from os.path import exists

from flask import Flask, render_template, flash, redirect, request, url_for, send_from_directory
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy

# path preparation
UPLOAD_FOLDER = 'F:/Dokumente/Dokumente/Jakob/Gaylian Net/Code/project/cloud/files'
notes_folder = 'F:/Dokumente/Dokumente/Jakob/Gaylian Net/Code/project/notes'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gaylian.db'
db = SQLAlchemy(app)

##### DATAMODELS #####

class CloudUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    authCode = db.Column(db.String(120), unique=True, nullable=False)

class files(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fileCode = db.Column(db.String(120), unique=True, nullable=False)
    fileformat = db.Column(db.String(8), nullable=False)

##### REDIRECTS #####
# school docs

@app.route("/school/<docName>")
def schoolDoc(docName):
    rand = random.randint(1,100)
    if rand == 1:
        return render_template('progressbar.html')
    else:
        with open('./markdowns/'+docName+'.md', 'r', encoding='utf-8') as f:
            lines = f.read()
        return render_template('markdown.html', content=lines)

@app.route("/school")
def schoolSearch():
    return render_template('school.html')

@app.route("/cloud")
def cloudSearch():
    return render_template('cloud.html')

# cloud
@app.route('/cloud/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # getting authCodes
        usedCode = request.form['authCode']
        authed = CloudUser.query.filter_by(authCode=usedCode).first()

        if authed:
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

            if file:
                from webpages import files
                # check if code is already used
                codeUsed = files.query.filter_by(fileCode=request.form['filecode']).first()
                if codeUsed:
                    return render_template('file_upload.html', error="Der Datei-Code wird bereits genutzt.")

                filename = secure_filename(file.filename)
                # getting file format
                fileparts = os.path.splitext(filename)
                fileformat = fileparts[1]

                # adding link to database
                fileCode = request.form['filecode']
                newFile = files(fileformat=fileformat, fileCode=fileCode)
                db.session.add(newFile)
                db.session.commit()
                db.session.refresh(newFile)
                insertedId= newFile.id

                # upload
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], str(insertedId)+fileformat))
                return redirect(url_for('download_file', code=fileCode))
        return render_template('file_upload.html', error="Code ungültig!")
    return render_template('file_upload.html')

@app.route('/cloud/files/<code>')
def download_file(code):
    file = files.query.filter_by(fileCode=code).first()
    fileName = str(file.id)+file.fileformat
    return send_from_directory(app.config["UPLOAD_FOLDER"], fileName)

# notes
@app.route('/notes/new', methods=['GET', 'POST'])
def write_note():
    if request.method == 'POST':
        if len(request.form['content']) > 1000:
            return render_template('write_note.html', error="Zu lang!")
        else:
            # getting highest file-number
            i = 0
            while (exists(notes_folder+'/'+str(i)+'.txt') == True):
                i=i+1
            
            with open(notes_folder+'/'+str(i)+'.txt', 'w') as f:
                f.write(request.form['content'])
            
            return redirect(url_for('show_note', number=i))
    return render_template('write_note.html')

@app.route('/notes/<number>')
def show_note(number):
    return send_from_directory(notes_folder, str(number)+'.txt')
