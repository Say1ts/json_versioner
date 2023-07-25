from cassandra.cqlengine import columns
from base.model import BaseModel


class RecordVID(BaseModel):
    id = columns.BigInt(primary_key=True)
    vid = columns.BigInt(primary_key=True, clustering_order="DESC")

    ref = columns.Text(index=True)

    content = columns.Text()
    evolution = columns.Text()
    common_hash = columns.Text(index=True)

    content_hashes = columns.Text(index=True)


class RecordID(BaseModel):
    id = columns.BigInt(primary_key=True)
    ref_hash = columns.Text(index=True)
    ref = columns.Text()
