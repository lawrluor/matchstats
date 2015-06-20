from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
Set = Table('Set', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('winner_id', INTEGER),
    Column('loser_id', INTEGER),
    Column('result', VARCHAR(length=64)),
)

set = Table('set', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('winner_id', Integer),
    Column('loser_id', Integer),
    Column('result', String(length=64)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['Set'].drop()
    post_meta.tables['set'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['Set'].create()
    post_meta.tables['set'].drop()
