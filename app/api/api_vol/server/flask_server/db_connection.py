import os
from sqlalchemy.engine import reflection
from sqlalchemy import create_engine, select
from sqlalchemy import select
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker


class DBConn():
    def __init__(self, automap=True, Base=None):
        # Get database config values
        self.configs = self.get_db_configs
        # Connect to the database
        self.engine = self.init_db_engine(self.configs)

        if automap:
            Base = automap_base()
            Base.prepare(self.engine, reflect=True)
            self.Base = Base
        elif Base:
            self.Base = Base
        else:
            raise ValueError

    @property
    def get_db_configs(self):
        return {
            'db_name': 'postgres',
            'db_user': os.environ['POSTGRES_USER'],
            'db_pass': os.environ['POSTGRES_PASSWORD'],
            'db_host': os.environ['POSTGRES_HOST'],
            'db_port': os.environ['POSTGRES_PORT'],
        }

    @get_db_configs.setter
    def set_db_configs(self, configs):
        self.configs = configs

    def init_db_engine(self, configs):
        db_string = 'postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}'.format(
            **configs)
        return create_engine(db_string, echo=False)
        
    @property
    def get_db_session(self):
        return sessionmaker(bind=self.engine)

    def get_db_table(self, name):
        return self.Base.classes[name]


