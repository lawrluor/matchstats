from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
set = Table('set', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('winner_id', INTEGER),
    Column('loser_id', INTEGER),
    Column('winner_tag', VARCHAR(length=64)),
    Column('loser_tag', VARCHAR(length=64)),
    Column('winner_score', INTEGER),
    Column('loser_score', INTEGER),
    Column('max_match_count', INTEGER),
    Column('total_matches', INTEGER),
    Column('round_type', INTEGER),
    Column('tournament', INTEGER),
    Column('tournament_name', VARCHAR(length=128)),
)

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
    Column('round_type', Integer),
    Column('tournament_id', Integer),
    Column('tournament_name', String(length=128)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['set'].columns['tournament'].drop()
    post_meta.tables['set'].columns['tournament_id'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['set'].columns['tournament'].create()
    post_meta.tables['set'].columns['tournament_id'].drop()
