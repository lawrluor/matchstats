from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
Match = Table('Match', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('set_id', INTEGER),
    Column('stage', VARCHAR(length=64)),
)

User = Table('User', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('tag', VARCHAR(length=64)),
    Column('main', VARCHAR(length=64)),
)

match = Table('match', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('set_id', Integer),
    Column('stage', String(length=64)),
)

user = Table('user', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('tag', String(length=64)),
    Column('main', String(length=64)),
)

set = Table('set', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('winner_id', Integer),
    Column('loser_id', Integer),
    Column('winner_tag', String(length=64)),
    Column('loser_tag', String(length=64)),
    Column('result', String(length=64)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['Match'].drop()
    pre_meta.tables['User'].drop()
    post_meta.tables['match'].create()
    post_meta.tables['user'].create()
    post_meta.tables['set'].columns['loser_tag'].create()
    post_meta.tables['set'].columns['winner_tag'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['Match'].create()
    pre_meta.tables['User'].create()
    post_meta.tables['match'].drop()
    post_meta.tables['user'].drop()
    post_meta.tables['set'].columns['loser_tag'].drop()
    post_meta.tables['set'].columns['winner_tag'].drop()
