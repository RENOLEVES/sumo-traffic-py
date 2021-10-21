import geopandas as gpd
import json
from sqlalchemy.orm import sessionmaker
from geoalchemy2 import Geometry, WKTElement
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
import os
from sqlalchemy import create_engine, inspect
import random

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
fpath = "blobs/building_footprint_ms.geojson"
geodataframe = gpd.read_file(fpath, bbox=bbox_Montreal)
print(geodataframe.head())
print(geodataframe.size)

################## Store Footprint Data ##################
print("################## Convert to WKT Footprint Data ##################")
geodataframe['geom'] = geodataframe['geometry'].apply(
    lambda x: WKTElement(x.wkt, srid=SRID))

# drop the geometry column as it is now duplicative
geodataframe.drop('geometry', 1, inplace=True)

print("################## Add Random Height Footprint Data ##################")
# add random height column
geodataframe['height'] = [3 + 10*random.gammavariate(3,1) for e in range(len(geodataframe))]

# For the geom column, we will use GeoAlchemy's type 'Geometry'
print("################## Writing to SQL Footprint Data ##################")
geodataframe.to_sql(name='building_footprint_ms', 
                    con= engine, 
                    if_exists='replace', 
                    index=True,
                    chunksize=1000,
                    dtype={
                        'height' : Float,
                        'geom': Geometry('POLYGON', srid=SRID),
                        })
