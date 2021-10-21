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
fpath = "gas_stations.json"
with open(fpath, 'r') as f:
    jsonContent = json.load(f)
df = pd.DataFrame(
    {'id': [e['id'] for e in jsonContent],
     'name': [e['name'] for e in jsonContent],
     'latitude': [e['geo']['latitude'] for e in jsonContent],
     'longitude': [e['geo']['longitude'] for e in jsonContent]})
geodataframe = gpd.GeoDataFrame(
    df, geometry=gpd.points_from_xy(df.longitude, df.latitude))
# geodataframe = gpd.read_file(fpath, bbox=bbox_Montreal)
geodataframe = geodataframe.drop(columns=['latitude'])
geodataframe = geodataframe.drop(columns=['longitude'])
geodataframe = geodataframe.drop(columns=['id'])
# geodataframe = geodataframe.cx[xmin:xmax, ymin:ymax]
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
geodataframe.to_sql(name='gas_stations',
                    con= engine,
                    if_exists='replace',
                    index=True,
                    chunksize=100,
                    dtype={
                        'name' : String,
                        'geom': Geometry('POINT', srid=SRID),
                        })
