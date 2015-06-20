from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
match = Table('match', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('set_id', Integer),
    Column('stage', String(length=64)),
    Column('winner', String(length=64)),
    Column('loser', String(length=64)),
    Column('winner_char', String(length=64)),
    Column('loser_char', String(length=64)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['match'].columns['loser_char'].create()
    post_meta.tables['match'].columns['winner_char'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['match'].columns['loser_char'].drop()
    post_meta.tables['match'].columns['winner_char'].drop()
