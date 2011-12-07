import os.path as op
from base64 import b64encode
import hashlib
from django.utils.encoding import force_unicode
from fsfield import settings


# Storage instances
_storage_cache = {}


def path_hash(value):
    """
    Get the hash used to store something named *value* in the filesystem.
    """
    value_str = force_unicode(value).encode("utf8")
    digest = hashlib.sha1(value_str).digest()
    return b64encode(digest, "_-").rstrip("=")


def hashed_path(value, depth):
    """
    Get the hashed path corresponding to *value*, with *depth* levels of 
    sub-directories.
    """
    hashed = path_hash(value)
    components = [hashed[i] for i in range(depth)]
    components.append(hashed)
    return op.join(*components)
        

def model_instance_field_path(instance, field_name):
    """
    Get the path used to store the Django model *instance* field named
    *field_name*.
    """
    return op.join(
        instance._meta.app_label,
        instance._meta.object_name, 
        hashed_path(instance.pk, settings.PATHS_DEPTH),
        field_name)


def default_storage():
    """
    Get the default storage instance configured in settings.
    """
    args, kwargs = settings.DEFAULT_STORAGE_ARGS
    key = (settings.DEFAULT_STORAGE_CLASS, tuple(args), tuple(kwargs.items()))
    if key not in _storage_cache:
        module, cls_name = settings.DEFAULT_STORAGE_CLASS.rsplit(".", 1)
        cls = getattr(__import__(module, {}, {}, cls_name), cls_name)
        _storage_cache[key] = cls(*args, **kwargs)
    return _storage_cache[key]
