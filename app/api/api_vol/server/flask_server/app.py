import json
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

def get_timestamp_all(vts):
    # Retrieve the last number inserted inside the 'numbers'
    query = "" + \
            "SELECT * " + \
            "FROM agents " + \
            f"WHERE vts = {vts} " + \
            "ORDER BY " + "vid" + " ASC"
    result_set = db.execute(query).mappings().all()
    return [dict(res) for res in result_set] if isinstance(result_set, list) else dict(result_set)
    

# from pprint import pprint
# last = get_timestamp_all(vts=10)
# pprint(json.dumps(last))



from flask import Flask, render_template
from flask_socketio import SocketIO, emit
    
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins='*')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home/')
def home():
    return "Home page"

@socketio.on('my event')
def test_message(message):
    emit('my response', {'data1': message})

@socketio.on('floating info event')
def test_message(message):
    print(message)
    last = get_timestamp_all(vts=message)
    emit('floating info response', last)

@socketio.on('connect')
def test_connect(sid):
    print(50*'0')
    # socketio.start_background_task(task, sid)
    # for i in range(1000):
    #     emit('my response', js_obj)
    #     socketio.sleep(1)
    print('Client CONNECTED')
    print(50*'1')

@socketio.on('disconnect')
def test_disconnect():
    print(50*'2')
    print('Client DISCONNECTED')
    print(50*'3')

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=8000)