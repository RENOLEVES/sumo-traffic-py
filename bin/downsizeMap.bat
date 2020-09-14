@ECHO OFF

set /p boundries="Enter the path of the boundries file: >"
set /p largeOSM="Enter the path of the large OSM file containg the boundry: >"
set /p outputFile="Enter the path of the SUMO net file: >"
for %%f in (%~dp0.) do set ParentDirectory=%%~dpf
set sumoplustools=%ParentDirectory%sumoplustools\

@ECHO ON

python %sumoplustools%ConvertMaps\createPoly.py -g %boundries% -p poly-file.poly
osmconvert %largeOSM% -B=poly-file.poly -o=osm-file.osm
python %sumoplustools%ConvertMaps\addOSM.py -osm osm-file.osm
netconvert --osm-files osm-file.osm -o %outputFile% --output.street-names=True --output.original-names=True