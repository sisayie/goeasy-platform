# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 13:36:38 2019

@author: chala
"""

import os

user = os.environ['POSTGRES_USER']
password = os.environ['POSTGRES_PASSWORD']
host = os.environ['POSTGRES_HOST']
database = os.environ['POSTGRES_DB']
port = os.environ['POSTGRES_PORT']

DATABASE_CONNECTION_URL = f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}'