from flask import Flask, render_template
from database import load_jobs 
app = Flask(__name__)
JOBS = load_jobs()
print(JOBS)
@app.route('/')
def helloWord():
    return render_template('home.html', jobs=JOBS, company='Jovian Careers')
if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)