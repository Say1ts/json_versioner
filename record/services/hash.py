import hashlib
import json


class Hasher:
    def __init__(self, obj):
        self.obj = obj

    @staticmethod
    def get_hash_for_two_vals(key, value) -> str:
        if isinstance(value, dict):
            value = json.dumps(value, sort_keys=True)
        elif type(value) is not str:
            value = str(value)
        return str(hashlib.sha256(
            (key + value).encode('utf-8')
        ).hexdigest())

    @staticmethod
    def get_ref_hash(ref):
        return hashlib.sha256(ref.encode('utf-8')).hexdigest()
