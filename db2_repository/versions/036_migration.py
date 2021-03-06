from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
tournament_header = Table('tournament_header', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('official_title', String(length=256)),
    Column('host', String(length=128)),
    Column('url', String(length=256)),
    Column('public_url', String(length=256)),
    Column('entrants', Integer),
    Column('game_type', String(length=128)),
    Column('date', Date),
    Column('name', String(length=256)),
    Column('tournament_type', String(length=64)),
    Column('region_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['tournament_header'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['tournament_header'].drop()
