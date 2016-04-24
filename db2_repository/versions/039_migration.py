from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
secondaries = Table('secondaries', pre_meta,
    Column('user_id', INTEGER),
    Column('character_id', INTEGER),
)

characters = Table('characters', post_meta,
    Column('user_id', Integer),
    Column('character_id', Integer),
)

user = Table('user', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('tag', VARCHAR(length=128)),
    Column('main', VARCHAR(length=64)),
    Column('region_id', INTEGER),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['secondaries'].drop()
    post_meta.tables['characters'].create()
    pre_meta.tables['user'].columns['main'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['secondaries'].create()
    post_meta.tables['characters'].drop()
    pre_meta.tables['user'].columns['main'].create()
