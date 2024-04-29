from flask import Flask, render_template, get_flashed_messages, jsonify, flash, request, redirect, url_for
from database import load_jobs, get_job, store_application, isDuplicateApplication
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
import os
app = Flask(__name__)
UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'uploads') #the best way to give path. Works on development as well as production server
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024  # 1MB
app.secret_key = os.urandom(24) #generate a random secret key, used in session cookies which store flash messages
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def helloWord():
    ALLJOBS = load_jobs()
    return render_template('home.html', jobs=ALLJOBS)

@app.route('/job/<id>/')
def show_job(id):
    JOB = get_job(id)
    if not JOB: return "Not Found",404  #if JOB is None, return a 404
    return render_template('jobpage.html',job = JOB)

@app.route('/job/<id>/apply', methods = ['POST','GET'])
def save_job(id):
    get_flashed_messages() #flush all the pre-stored flash messages
    #first we validate file type and size, then we check if the application is duplicate
    if 'cv' not in request.files:
        flash('No file part', 'error')
        #we redirect to application page, right at the application form. For this, html form must have an id = "application_form"
        return redirect(url_for('show_job',id = request.view_args['id']) + '#application_form')
    file = request.files['cv']
    # If user does not select file, browser also submits an empty part without filename, so we should check if the filename is empty
    if file.filename == '':
        flash('No selected file', 'error')
        return redirect(url_for('show_job',id = request.view_args['id']) + '#application_form')

    if file and allowed_file(file.filename):

        if(isDuplicateApplication(id, request.form)):
            flash(f'User {request.form.get("name")} has already applied for this job', 'duplicate')
            return redirect(url_for('show_job',id = request.view_args['id']))
        #if not duplicate, save file into uploads folder and store application data in database
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        application_data = request.form
        pdfFile = [filename, file_path]
        store_application(id, application_data, pdfFile) 
        flash("Your application form has been submitted successfully!", 'success')
        return redirect(url_for('show_job',id = id))
    else:
        flash('File type not allowed', 'error')
        return redirect(url_for('show_job',id = request.view_args['id']) + '#application_form')

    #this is a fallback, if the user somehow manages to bypass the allowed_file check
    return render_template('home.html')

#if file size > 1MB, then RequestEntityTooLarge error will be thrown, which will be handled by this error handler
@app.errorhandler(RequestEntityTooLarge)
def handle_file_size_too_large(e):
    flash('File size must be less than 1MB', 'error')
    return redirect(url_for('show_job',id = request.view_args['id']) + '#application_form')
    
if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)