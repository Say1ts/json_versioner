import json
from collections import namedtuple

from record.services.queries import get_version_by_vid


def calculate_merge_evolution(old_vid, new_vid):
    old = get_version_by_vid(old_vid)
    new = get_version_by_vid(new_vid)

    if not old:
        return {'exists': False, 'old_vid': old_vid}

    if not new:
        return {'exists': False, 'new_vid': new_vid}

    if old.id != new.id:
        return {'error': 'different references of the versions'}

    if old.vid > new.vid:
        return {'error': '"old_vid" is greater than "new_vid"'}

    old_content = json.loads(old.content)
    new_content = json.loads(new.content)
    new_evolution = json.loads(new.evolution)

    response = namedtuple('response', [
        'id', 'vid', 'ref', 'ref_hash', 'content', 'evolution', 'content_hash'])

    for key, value in old_content.items():
        if key not in new_content.keys():
            new_content[key] = value
            new_evolution[key] = -1
    return response(new.id, new.vid, new.ref, new.ref_hash,
                    new_content, new_evolution, new.common_hash)
