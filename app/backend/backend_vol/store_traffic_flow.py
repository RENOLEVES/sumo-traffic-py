
import traci
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import declarative_base
import os
import sys
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
db_string = 'postgresql://{}:{}@{}:{}/{}'.format(
    db_user, db_pass, db_host, db_port, db_name)
db = create_engine(db_string)


Base = declarative_base()


class Agent(Base):
    __tablename__ = 'agents'
    id = Column(Integer, primary_key=True)
    vname = Column(String)
    vts = Column(Integer)
    vtype = Column(String)
    vlon = Column(Float)
    vlat = Column(Float)
    vemis_co2 = Column(Float)
    vemis_co = Column(Float)
    vemis_hc = Column(Float)
    vemis_nox = Column(Float)
    vemis_pm25 = Column(Float)
    vemis_noise = Column(Float)
    vfuel = Column(Float)

    def __repr__(self):
        return "<User(id='%s', vname='%s', vts='%s', vtype='%s', vlon='%s', vlat='%s')>" % (
            self.id, self.vname, self.vts, self.vtype, self.vlon, self.vlat)


Base.metadata.create_all(db)

Session = sessionmaker(bind=db)
session = Session()


#################### SUMO ####################

if 'SUMO_HOME' in os.environ:
    sumo_tools_path = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sumo_binary_path = os.path.join(os.environ['SUMO_HOME'], 'bin/sumo')
    sumo_gui_binary_path = os.path.join(
        os.environ['SUMO_HOME'], 'bin/sumo-gui')
    sys.path.append(sumo_tools_path)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

# import traci
# import libsumo

sumoCmd = [sumo_binary_path, '-c', 'sumo-scenarios/Montreal/montreal.sumocfg']
print(sumoCmd)
traci.start(sumoCmd)
step = 0
nr_steps_per_run = 5
tt = time.time()
while step < 5000:
    [traci.simulationStep() for el in range(nr_steps_per_run)]
    # traci.simulationStep()
    # step += nr_steps_per_run
    if step % 60 == 0:
        print(round(time.time()-tt, 1), " seconds")
        tt = time.time()
    # print("--> ", step, "  ---   ", round(t0-tt, 1), " seconds")
    # continue
    vehicleIDS = traci.vehicle.getIDList()
    for vehicleID in vehicleIDS:
        x, y = traci.vehicle.getPosition(vehicleID)
        vlon, vlat = traci.simulation.convertGeo(x, y)
        vtype = traci.vehicle.getVehicleClass(vehicleID)
        emiss_co2 = round(traci.vehicle.getCO2Emission(vehicleID), 3)
        emiss_co = round(traci.vehicle.getCOEmission(vehicleID), 3)
        emiss_hc = round(traci.vehicle.getHCEmission(vehicleID), 3)
        emiss_nox = round(traci.vehicle.getNOxEmission(vehicleID), 3)
        emiss_pm25 = round(traci.vehicle.getPMxEmission(vehicleID), 3)
        emiss_noise = round(traci.vehicle.getNoiseEmission(vehicleID), 3)
        fuel = round(traci.vehicle.getFuelConsumption(vehicleID), 3)

        # print( vehicleID )
        # print( x, y )
        # print( vlon, vlat )
        # print( emiss_class )
        # print( "---------------------------------" )

        session.add(Agent(vname=vehicleID,
                          vts=step,
                          vtype=vtype,
                          vlon=vlon,
                          vlat=vlat,
                          vemis_co2=emiss_co2,
                          vemis_co=emiss_co,
                          vemis_hc=emiss_hc,
                          vemis_nox=emiss_nox,
                          vemis_pm25=emiss_pm25,
                          vemis_noise=emiss_noise,
                          vfuel=fuel,
                          ))
    session.commit()
    # break
    print("--> ", step, "  ---   ", len(vehicleIDS))
    # print("--> ", step, "  ---   ")
    # break
    step += nr_steps_per_run
    # time.sleep(.002)


traci.close()
