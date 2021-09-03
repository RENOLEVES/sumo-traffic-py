
import os, sys
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


################## DB ##################

db_name = 'postgres'
db_user = os.environ['POSTGRES_USER']
db_pass = os.environ['POSTGRES_PASSWORD']
db_host = os.environ['POSTGRES_HOST']
db_port = os.environ['POSTGRES_PORT']

# Connect to the database
db_string = 'postgresql://{}:{}@{}:{}/{}'.format(db_user, db_pass, db_host, db_port, db_name)
db = create_engine(db_string)


from sqlalchemy.orm import declarative_base
Base = declarative_base()
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker


class Agent(Base):
    __tablename__ = 'agents'
    vid = Column(String, primary_key=True)
    vts = Column(Integer, primary_key=True)
    vtype = Column(String)
    vlon = Column(Float)
    vlat = Column(Float)
    vemis_co2 = Column(Float)
    def __repr__(self):
        return "<User(vid='%s', vts='%s', vtype='%s', vlon='%s', vlat='%s')>" % (
         self.vid, self.vts, self.vtype, self.vlon, self.vlat)

Base.metadata.create_all(db)

Session = sessionmaker(bind=db)
session = Session()


#################### SUMO ####################

if 'SUMO_HOME' in os.environ:
    sumo_tools_path = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sumo_binary_path = os.path.join(os.environ['SUMO_HOME'], 'bin/sumo')
    sumo_gui_binary_path = os.path.join(os.environ['SUMO_HOME'], 'bin/sumo-gui')
    sys.path.append(sumo_tools_path)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

# import traci
# import libsumo
import libsumo as traci

sumoCmd = [sumo_binary_path, '-c', 'sumo-scenarios/Montreal/montreal.sumocfg']
print(sumoCmd)
traci.start(sumoCmd)
step = 0
nr_steps_per_run = 5
while step < 5000:
    [traci.simulationStep() for el in range(nr_steps_per_run)]
    vehicleIDS = traci.vehicle.getIDList()
    for vehicleID in vehicleIDS:
        x, y = traci.vehicle.getPosition(vehicleID)
        vlon, vlat = traci.simulation.convertGeo(x, y)
        vtype = traci.vehicle.getVehicleClass(vehicleID)
        emiss_co2 = round(traci.vehicle.getCO2Emission(vehicleID)/1000, 2)

        # print( vehicleID )
        # print( x, y )
        # print( vlon, vlat )
        # print( emiss_class )
        # print( "---------------------------------" )

        session.add( Agent( vid=vehicleID,
                            vts=step, 
                            vtype= vtype,
                            vlon= vlon,
                            vlat= vlat,
                            vemis_co2=emiss_co2,
                             ) )
        # time.sleep(2)
    session.commit()
    # break
    print("--> ",step , "  ---   ", len(vehicleIDS))
    # break
    step += nr_steps_per_run
    # time.sleep(.002)
    

traci.close()
