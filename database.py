# IMPORT THE SQALCHEMY LIBRARY's CREATE_ENGINE METHOD
from sqlalchemy import create_engine, text
import os
# DEFINE THE DATABASE CREDENTIALS
user = os.environ['USERNAME']
password = os.environ['PASSWORD']
host = os.environ['HOSTNAME']
port = os.environ['DBPORT']
database = os.environ['DATABASE']
engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}")

def load_jobs():
    # Establish a connection
    with engine.connect() as connection:
        # Now you can execute SQL queries using this connection
        # For example:
        sql_query = "SELECT * FROM jobs"
        result = connection.execute(text(sql_query)) # text() helps execute raw sql queries
        
        #to work on the fetched sql entries, we should convert them to an array of dictionaries, where each dict = each row of the table 
        
        # Fetch all rows from the result
        rows = result.fetchall()
        # Get column names
        columns = result.keys()
        # Convert rows into dictionaries
        list_of_dicts = [dict(zip(columns, row)) for row in rows]
        return list_of_dicts
        
def get_job(id):
    print("inside the getJob func with id",id)
    with engine.connect() as connection:
        sql_query = f"SELECT * from jobs WHERE id = {id}"
        result = connection.execute(text(sql_query))
        rows = result.fetchall()
        if (len(rows)==0) : return None
        columns = result.keys()
        JOB = dict(zip(columns, rows[0]))
        return JOB

def store_application(job_id, application, pdfFile):
    with engine.connect() as conn:
        sql_query = text("INSERT INTO applications (job_id, full_name, email, experience, tell_us_more, filename, filepath) VALUES (:job_id, :full_name, :email, :experience, :tell_us_more, :filename, :filepath)")
        params = {
            'job_id': job_id,
            'full_name': application.get('name'),
            'email': application.get('email'),
            'experience': application.get('experience'),
            'tell_us_more': application.get('message'),
            'filename': pdfFile[0],
            'filepath': pdfFile[1]
        }
        conn.execute(sql_query, params)
        conn.commit()

def isDuplicateApplication(id, application):
    print("inside the isDuplicateApplication func with application",application)
    with engine.connect() as conn:
        sql_query = text("SELECT * FROM applications WHERE email = :email AND job_id = :job_id")
        params = {
            'email': application.get('email'),
            'job_id': id
        }
        result = conn.execute(sql_query, params)
        rows = result.fetchall()
        print("rows: ",rows)
        print(len(rows)>0)
        return len(rows) > 0
