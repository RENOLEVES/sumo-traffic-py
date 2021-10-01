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
res = agentQuery.query_floating_time_range(value=10, bufferLength=115)
print( res )





# def get_timestamp_all(vts):
#     # result = session.execute(select(Agents).where(Agents.vts == vts))
#     # # print( "result:   ", result.scalars() )
#     # for agent_obj in result.scalars():
#     #     print(f"{agent_obj.vname} {agent_obj.vts}")
#     records = session.query(Agents).filter(Agents).first()
#         # .(vname == 'veh0')
#         # .all()
        
        
#     for record in records:
#         print("----------------")
#         print(record)
        
#     # vts = message
#     # # Retrieve the last number inserted inside the 'numbers'
#     # query = "" + \
#     #         "SELECT vname, vts " + \
#     #         "FROM agents " + \
#     #         f"WHERE vts = {vts} " + \
#     #         "ORDER BY " + "vname" + " ASC"
#     # result_set = db.execute(query).mappings().all()
#     # print([res for res in result_set])

#     # return [dict(res) for res in result_set] if isinstance(result_set, list) else dict(result_set)
    

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

# @socketio.on('my event')
# def test_message(message):
#     emit('my response', {'data1': message})

@socketio.on('float_req')
def handle_ts(value):
    value, bufferLength = value
    last = agentQuery.query_floating_time_range(value=value, bufferLength=bufferLength)
    emit('float_res', last)

@socketio.on('emis_req')
def handle_emis(message):
    last = get_emis(message)
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