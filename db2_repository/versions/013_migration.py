from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
plactrue = Table('plactrue', pre_meta,
    Column('tournament_id', INTEGER, primary_key=True, nullable=False),
    Column('user_id', INTEGER, primary_key=True, nullable=False),
    Column('placement', INTEGER),
    Column('tournament_name', VARCHAR(length=128)),
    Column('seed', INTEGER),
)

placement = Table('placement', post_meta,
    Column('tournament_id', Integer, primary_key=True, nullable=False),
    Column('user_id', Integer, primary_key=True, nullable=False),
    Column('placement', Integer),
    Column('tournament_name', String(length=128)),
    Column('seed', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['plactrue'].drop()
    post_meta.tables['placement'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['plactrue'].create()
    post_meta.tables['placement'].drop()
