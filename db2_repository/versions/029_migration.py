from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
sub_tournament = Table('sub_tournament', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('official_title', VARCHAR(length=128)),
    Column('host', VARCHAR(length=128)),
    Column('url', VARCHAR(length=256)),
    Column('public_url', VARCHAR(length=256)),
    Column('entrants', INTEGER),
    Column('bracket_type', VARCHAR(length=128)),
    Column('date', DATE),
    Column('name', VARCHAR(length=256)),
    Column('tournament_type', VARCHAR(length=64)),
    Column('parent_tournament', INTEGER),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['sub_tournament'].columns['parent_tournament'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['sub_tournament'].columns['parent_tournament'].create()
