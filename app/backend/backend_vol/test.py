import os, sys
import traci


if 'SUMO_HOME' in os.environ:
    sumo_tools_path = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sumo_binary_path = os.path.join(os.environ['SUMO_HOME'], 'bin/sumo')
    sumo_gui_binary_path = os.path.join(os.environ['SUMO_HOME'], 'bin/sumo-gui')
    sys.path.append(sumo_tools_path)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

sumoCmd = [sumo_binary_path, '--remote-port 9999', '-c', 'example.sumocfg']
print(sumoCmd)
traci.start(sumoCmd)
step = 0
while step < 1000:
   traci.simulationStep()
   if traci.inductionloop.getLastStepVehicleNumber("0") > 0:
       traci.trafficlight.setRedYellowGreenState("0", "GrGr")
   step += 1

traci.close()