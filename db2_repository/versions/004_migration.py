from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
tournament = Table('tournament', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('title', String(length=128)),
    Column('host', String(length=128)),
    Column('entrants', Integer),
    Column('bracket_type', String(length=128)),
    Column('game_type', String(length=128)),
    Column('date', String(length=128)),
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
    Column('tournament', String(length=128)),
    Column('round_type', Integer),
    Column('tournament_relation', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['tournament'].create()
    post_meta.tables['set'].columns['tournament_relation'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['tournament'].drop()
    post_meta.tables['set'].columns['tournament_relation'].drop()
