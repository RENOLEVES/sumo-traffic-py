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
fpath = "blobs/building-lots-mtl-ca.geojson"
# fpath = "footprints.geojson"
geodataframe = gpd.read_file(fpath, bbox=bbox_Montreal)
# geodataframe.to_file("footprints.geojson", driver="GeoJSON")
print(geodataframe.head())
print(geodataframe.size)

# explodes multipolygons to multiple polygon rows
mask = geodataframe.geom_type=='Polygon'
mask_not = geodataframe.geom_type!='Polygon'
geodataframe = geodataframe.loc[mask].append(geodataframe.loc[mask_not].explode(), ignore_index=True)
geodataframe.reset_index(drop=True, inplace=True)

################## Store Footprint Data ##################
print("################## Convert to WKT Footprint Data ##################")
geodataframe['geom'] = geodataframe['geometry'].apply(
    lambda x: WKTElement(x.wkt, srid=SRID))

# drop the geometry column as it is now duplicative
geodataframe.drop('geometry', 1, inplace=True)

# convert height info to integer for data size reduction
geodataframe = geodataframe.fillna(0)
# geodataframe.height_mean = geodataframe.height_mean.astype(int)
# geodataframe.height_max = geodataframe.height_max.astype(int)
# geodataframe.height_stdev = geodataframe.height_stdev.astype(int)
# geodataframe.maximale = geodataframe.maximale.astype(int)

# # remove other columns and keep only one
# geodataframe['height'] = geodataframe.height_max
# geodataframe['height_max_allowed'] = geodataframe.maximale
# geodataframe.drop('height_mean', 1, inplace=True)
# geodataframe.drop('height_stdev', 1, inplace=True)
# geodataframe.drop('height_max', 1, inplace=True)
# geodataframe.drop('maximale', 1, inplace=True)

print(geodataframe.head())
print(geodataframe.shape)

# For the geom column, we will use GeoAlchemy's type 'Geometry'
print("################## Writing to SQL Footprint Data ##################")
geodataframe.to_sql(name='building_lots', 
                    con= engine, 
                    if_exists='replace', 
                    index=True,
                    chunksize=1000,
                    dtype={
                        'uid':                 Integer,
                        'building_number':     Integer,
                        'street_number':       Integer,
                        'street_name':         String,
                        'unit_number':         String,
                        'municipality_code':   Integer,
                        'max_floors':         Integer,
                        'dwelling_number':    Integer,
                        'year_built':           Integer,
                        'landuse_code':        Integer,
                        'firstletter_apt':     String,
                        'lastletter_apt':      String,
                        'landuse_text':        String,
                        'unit_category':       String,
                        'nad83_registration':  String,
                        'land_area':          Integer,
                        'built_area':         Integer,
                        'borough_code':        String,
                        'geom': Geometry('POLYGON', srid=SRID),
                        })
