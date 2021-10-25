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
import glob
import pprint

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


################## Grab  Data ##################


################## Parse  Data ##################
print("################## Parse  Data ##################")
bbox_Montreal = (-73.290386, 45.828865, -74.229416, 45.333622)
xmax, ymax, xmin, ymin = bbox_Montreal
fpath = [
#  './blobs/powe_r_ring.geojson',
 './blobs/power_items.geojson',
 './blobs/power_substations_canvec1.geojson',
 './blobs/power_substations_canvec2.geojson',
 './blobs/powerlines_canvec.geojson']

pprint.pprint(fpath)
geodataframes = [gpd.read_file(f) for f in fpath]
print([el.shape for el in geodataframes])
geodataframe = pd.concat(geodataframes)
print(geodataframe.shape)

################## Store  Data ##################
print("################## Convert to WKT  Data ##################")
geodataframe['geom'] = geodataframe['geometry'].apply(
    lambda x: WKTElement(x.wkt, srid=SRID))

# drop the geometry column as it is now duplicative
geodataframe.drop('geometry', 1, inplace=True)

# For the geom column, we will use GeoAlchemy's type 'Geometry'
print("################## Writing to SQL  Data ##################")
geodataframe.to_sql(name='power_grid',
                    con= engine,
                    if_exists='replace',
                    index=True,
                    chunksize=100,
                    dtype={
                        'geom': Geometry('Geometry', srid=SRID),
                        }
                    )
