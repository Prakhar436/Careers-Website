# IMPORT THE SQALCHEMY LIBRARY's CREATE_ENGINE METHOD
from sqlalchemy import create_engine, text
import os
# DEFINE THE DATABASE CREDENTIALS
user = os.environ['USERNAME']
password = os.environ['PASSWORD']
host = os.environ['HOSTNAME']
port = os.environ['PORT']
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

