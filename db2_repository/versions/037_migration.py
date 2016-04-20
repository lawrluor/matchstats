from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
tournament_header = Table('tournament_header', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('official_title', VARCHAR(length=256)),
    Column('host', VARCHAR(length=128)),
    Column('url', VARCHAR(length=256)),
    Column('public_url', VARCHAR(length=256)),
    Column('entrants', INTEGER),
    Column('game_type', VARCHAR(length=128)),
    Column('date', DATE),
    Column('name', VARCHAR(length=256)),
    Column('tournament_type', VARCHAR(length=64)),
    Column('region_id', INTEGER),
)

tournament = Table('tournament', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('parent_id', INTEGER),
    Column('official_title', VARCHAR(length=256)),
    Column('host', VARCHAR(length=128)),
    Column('url', VARCHAR(length=256)),
    Column('public_url', VARCHAR(length=256)),
    Column('entrants', INTEGER),
    Column('bracket_type', VARCHAR(length=128)),
    Column('game_type', VARCHAR(length=128)),
    Column('date', DATE),
    Column('name', VARCHAR(length=256)),
    Column('tournament_type', VARCHAR(length=64)),
    Column('region_id', INTEGER),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['tournament_header'].columns['tournament_type'].drop()
    pre_meta.tables['tournament'].columns['tournament_type'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['tournament_header'].columns['tournament_type'].create()
    pre_meta.tables['tournament'].columns['tournament_type'].create()
