from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
set = Table('set', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('winner_id', Integer),
    Column('loser_id', Integer),
    Column('winner_tag', String(length=64)),
    Column('loser_tag', String(length=64)),
    Column('winner_score', Integer),
    Column('loser_score', Integer),
    Column('max_match_count', Integer),
    Column('total_matches', Integer),
    Column('tournament', String(length=64)),
    Column('round_type', Integer),
)

user = Table('user', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('tag', String(length=64)),
    Column('main', String(length=64)),
    Column('region', String(length=128)),
    Column('seed', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['set'].columns['round_type'].create()
    post_meta.tables['user'].columns['seed'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['set'].columns['round_type'].drop()
    post_meta.tables['user'].columns['seed'].drop()
