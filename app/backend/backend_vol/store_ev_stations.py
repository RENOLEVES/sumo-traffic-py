import geopandas as gpd
import pandas as pd
import json
from sqlalchemy.orm import sessionmaker
from geoalchemy2 import Geometry, WKTElement
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
import os
from sqlalchemy import create_engine, inspect
import random
from shapely.geometry import Polygon

################## DB ##################

db_name = 'postgres'
db_user = os.environ['POSTGRES_USER']
db_pass = os.environ['POSTGRES_PASSWORD']
db_host = os.environ['POSTGRES_HOST']
db_port = os.environ['POSTGRES_PORT']

# Connect to the database
db_string = 'postgresql://{}:{}@{}:{}/{}'.format(
    db_user, db_pass, db_host, db_port, db_name)
engine = create_engine(db_string, echo=False)
engine.execute('CREATE EXTENSION IF NOT EXISTS postgis')
SRID = 4326


################## Grab Footprint Data ##################


################## Parse Footprint Data ##################
print("################## Parse Footprint Data ##################")
bbox_Montreal = (-73.290386, 45.828865, -74.229416, 45.333622)
xmax, ymax, xmin, ymin = bbox_Montreal
fpath = "blobs/ev_stations.json"
with open(fpath, 'r') as f:
    jsonContent = json.load(f)
columns = jsonContent[0].keys()
parsed_data = [ {"type": "Feature", "properties": el,"geometry": {"type": "Point", "coordinates":[el['Long'], el['Lat']]}} for el in jsonContent]
geodataframe = gpd.GeoDataFrame.from_features(parsed_data)
geodataframe = geodataframe.drop(columns=['Lat'])
geodataframe = geodataframe.drop(columns=['Long'])
print(geodataframe.head())
print(geodataframe.shape)
print(geodataframe.columns)


################## Store Footprint Data ##################
print("################## Convert to WKT Footprint Data ##################")
geodataframe['geom'] = geodataframe['geometry'].apply(
    lambda x: WKTElement(x.wkt, srid=SRID))

# drop the geometry column as it is now duplicative
geodataframe.drop('geometry', 1, inplace=True)

# For the geom column, we will use GeoAlchemy's type 'Geometry'
print("################## Writing to SQL Footprint Data ##################")
geodataframe.to_sql(name='ev_stations',
                    con= engine,
                    if_exists='replace',
                    index=True,
                    chunksize=100,
                    dtype={
                        'geom': Geometry('POINT', srid=SRID),
                        })
