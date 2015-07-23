from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
tournament = Table('tournament', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('official_title', VARCHAR(length=128)),
    Column('host', VARCHAR(length=128)),
    Column('entrants', INTEGER),
    Column('bracket_type', VARCHAR(length=128)),
    Column('game_type', VARCHAR(length=128)),
    Column('date', DATE),
    Column('name', VARCHAR(length=128)),
    Column('tournament_type', VARCHAR(length=64)),
    Column('region', VARCHAR(length=64)),
)

tournament = Table('tournament', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('official_title', String(length=128)),
    Column('host', String(length=128)),
    Column('entrants', Integer),
    Column('bracket_type', String(length=128)),
    Column('game_type', String(length=128)),
    Column('date', Date),
    Column('name', String(length=128)),
    Column('tournament_type', String(length=64)),
    Column('region_name', String(length=64)),
)

user = Table('user', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('tag', VARCHAR(length=64)),
    Column('main', VARCHAR(length=64)),
    Column('region', VARCHAR(length=64)),
)

user = Table('user', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('tag', String(length=64)),
    Column('main', String(length=64)),
    Column('region_name', String(length=64)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['tournament'].columns['region'].drop()
    post_meta.tables['tournament'].columns['region_name'].create()
    pre_meta.tables['user'].columns['region'].drop()
    post_meta.tables['user'].columns['region_name'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['tournament'].columns['region'].create()
    post_meta.tables['tournament'].columns['region_name'].drop()
    pre_meta.tables['user'].columns['region'].create()
    post_meta.tables['user'].columns['region_name'].drop()
