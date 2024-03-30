from flask import Flask, render_template
app = Flask(__name__)
JOBS = [
    {'id': 1,
    'Role': 'Data Scientist',
    'Salary': 1500000,
    'Location' : 'Bengaluru'
    },
    {'id': 2,
    'Role': 'Data Analyst',
    'Location' : 'Delhi'
    },
    {'id': 3,
    'Role': 'Software Engineer',
    'Salary': 300000,
    'Location' : 'USA'
    }
]
@app.route('/')
def helloWord():
    return render_template('home.html', jobs=JOBS, company='Jovian Careers')
if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)