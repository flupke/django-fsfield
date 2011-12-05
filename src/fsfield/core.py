import os.path as op
from base64 import b64encode
import hashlib
from django.utils.encoding import force_unicode



def path_hash(value):
    """
    Get the hash used to store something named *value* in the filesystem.
    """
    value_str = force_unicode(value).encode("utf8")
    digest = hashlib.sha1(value_str).digest()
    return b64encode(digest, "_-").rstrip("=")


def hashed_path(value, depth):
    hashed = path_hash(value)
    components = [hashed[i] for i in range(depth)]
    components.append(hashed)
    return op.join(*components)
        
