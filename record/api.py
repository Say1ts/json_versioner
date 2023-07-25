from typing import Optional

from record.schema import MergeEvolution, VersionResponse, NotifyUserResponse, RecordCreator, RegisterRefResponse
from record.services.Registrator import IdRecord, VidRecord
import record.services.queries as db
import json
from Notification.Notification import notificator
from record.services.merge_evolution import calculate_merge_evolution


class API:
    registrator_id = IdRecord
    registrator_vid = VidRecord

    @staticmethod
    def __get_specific_fields_version(response) -> VersionResponse:
        res = {
            'id': response.id,
            'vid': response.vid,
            'ref': response.ref,
            'ref_hash': response.ref_hash,
            'content': json.loads(response.content),
            'evolution': json.loads(response.evolution),
            'content_hash': response.common_hash
        }
        return VersionResponse(**res)

    @classmethod
    def register_ref(cls, ref: str):
        obj = cls.registrator_id(ref=ref)
        obj.register()
        res = {
            'id': obj.id,
            'ref': obj.ref,
            'ref_hash': obj.ref_hash,
        }
        return RegisterRefResponse(**res)

    @classmethod
    def register_version(cls, item: RecordCreator, without_commit: Optional[bool] = False) -> VersionResponse:
        version = cls.registrator_vid(item.ref, item.content)
        response = version.register(without_commit=without_commit)
        res = {
            'id': response.id,
            'vid': response.vid,
            'ref': response.ref,
            'ref_hash': version.ref_registrator.ref_hash,
            'content': item.content,
            'evolution': json.loads(response.evolution),
            'content_hash': version.common_hash
        }
        return VersionResponse(**res)

    @staticmethod
    def get_merge_evolution(old_vid: int, new_vid: int) -> MergeEvolution:
        response = calculate_merge_evolution(old_vid, new_vid)
        if isinstance(response, dict):
            return MergeEvolution(**response)
        res = {
            'id': response.id,
            'vid': response.vid,
            'ref': response.ref,
            'ref_hash': response.ref_hash,
            'content': response.content,
            'evolution': response.evolution,
            'content_hash': response.content_hash
        }
        return MergeEvolution(**res)

    @classmethod
    def register_version_by_user(cls, item: RecordCreator, user: str) -> NotifyUserResponse:
        result = cls.register_version(item)
        message = result.evolution
        response = NotifyUserResponse(
            message=message,
            user=user,
            is_notified=notificator.notify(user, message),
            version=VersionResponse(**result.dict()),
        )
        return response

    @staticmethod
    def get_last_version_by_ref(ref: str) -> VersionResponse:
        id = db.get_id_by_ref(ref)
        response = db.get_last_record_by_id(id)
        if not response:
            return VersionResponse(exists=False, ref=ref)
        return API.__get_specific_fields_version(response)

    @staticmethod
    def get_last_version_by_ref_hash(ref_hash: str) -> VersionResponse:
        id = db.get_id_by_ref_hash(ref_hash)
        response = db.get_last_record_by_id(id)
        if not response:
            return VersionResponse(exists=False, ref_hash=ref_hash)
        return API.__get_specific_fields_version(response)

    @staticmethod
    def get_last_version_by_id(id: int) -> VersionResponse:
        response = db.get_last_record_by_id(id)
        if not response:
            return VersionResponse(exists=False, id=id)
        return API.__get_specific_fields_version(response)

    @staticmethod
    def get_version_by_vid(vid: int) -> VersionResponse:
        response = db.get_version_by_vid(vid)
        if not response:
            return VersionResponse(exists=False, vid=vid)
        return API.__get_specific_fields_version(response)

    @staticmethod
    def get_next_version_by_vid(vid: int) -> VersionResponse:
        try:
            id = db.get_version_by_vid(vid).id
            response = db.get_next_version_by_vid(id, vid)
            return API.__get_specific_fields_version(response)
        except AttributeError as e:
            print(e)
            return VersionResponse(exists=False)

    @staticmethod
    def get_prev_version_by_vid(vid: int) -> VersionResponse:
        try:
            id = db.get_version_by_vid(vid).id
            response = db.get_prev_version_by_vid(id, vid)
            return API.__get_specific_fields_version(response)
        except AttributeError as e:
            print(e)
            return VersionResponse(exists=False)

    @staticmethod
    def clean_after_test():
        db.clean_after_test()
