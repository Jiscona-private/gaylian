import random, os, datetime
from os.path import exists
from time import sleep

from flask import Flask, render_template, flash, redirect, request, url_for, send_from_directory, jsonify
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_socketio import SocketIO

# general preparation
bcrypt = Bcrypt()

# path preparation
UPLOAD_FOLDER = 'F:/Dokumente/Dokumente/Jakob/Gaylian Net/Code/github/gaylian/cloud/files'
NOTES_FOLDER = 'F:/Dokumente/Dokumente/Jakob/Gaylian Net/Code/github/gaylian/notes'
MD_FOLDER = 'F:/Dokumente/Dokumente/Jakob/Gaylian Net/Code/github/gaylian/markdowns'
ADMIN_PW = "GdSk1cktawyo"

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['NOTES_FOLDER'] = NOTES_FOLDER
app.config['MD_FOLDER'] = MD_FOLDER
app.config['ADMIN_PW'] = ADMIN_PW
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gaylian.db'
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'

socketio = SocketIO(app)
db = SQLAlchemy(app)

##### DATAMODELS #####

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    authDigit = db.Column(db.String(1), nullable=False)
    authHash = db.Column(db.String(120), nullable=False)
    storageUsed = db.Column(db.Integer, nullable=False)
    storageOwned = db.Column(db.Integer, nullable=False)

class Files(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fileCode = db.Column(db.String(32), unique=True, nullable=False)
    filename = db.Column(db.String(120), nullable=False)
    filePass = db.Column(db.String(132), nullable=True)
    uploadUser = db.Column(db.Integer, nullable=False)
    uploadTime = db.Column(db.DateTime(), default=datetime.datetime.now()) 

class Markdowns(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fileCode = db.Column(db.String(32), unique=True, nullable=False)
    filePass = db.Column(db.String(32), nullable=True)
    uploadUser = db.Column(db.Integer, nullable=False)
    uploadTime = db.Column(db.DateTime(), default=datetime.datetime.now()) 

class Notes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filePass = db.Column(db.String(32), nullable=True)
    ipAdr = db.Column(db.Integer, nullable=False)    

##### REDIRECTS #####
@app.route("/")
def start():
    return render_template('index.html')

# school docs

@app.route("/school/<code>", methods=['GET', 'POST'])
def schoolDoc(code):
    rand = random.randint(1,100)
    if rand == 1:
        return render_template('progressbar.html')
    else:
        file = Markdowns.query.filter_by(fileCode=code).first()
        docId = file.id

        if request.method == 'POST':
            if request.form['pw'] == file.filePass:
                with open(app.config["MD_FOLDER"]+'/'+str(docId)+'.md', 'r', encoding='utf-8') as f:
                    lines = f.read()
                return render_template('markdown.html', content=lines)
            return render_template('pw_input.html', error="Falsches Password")

        if (file.filePass == None):   
            with open(app.config["MD_FOLDER"]+'/'+str(docId)+'.md', 'r', encoding='utf-8') as f:
                lines = f.read()
            return render_template('markdown.html', content=lines)

        return render_template('pw_input.html')        

@app.route("/school", methods=['GET', 'POST'])
def schoolSearch():
    if request.method == 'POST':
        return redirect(url_for('schoolDoc', code=request.form['code']))
    return render_template('school.html')
    

@app.route('/school/new', methods=['GET', 'POST'])
def upload_md():
    if request.method == 'POST':
        # getting authCodes
        md = request.form['markdown']
        fileCode = request.form['filecode']
        authCode = request.form['authCode']

        if fileCode == "new":
            return render_template('create_md.html', error="OH MEIN GÖTT!!!! häckerangriff 🤯🤯🤯!!1! Nein, aber mal ehrlich: sehen wir wirklich so dumm aus?", )  

        if verify(request.form['authCode']) == True:
            if md:
                from webpages import Markdowns

                # get storageUsed and add filesize
                uploadUser = getCodeUser(authCode)

                if uploadUser.storageOwned < uploadUser.storageUsed:
                    return render_template('create_md.html', error="Ihr Speicher ist voll.", mdContent = md)            

                # check if code is already used
                codeUsed = Markdowns.query.filter_by(fileCode = fileCode).first()
                if codeUsed:
                    return render_template('create_md.html', error="Der Datei-Code wird bereits genutzt.", mdContent = md)
                # set filePass
                filePass = None
                if (request.form['filePass']):
                    filePass = request.form['filePass']

                # adding link to database
                
                newMD = Markdowns(fileCode = fileCode, filePass=filePass, uploadUser=uploadUser.id)
                db.session.add(newMD)
                db.session.commit()
                db.session.refresh(newMD)
                insertedId= newMD.id
                
                with open(app.config["MD_FOLDER"]+'/'+str(insertedId)+'.md', 'w', encoding='utf-8') as f:
                    f.write(md)

                filesize = os.stat(app.config["MD_FOLDER"]+'/'+str(insertedId)+'.md').st_size

                uploadUser.storageUsed = (uploadUser.storageUsed + filesize)
                db.session.commit()

                if uploadUser.storageOwned < uploadUser.storageUsed :
                    os.remove(app.config["MD_FOLDER"]+'/'+str(insertedId)+'.md') 
                    return render_template('file_upload.html', error="Ihr Speicherplatz reicht nicht mehr aus.", mdContent = md)
                return redirect(url_for('schoolDoc', code=fileCode))

        return render_template('create_md.html', error="Code ungültig!", mdContent = md)
    return render_template('create_md.html')

@app.route("/school/<code>/edit", methods=['GET', 'POST'])
def edit_md(code):
    file = Markdowns.query.filter_by(fileCode=code).first()

    if (request.method == 'POST'):
        if request.form['filecode'] == "new":
            return render_template('create_md.html', error="OH MEIN GÖTT!!!! häckerangriff 🤯🤯🤯!!1! Nein, aber mal ehrlich: sehen wir wirklich so dumm aus?", mdContent = md)

        # getting file and user        
        userId = file.uploadUser
        uploadUser = Users.query.filter_by(id=userId).first()

        authInput = request.form['authCode']          

        if bcrypt.check_password_hash(uploadUser.authHash, authInput[1:]):
            md = request.form['markdown']
            fileCode = request.form['filecode']

            sizeBefore = os.stat(app.config["MD_FOLDER"]+'/'+str(file.id)+'.md').st_size

            if md:
                # get storageUsed and add filesize
                if uploadUser.storageOwned < uploadUser.storageUsed:
                    return render_template('edit_md.html', error="Ihr Speicher ist voll.", mdContent = md)            

                # check if code is already used
                codeUsed = Markdowns.query.filter_by(fileCode = fileCode).first()
                if (codeUsed and (codeUsed.fileCode != fileCode)) :
                    return render_template('edit_md.html', error="Der Datei-Code wird bereits genutzt.",  mdContent = md)

                # changing link to database
                
                file.fileCode = fileCode
                # getting filepass
                filePass = None
                if (request.form['filePass']):
                    filePass = request.form['filePass']
                file.filePass = filePass
                db.session.commit()
                
                with open(app.config["MD_FOLDER"]+'/'+str(file.id)+'.md', 'w', encoding='utf-8') as f:
                    f.write(md)

                sizeAfter = os.stat(app.config["MD_FOLDER"]+'/'+str(file.id)+'.md').st_size

                uploadUser.storageUsed = (uploadUser.storageUsed + (sizeAfter - sizeBefore))
                db.session.commit()

                if uploadUser.storageOwned < uploadUser.storageUsed :
                    os.remove(app.config["MD_FOLDER"]+'/'+str(file.id)+'.md') 
                    return render_template('file_upload.html', error="Ihr Speicherplatz reicht nicht mehr aus.", mdContent = md)
                return redirect(url_for('schoolDoc', code=fileCode))
                    
        return render_template('edit_md.html', error="Falsches Password", mdContent = md)

    with open(app.config["MD_FOLDER"]+'/'+str(file.id)+'.md', 'r', encoding='utf-8') as f:
        lines = f.read()
    return render_template('edit_md.html', mdContent = lines)

@app.route("/cloud", methods=['GET', 'POST'])
def cloudSearch():
    if request.method == 'POST':
        return redirect(url_for('download_file', code=request.form['code']))
    return render_template('cloud.html')

# cloud
@app.route('/cloud/new', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':

        fileCode = request.form['filecode']
        authCode = request.form['authCode']
        # getting authCodes
        if fileCode == "new":
            return render_template('create_md.html', error="OH MEIN GÖTT!!!! häckerangriff 🤯🤯🤯!!1! Nein, aber mal ehrlich: sehen wir wirklich so dumm aus?")  

        if verify(authCode) == True:

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
                from webpages import Files

                # get storageUsed and add filesize
                uploadUser = getCodeUser(authCode)

                if uploadUser.storageOwned < uploadUser.storageUsed:
                    return render_template('file_upload.html', error="Ihr Speicher ist voll.")            

                # check if code is already used
                codeUsed = Files.query.filter_by(fileCode=fileCode).first()
                if codeUsed:
                    return render_template('file_upload.html', error="Der Datei-Code wird bereits genutzt.")
                

                filename = secure_filename(file.filename)

                # set filepass
                filePass = None
                if request.form['filePass']:
                    filePass = request.form['filePass']



                # adding link to database
                newFile = Files(filename=filename, fileCode=fileCode, filePass=filePass, uploadUser=uploadUser.id)
                db.session.add(newFile)
                db.session.commit()
                db.session.refresh(newFile)
                insertedId= newFile.id

                # upload
                os.mkdir(os.path.join(app.config['UPLOAD_FOLDER'], str(insertedId)))
                
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], str(insertedId), filename))

                filesize = os.stat(os.path.join(app.config['UPLOAD_FOLDER'], str(insertedId), filename)).st_size

                uploadUser.storageUsed = (uploadUser.storageUsed + filesize)
                db.session.commit()

                if uploadUser.storageOwned < uploadUser.storageUsed :
                    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], str(insertedId)+filename)) 
                    return render_template('file_upload.html', error="Ihr Speicherplatz reicht nicht mehr aus.")
                return redirect(url_for('download_file', code=fileCode))
        return render_template('file_upload.html', error="Code ungültig!")
    return render_template('file_upload.html')

@app.route('/cloud/<code>')
def offer_file(code):
    file = Files.query.filter_by(fileCode=code).first()
    if (file == None):
        return render_template('fileNotFound.html')

    file_split = os.path.splitext(file.filename)
    if (file_split[1] == '.png'):
        return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER'], str(file.id)), file.filename)

    return render_template('file_offer.html', filename = file.filename)

@app.route('/cloud/<code>/download', methods=['GET', 'POST'])
def download_file(code):
    file = Files.query.filter_by(fileCode=code).first()
    if (file == None):
        return render_template('fileNotFound.html')

    if request.method == 'POST':
        if request.form['pw'] == file.filePass:
            return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER'], str(file.id)), file.filename)
        return render_template('pw_input.html', error="Falsches Password")

    if (file.filePass == None):   
        return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER'], str(file.id)), file.filename)

    

# notes
@app.route('/notes/new', methods=['GET', 'POST'])
def write_note():
    if request.method == 'POST':
        if len(request.form['content']) > 1000:
            return render_template('write_note.html', error="Zu lang!", note=request.form['content'])
        # checking if IP already had to many requests
        from webpages import Notes
        writtenNotes = Notes.query.filter_by(ipAdr=request.remote_addr).count()

        if (writtenNotes >= 1000):
            return render_template('write_note.html', error="Sie haben bereits zu viele Notizen verfasst.")

        else:
            # wait 1 sec (stop dos attacks)
            sleep(1)
            # writing database entry
            # set filePass
            filePass = None
            if request.form['filePass']:
                filePass = request.form['filePass']

            # adding link to database
                
            newNote = Notes(filePass=filePass, ipAdr=request.remote_addr)
            db.session.add(newNote)
            db.session.commit()
            db.session.refresh(newNote)
            insertedId= newNote.id
            
            with open(app.config["NOTES_FOLDER"]+'/'+str(insertedId)+'.txt', 'w', encoding='utf-8') as f:
                f.write(request.form['content'])
            
            return redirect(url_for('show_note', number=insertedId))
    return render_template('write_note.html')

@app.route('/notes/<number>', methods=["POST","GET"])
def show_note(number):
    note = Notes.query.filter_by(id=number).first()

    if (note==None):
        return render_template('fileNotFound.html')

    if request.method == 'POST':
        if request.form['pw'] == note.filePass:
            return send_from_directory(app.config["NOTES_FOLDER"], str(number)+'.txt')
        return render_template('pw_input.html', error="Falsches Password")

    if (note.filePass == None):   
        return send_from_directory(app.config["NOTES_FOLDER"], str(number)+'.txt')
    return render_template('pw_input.html')
    
# admin

@app.route('/user/new', methods=["POST","GET"])
def createUser():
    if request.method == "POST":
        if (request.form['adminName'] == "./admin" and request.form['adminPassword'] == app.config['ADMIN_PW']):
            username = request.form['uname']
            pw = request.form['password']
            storage = int(request.form['storage'])
            

            newUser = Users(username=username, authDigit=pw[0], authHash=bcrypt.generate_password_hash(pw[1:]), storageUsed=0, storageOwned=(storage * 1024 * 1024))
            db.session.add(newUser)
            db.session.commit()
            db.session.refresh(newUser)

            return "done"
    return render_template('createUser.html')

## === ERROR HANDLER ===

@app.errorhandler(404)
def not_found(e):
  return render_template("404.html")

@app.errorhandler(500)
def server_error(e):
  return render_template("500.html")

## === DEFS ===

def verify(passcode):
    users = Users.query.filter_by(authDigit=passcode[0]).all()
    for passUser in users:
        if bcrypt.check_password_hash(passUser.authHash, passcode[1:]):
            return True
    return False

def getCodeUser(passcode):
    users = Users.query.filter_by(authDigit=passcode[0]).all()
    for passUser in users:
        if bcrypt.check_password_hash(passUser.authHash, passcode[1:]):
            return passUser
    return None


if __name__ == '__main__':
    app.run()