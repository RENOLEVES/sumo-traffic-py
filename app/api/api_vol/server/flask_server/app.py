from flask_socketio import SocketIO, emit
from flask import Flask, render_template
from db_connection import DBConn
from db_query import AgentQuery

# create a database connection instance
Conn = DBConn()
# create a Session instance
session = Conn.get_db_session()
# get table data model
Agents = Conn.get_db_table("agents")

# create a db query instance
agentQuery = AgentQuery(session=session, model=Agents)
# res = agentQuery.query_emission_time_range(time_value=10, buffer_length=115, emission_ids=['vts', 'vlon','vname'])
# from pprint import pprint
# pprint(res)
# for el in res:
#     pprint(el)
    # pprint(el.vts)


# pprint(dir(Agents.classes))

def get_emis(message):
    print(f"message: {message}")
    emis_name = message.name
    vname = message['vname']
    vts = message['vts']
    query = "" + \
            f"SELECT vemis_{emis_name} " + \
        "FROM agents " + \
            f"WHERE vname = '{vname}' " + \
            f"AND vts <= {vts} " + \
        "ORDER BY " + "vname" + " ASC"
    print(query)
    result_set = db.execute(query).mappings().all()
    return [res.vemis_co2 for res in result_set] if isinstance(result_set, list) else dict(result_set)


# from pprint import pprint
# last = get_emis_co2("veh2", vts=10000)
# print(last)


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins='*')

FLOATING_FIELDS = {'lon': 'vlon', 'lat': 'vlat', 'name': 'vname'}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/home/')
def home():
    return "Home page"


@socketio.on('float_req')
def handle_ts(value):
    time_value, buffer_length, emission_ids = value
    last = agentQuery.query_emission_time_range(time_value=time_value, buffer_length=buffer_length, emission_ids=emission_ids)
    emit('float_res', last)


@socketio.on('emis_req')
def handle_emis(value):
    time_value, buffer_length, emission_ids = value
    last = agentQuery.query_emission_time_range(time_value=time_value, buffer_length=buffer_length, emission_ids=emission_ids)
    emit('emis_res', last)


@socketio.on('connect')
def test_connect(sid):
    print(50*'0')
    print('Client CONNECTED')
    print(50*'1')
    emit('connect', 'SOCKET CONNECTED')


@socketio.on('disconnect')
def test_disconnect():
    print(50*'2')
    print('Client DISCONNECTED')
    print(50*'3')
    emit('disconnect', 'SOCKET DISCONNECTED')


if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=8000)
