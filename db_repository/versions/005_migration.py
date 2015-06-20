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
    Column('winner_id', INTEGER),
    Column('loser_id', INTEGER),
    Column('result', VARCHAR(length=64)),
)

sets = Table('sets', pre_meta,
    Column('winner_id', INTEGER),
    Column('loser_id', INTEGER),
)

user = Table('user', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('tag', VARCHAR(length=64)),
    Column('main', VARCHAR(length=64)),
    Column('wins', INTEGER),
    Column('losses', INTEGER),
)

Match = Table('Match', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('set_id', Integer),
    Column('stage', String(length=64)),
)

Set = Table('Set', post_meta,
    Column('winner_id', Integer, primary_key=True, nullable=False),
    Column('loser_id', Integer, primary_key=True, nullable=False),
    Column('result', String(length=64)),
)

User = Table('User', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('tag', String(length=64)),
    Column('main', String(length=64)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['set'].drop()
    pre_meta.tables['sets'].drop()
    pre_meta.tables['user'].drop()
    post_meta.tables['Match'].create()
    post_meta.tables['Set'].create()
    post_meta.tables['User'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['set'].create()
    pre_meta.tables['sets'].create()
    pre_meta.tables['user'].create()
    post_meta.tables['Match'].drop()
    post_meta.tables['Set'].drop()
    post_meta.tables['User'].drop()
