import os
import time
import random
from sqlalchemy import create_engine

db_name = 'postgres'
db_user = os.environ['POSTGRES_USER']
db_pass = os.environ['POSTGRES_PASSWORD']
db_host = os.environ['POSTGRES_HOST']
db_port = os.environ['POSTGRES_PORT']

# Connect to the database
db_string = 'postgresql://{}:{}@{}:{}/{}'.format(db_user, db_pass, db_host, db_port, db_name)
db = create_engine(db_string)

def create_table():
    db.execute( "CREATE TABLE IF NOT EXISTS vehicles (" + \
                "timestamp INTEGER," + \
                "type TEXT," + \
                "latitude FLOAT" + \
                "longitude FLOAT" + \
                ");" )

def add_new_row(n):
    # Insert a new number into the 'numbers' table.
    db.execute("INSERT INTO numbers (number, timestamp) " + \
        "VALUES (" + \
        str(n) + "," + \
        str(int(round(time.time() * 1000))) + ");")

def get_last_row():
    # Retrieve the last number inserted inside the 'numbers'
    query = "" + \
            "SELECT * " + \
            "FROM vehicles " + \
            "WHERE timestamp >= (SELECT max(timestamp) FROM numbers)" +\
            "LIMIT 1"
    result_set = db.execute(query)  
    for (r) in result_set:  
        return r[0]

if __name__ == '__main__':
    print('Application started')
    create_table()
    print('Table Created')

    while True:
        add_new_row(random.randint(1,100000))
        print('The last value inserted is: {}'.format(get_last_row()))
        time.sleep(.5)
