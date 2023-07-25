from datetime import datetime
import pytz
from cassandra.cqlengine.query import DoesNotExist

from record.model import RecordID, RecordVID


def get_id_by_ref(ref):
    try:
        res = RecordID.objects.filter(ref=ref).allow_filtering().limit(1).get()

    except Exception as e:
        print(f'{e} \n Version does not Exist. get_id_by_ref {ref}')
        return None

    return res.id


def get_id_by_ref_hash(ref_hash):
    try:
        res = RecordID.objects.filter(ref_hash=ref_hash).limit(1).get()

    except Exception as e:
        print(f'{e} \n Version does not Exist. get_id_by_ref_hash')
        return None
    return res.id


def get_last_record_by_id(id):
    try:
        res = RecordVID.objects.filter(id=id).order_by('-vid').limit(1).get()
        res.ref_hash = res.common_hash

    except Exception as e:
        print(f'{e} \n Version does not Exist. get_last_record_by_id {id}')
        return None
    return res


def get_version_by_vid(vid):
    try:
        res = RecordVID.objects.filter(vid=vid).allow_filtering().limit(1).get()
        res.ref_hash = res.common_hash

    except Exception as e:
        print(f'{e} \n Version does not Exist. get_version_by_vid')
        return None
    return res


def clean_after_test():
    try:
        id = RecordID.objects.filter(ref="test:some_value:12345")\
            .allow_filtering().limit(1).get().id
    except Exception as e:
        print('Не удалось найти тестовую запись \n', e)
    try:
        RecordID.objects.filter(id=id).delete()
    except Exception as e:
        print('Не удалось удалить тестовую запись ID \n', e)
    try:
        RecordVID.objects.filter(id=id).allow_filtering().delete()
    except Exception as e:
        print('Не удалось удалить тестовую запись VID \n', e)


def register_id(id, ref_hash, ref):
    return RecordID.create(
        id=id,
        ref=ref,
        ref_hash=ref_hash,
        created_at=datetime.now(pytz.timezone('Asia/Almaty'))
    )


def get_next_version_by_vid(id, v):
    try:
        res = RecordVID.objects.filter(RecordVID.id == id, RecordVID.vid > v).order_by('vid').limit(1).get()
        res.ref_hash = res.common_hash
        return res
    except DoesNotExist as e:
        print(e, f'vid {v} not found')
        return None


def get_prev_version_by_vid(id, v):
    try:
        res = RecordVID.objects.filter(RecordVID.id == id, RecordVID.vid < v).order_by('-vid').limit(1).get()
        res.ref_hash = res.common_hash
        return res
    except DoesNotExist as e:
        print(e, f'vid {v} not found')
        return None
