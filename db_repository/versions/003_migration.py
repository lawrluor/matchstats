from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
set = Table('set', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('body', VARCHAR(length=140)),
    Column('timestamp', DATETIME),
    Column('tourney', VARCHAR(length=64)),
    Column('round', VARCHAR(length=64)),
    Column('user_id', INTEGER),
)

sets = Table('sets', post_meta,
    Column('winner_id', Integer),
    Column('loser_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['set'].drop()
    post_meta.tables['sets'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['set'].create()
    post_meta.tables['sets'].drop()
