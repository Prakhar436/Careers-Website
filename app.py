from flask import Flask, render_template, jsonify
from database import load_jobs, get_job

app = Flask(__name__)

@app.route('/')
def helloWord():
    ALLJOBS = load_jobs()
    return render_template('home.html', jobs=ALLJOBS)

@app.route('/job/<id>/')
def show_job(id):
    JOB = get_job(id)
    if not JOB: return "Not Found",404  #if JOB is None, return a 404
    return render_template('jobpage.html',job = JOB)
    
if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)