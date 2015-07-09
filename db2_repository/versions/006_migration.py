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
    Column('tournament', VARCHAR(length=128)),
    Column('round_type', INTEGER),
    Column('tournament_relation', INTEGER),
)

tournament = Table('tournament', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('title', VARCHAR(length=128)),
    Column('host', VARCHAR(length=128)),
    Column('entrants', INTEGER),
    Column('bracket_type', VARCHAR(length=128)),
    Column('game_type', VARCHAR(length=128)),
    Column('date', VARCHAR(length=128)),
)

tournament = Table('tournament', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('official_title', String(length=128)),
    Column('host', String(length=128)),
    Column('entrants', Integer),
    Column('bracket_type', String(length=128)),
    Column('game_type', String(length=128)),
    Column('date', String(length=128)),
    Column('name', String(length=128)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['set'].columns['tournament'].drop()
    pre_meta.tables['tournament'].columns['title'].drop()
    post_meta.tables['tournament'].columns['name'].create()
    post_meta.tables['tournament'].columns['official_title'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['set'].columns['tournament'].create()
    pre_meta.tables['tournament'].columns['title'].create()
    post_meta.tables['tournament'].columns['name'].drop()
    post_meta.tables['tournament'].columns['official_title'].drop()
