from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
tournament = Table('tournament', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('official_title', VARCHAR(length=128)),
    Column('host', VARCHAR(length=128)),
    Column('url', VARCHAR(length=128)),
    Column('entrants', INTEGER),
    Column('bracket_type', VARCHAR(length=128)),
    Column('game_type', VARCHAR(length=128)),
    Column('date', DATE),
    Column('name', VARCHAR(length=128)),
    Column('tournament_type', VARCHAR(length=64)),
    Column('region_id', INTEGER),
    Column('dev_url', VARCHAR(length=256)),
)

tournament = Table('tournament', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('official_title', String(length=128)),
    Column('host', String(length=128)),
    Column('url', String(length=128)),
    Column('public_url', String(length=256)),
    Column('entrants', Integer),
    Column('bracket_type', String(length=128)),
    Column('game_type', String(length=128)),
    Column('date', Date),
    Column('name', String(length=128)),
    Column('tournament_type', String(length=64)),
    Column('region_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['tournament'].columns['dev_url'].drop()
    post_meta.tables['tournament'].columns['public_url'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['tournament'].columns['dev_url'].create()
    post_meta.tables['tournament'].columns['public_url'].drop()
