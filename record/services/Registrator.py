import hashlib
import json

from record.services.queries import *
from record.services.hash import Hasher
import redis_counter
from collections import namedtuple


class IdRecord:
    def __init__(self, ref: str):
        self.hasher = Hasher(self)
        self.__id = None
        self.__last_version = None
        self.exists = None
        self.ref = ref
        if ref:
            self.ref_hash = self.hasher.get_ref_hash(ref)

        self.model = RecordID

    @property
    def ref(self) -> str:
        return self.__ref

    @ref.setter
    def ref(self, value: str) -> None:
        self.__ref = value
        self.ref_hash = self.hasher.get_ref_hash(value)

    @property
    def id(self) -> int:
        if self.__id is None:
            self.__id = get_id_by_ref(self.ref)
        return self.__id

    @id.setter
    def id(self, value: int) -> None:
        if value is None:
            self.__id = redis_counter.generate_id()
            register_id(self.id, self.ref_hash, self.ref)
            self.exists = False
        else:
            self.__id = value

    @property
    def last_version(self) -> RecordVID or None:
        if self.exists is not False:
            if self.__last_version:
                return self.__last_version
            try:
                self.__last_version = get_last_record_by_id(self.id)
                return self.__last_version
            except Exception as e:
                print(e)
                return None

    def register(self) -> None:
        self.id = get_id_by_ref_hash(self.ref_hash)


class VidRecord:
    def __init__(self, ref: str, content: dict):
        self.hasher = Hasher(self)
        self.ref = ref
        self.vid = None
        self.evolution = None
        self.content_hashes = None
        self.common_hash = None
        self.last_content = None

        self.origin_content = content
        self.content = content
        self.model = RecordVID
        self.ref_registrator = IdRecord(ref)

    @property
    def content(self) -> dict:
        return self.__content

    @content.setter
    def content(self, content: dict):
        self.__content = content
        self.get_common_hash()

    def compare_content_hashes(self) -> bool:
        if self.ref_registrator.last_version:
            if self.common_hash == \
                    self.ref_registrator.last_version.common_hash:
                return True

    def get_last_evol_and_hashes(self) -> None:
        if self.ref_registrator.last_version is not None:
            self.evolution = json.loads(
                self.ref_registrator.last_version.evolution)
            self.content_hashes = json.loads(
                self.ref_registrator.last_version.content_hashes)
            self.last_content = json.loads(
                self.ref_registrator.last_version.content)

            self.clean_deleted_keys_from_old_content()
        else:
            self.evolution = {}
            self.content_hashes = {}
            self.last_content = {}

    def clean_deleted_keys_from_old_content(self) -> None:
        list_of_keys_for_deletion = []
        for key, value in self.evolution.items():
            if value == -1:
                list_of_keys_for_deletion.append(key)
        for key in list_of_keys_for_deletion:
            del self.evolution[key]
            del self.content_hashes[key]
            del self.last_content[key]
            
    def register(self, without_commit=False) -> RecordVID or namedtuple:
        self.ref_registrator.register()

        # Check for existing the same version in db.
        if self.compare_content_hashes():
            return self.ref_registrator.last_version

        self.get_last_evol_and_hashes()
        self.vid = redis_counter.generate_vid()
        self.calculate_new_evol_and_hashes()

        if without_commit:
            result = namedtuple('RecordVID', self.get_params().keys())
            return result(**self.get_params())
        return RecordVID.create(**self.get_params())

    def get_vid(self) -> None:
        self.vid = redis_counter.generate_vid()

    def get_params(self) -> dict:
        params = {
            'vid': self.vid,
            'id': self.ref_registrator.id,
            'ref': self.ref,

            'created_at': datetime.now(pytz.timezone('Asia/Almaty')),

            'content': json.dumps(self.origin_content),
            'evolution': json.dumps(self.evolution),
            'common_hash': self.common_hash,

            'content_hashes': json.dumps(self.content_hashes),
        }
        return params

    def convert_nested_content(self):
        result_content = self.content.copy()
        for key, value in result_content.items():
            if isinstance(result_content, dict):
                result_content[key] = json.dumps(value)
            elif isinstance(result_content, str):
                continue
            result_content[key] = str(value)
            return result_content

    def calculate_new_evol_and_hashes(self):

        content_for_evolution = self.convert_nested_content()
        sorted_new_content = dict(sorted(content_for_evolution.items()))
        for new_key, new_value in sorted_new_content.items():
            # получаем хэш для текущей пары ключ-значение
            current_hash = self.hasher.get_hash_for_two_vals(new_key, new_value)

            if new_key in self.content_hashes.keys():
                # сравниваем значения получившегося хеша с ранними хешами
                if current_hash != self.content_hashes[new_key]:
                    self.evolution[new_key] = self.vid
                    self.content_hashes[new_key] = current_hash
                
                # удаляем из предыдущего контента то, что уже обработано и есть в текущем
                self.last_content.pop(new_key)

            else:
                self.evolution[new_key] = self.vid
                self.content_hashes[new_key] = current_hash

        self.migrate_old_content_to_current()

    def migrate_old_content_to_current(self):
        for key, value in self.last_content.items():
            self.content[key] = value
            self.evolution[key] = -1

    def get_common_hash(self):
        converted_content = self.convert_nested_content()
        solt = 'f2d1f7be40303c7a2312c5a5e071d66e' \
               '960936fd22f41d3860326eed78f42b48'
        sorted_content = dict(sorted(converted_content.items()))
        prev_hash = solt
        if converted_content != prev_hash:
            for key, value in sorted_content.items():
                if self.evolution:
                    if self.evolution[key] != -1:
                        current_hash = Hasher.get_hash_for_two_vals(key, value)
                        prev_hash = Hasher.get_hash_for_two_vals\
                            (current_hash, prev_hash)
                else:
                    current_hash = Hasher.get_hash_for_two_vals(key, value)
                    prev_hash = Hasher.get_hash_for_two_vals \
                        (current_hash, prev_hash)
        self.common_hash = str(prev_hash)




