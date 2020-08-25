import os

from sqlalchemy import (Column, Integer, MetaData, String, Table,
                        create_engine, ARRAY)

from databases import Database
from app.config import SQLALCHEMY_DATABASE_URI
DATABASE_URI = SQLALCHEMY_DATABASE_URI#os.getenv('DATABASE_URI')

engine = create_engine(DATABASE_URI)
metadata = MetaData()

emails = Table(
    'emails',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('sender', String(50)),
    Column('recipient', ARRAY(String)),
    Column('content',String(1000)),
    Column('status',String(20))
)

database = Database(DATABASE_URI)