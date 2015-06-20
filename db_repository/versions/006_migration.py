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

Set = Table('Set', pre_meta,
    Column('winner_id', INTEGER, primary_key=True, nullable=False),
    Column('loser_id', INTEGER, primary_key=True, nullable=False),
    Column('result', VARCHAR(length=64)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['Match'].drop()
    pre_meta.tables['Set'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['Match'].create()
    pre_meta.tables['Set'].create()
