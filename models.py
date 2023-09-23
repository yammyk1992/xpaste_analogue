from datetime import datetime
from sqlalchemy import MetaData, String, Integer, Column, Table, TIMESTAMP
import services

metadata = MetaData()

text = Table(
    'text_table',
    metadata,
    Column('id', Integer, default=None, primary_key=True, autoincrement=True),
    Column('text', String, nullable=False),
    Column('salt', String, default=services.get_salt),
    Column('created_at', TIMESTAMP, default=datetime.utcnow)
)
