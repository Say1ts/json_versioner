
from cassandra.cqlengine.models import Model
from cassandra.cqlengine import columns

from database.config import SCYLLA_KEYSPACE


class BaseModel(Model):
    __abstract__ = True
    __keyspace__ = SCYLLA_KEYSPACE
    __connection__ = 'cluster1'
    created_at = columns.DateTime()


class VersionModel(BaseModel):
    __abstract__ = True

    content = columns.Text()
    evolution = columns.Text()
    common_hash = columns.Text(index=True)

    content_hashes = columns.Text()
