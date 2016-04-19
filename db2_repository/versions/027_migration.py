from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
sub_tournament = Table('sub_tournament', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('official_title', String(length=128)),
    Column('host', String(length=128)),
    Column('url', String(length=256)),
    Column('public_url', String(length=256)),
    Column('entrants', Integer),
    Column('bracket_type', String(length=128)),
    Column('date', Date),
    Column('name', String(length=256)),
    Column('tournament_type', String(length=64)),
    Column('parent_tournament', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['sub_tournament'].columns['parent_tournament'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['sub_tournament'].columns['parent_tournament'].drop()
