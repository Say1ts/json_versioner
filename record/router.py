from record.schema import Record, RecordCreator, RefHash, Ref, Id, Vid, MergeEvolution
from fastapi import APIRouter

from record.api import API

record_router = APIRouter()


@record_router.get("/vid/{vid}", tags=["record"])
async def get_version_by_vid(vid: int):
    return API.get_version_by_vid(vid)


@record_router.get("/ref/{ref}", tags=["record"])
async def get_last_version_by_ref(ref: str):
    return API.get_last_version_by_ref(ref)


@record_router.get("/ref_hash/{ref_hash}", tags=["record"])
async def get_last_version_by_ref_hash(ref_hash: str):
    return API.get_last_version_by_ref_hash(ref_hash)


@record_router.get("/id/{id}", tags=["record"])
async def get_last_version_by_id(id: int):
    return API.get_last_version_by_id(id)


@record_router.post("/register/content", tags=["record"])
async def register_version(item: RecordCreator):
    return API.register_version(item)


@record_router.post("/register/content_without_commit", tags=["record"])
async def register_version_without_commit(item: RecordCreator):
    return API.register_version(item, without_commit=True)


@record_router.post("/register/content_by_user/{user}", tags=["record"])
async def register_version_by_user(item: RecordCreator, user):
    return API.register_version_by_user(item, user)


@record_router.post("/register/ref/{ref}", tags=["record"])
async def register_ref(ref: str):
    return API.register_ref(ref)


@record_router.post("/register/merge-evolution/", tags=["record"])
async def merge_evolution(old_id: int, new_id: int):
    return API.get_merge_evolution(old_id, new_id)


@record_router.get("/get_next_version_by_vid/{v}", tags=["record"])
async def get_next_version_by_vid(v: int):
    return API.get_next_version_by_vid(v)


@record_router.get("/get_prev_version_by_vid/{v}", tags=["record"])
async def get_prev_version_by_vid(v: int):
    return API.get_prev_version_by_vid(v)


@record_router.post("/test/", tags=["record"])
async def clean_after_test():
    return API.clean_after_test()
