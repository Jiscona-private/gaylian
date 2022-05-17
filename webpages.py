from enum import auto
import random, os
from os.path import exists

from flask import Flask, render_template, flash, redirect, request, url_for, send_from_directory
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
#from flask_bcrypt import Bcrypt

# path preparation
UPLOAD_FOLDER = 'F:/Dokumente/Dokumente/Jakob/Gaylian Net/Code/project/cloud/files'
NOTES_FOLDER = 'F:/Dokumente/Dokumente/Jakob/Gaylian Net/Code/project/notes'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['NOTES_FOLDER'] = NOTES_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gaylian.db'
db = SQLAlchemy(app)

##### DATAMODELS #####

class user(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    authDigit = db.Column(db.String(1), nullable=False)
    authHash = db.Column(db.String(120), nullable=False)
    storageUsed = db.Column(db.Integer, nullable=False)
    storageOwned = db.Column(db.Integer, nullable=False)

class file(db.Model):
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
        authed = user.query.filter_by(authCode=usedCode).first()

        if authed:
            # check if the post request has the file part
            if 'file' not in request.file:
                flash('No file part')
                return redirect(request.url)

            file = request.file['file']
            # If the user does not select a file, the browser submits an
            # empty file without a filename.

            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)

            if file:
                from webpages import file
                # check if code is already used
                codeUsed = file.query.filter_by(fileCode=request.form['filecode']).first()
                if codeUsed:
                    return render_template('file_upload.html', error="Der Datei-Code wird bereits genutzt.")

                filename = secure_filename(file.filename)
                # getting file format
                fileparts = os.path.splitext(filename)
                fileformat = fileparts[1]

                # adding link to database
                fileCode = request.form['filecode']
                newFile = file(fileformat=fileformat, fileCode=fileCode)
                db.session.add(newFile)
                db.session.commit()
                db.session.refresh(newFile)
                insertedId= newFile.id

                # upload
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], str(insertedId)+fileformat))
                return redirect(url_for('download_file', code=fileCode))
        return render_template('file_upload.html', error="Code ungültig!")
    return render_template('file_upload.html')

@app.route('/cloud/<code>')
def download_file(code):
    file = file.query.filter_by(fileCode=code).first()
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
            while (exists(app.config["NOTES_FOLDER"]+'/'+str(i)+'.txt') == True):
                i=i+1
            
            with open(app.config["NOTES_FOLDER"]+'/'+str(i)+'.txt', 'w') as f:
                f.write(request.form['content'])
            
            return redirect(url_for('show_note', number=i))
    return render_template('write_note.html')

@app.route('/notes/<number>')
def show_note(number):
    return send_from_directory(app.config["NOTES_FOLDER"], str(number)+'.txt')

@app.route('/user/new', methods=["POST","GET"])
def createUser():
    if request.method == "POST":
        if (request.form['adminName'] == "./admin"):
            username = request.form['username']
            pw = username = request.form['password']
            storage = request.form['storage']

            newUser = user(username=username, authDigit=pw[0], authHash=pw[1:], storageUsed=0, storageOwned=(storage*1024*1024))
            db.session.add(newUser)
            db.session.commit()
            db.session.refresh(newUser)

            return "done"
    return render_template('createUser.html')

def verify(passcode):
    user.query.filter_by(authDigit=passcode[0]).all()

    return True


if __name__ == '__main__':
    app.run()