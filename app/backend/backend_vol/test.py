import os, sys
import traci
import time
from sqlalchemy import create_engine



################## DB ##################

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
                "vts INTEGER" + "," + \
                "vtype TEXT" + "," + \
                "vlon FLOAT" + "," + \
                "vlat FLOAT" + \
                ");" )

def add_new_row(vts, vtype, vlon, vlat ):
    # Insert a new number into the 'numbers' table.
    cmd =   "INSERT INTO vehicles" + \
            "(vts, vtype, vlon, vlat) " + \
            "VALUES (" + \
            str(vts) + "," + \
            f"'{vtype}'" + "," + \
            str(vlon) + "," + \
            str(vlat) + \
            ");"
    print(cmd)
    db.execute(cmd)

create_table()

#################### SUMO ####################

if 'SUMO_HOME' in os.environ:
    sumo_tools_path = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sumo_binary_path = os.path.join(os.environ['SUMO_HOME'], 'bin/sumo')
    sumo_gui_binary_path = os.path.join(os.environ['SUMO_HOME'], 'bin/sumo-gui')
    sys.path.append(sumo_tools_path)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

sumoCmd = [sumo_binary_path, '-c', 'sumo-scenarios/Lachine/lachine.sumocfg']
print(sumoCmd)
traci.start(sumoCmd)
step = 0
while step < 1000:
    traci.simulationStep()
    vehicleIDS = traci.vehicle.getIDList()
    for vehicleID in vehicleIDS:
        x, y = traci.vehicle.getPosition(vehicleID)
        vlon, vlat = traci.simulation.convertGeo(x, y)
        vtype = traci.vehicle.getVehicleClass(vehicleID)
        print( vehicleID )
        print( x, y )
        print( vlon, vlat )
        print( traci.vehicle.getVehicleClass(vehicleID) )
        print( "---------------------------------" )
        add_new_row(step, vtype, vlon, vlat )
        # time.sleep(.2)
    print("--> ",step , "  ---   ", len(vehicleIDS))
    # break
    step += 1
    time.sleep(2)
    

traci.close()
