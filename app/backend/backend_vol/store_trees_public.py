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


################## Grab Data ##################


################## Parse Data ##################
print("################## Parse  Data ##################")
bbox_Montreal = (-73.290386, 45.828865, -74.229416, 45.333622)
xmax, ymax, xmin, ymin = bbox_Montreal
fpath = "blobs/arbres-publics.csv"
geodataframe = gpd.read_file(fpath)
geodataframe = geodataframe[geodataframe['Longitude']!=""]
geodataframe = geodataframe[geodataframe['Latitude']!=""]
geodataframe.drop('geometry', axis=1, inplace=True)
gdf = gpd.GeoDataFrame(
    geodataframe, geometry=gpd.points_from_xy(geodataframe['Longitude'], geodataframe['Latitude']))
# geodataframe.drop('Longitude', axis=1, inplace=True)
# geodataframe.drop('Latitude', axis=1, inplace=True)
geodataframe.drop('Coord_X', axis=1, inplace=True)
geodataframe.drop('Coord_Y', axis=1, inplace=True)

################## Store Data ##################
print("################## Convert to WKT  Data ##################")
geodataframe['geom'] = geodataframe['geometry'].apply(
    lambda x: WKTElement(x.wkt, srid=SRID))

# drop the geometry column as it is now duplicative
geodataframe.drop('geometry', axis=1, inplace=True)

# For the geom column, we will use GeoAlchemy's type 'Geometry'
print("################## Writing to SQL  Data ##################")
geodataframe.to_sql(name='trees_public',
                    con= engine,
                    if_exists='replace',
                    index=True,
                    chunksize=100,
                    dtype={
                        'geom': Geometry('Geometry', srid=SRID),
                        }
                    )
