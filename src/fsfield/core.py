import os.path as op
from base64 import b64encode
import hashlib
from django.utils.encoding import force_unicode
from fsfield import settings


_default_storage = None


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
        

def field_path(app_label, model_name, pk, field_name):
    """
    Lower level version of :func:`model_instance_field_path`.
    """
    return op.join(
            app_label, 
            model_name, 
            hashed_path(pk, settings.PATHS_DEPTH), 
            field_name)


def model_instance_field_path(instance, field_name):
    """
    Get the path used to store the Django model *instance* field named
    *field_name*.

    Note that the returned path is a relative path, to get the absolute path,
    you must pass the value returned by this function to your storage's
    :meth:`~django.core.files.storage.Storage.path` method.
    """
    return field_path(
            instance._meta.app_label,
            instance._meta.object_name, 
            instance.pk,
            field_name)


def default_storage():
    """
    Get the default storage instance configured in settings.
    """
    global _default_storage
    if _default_storage is None:
        module, cls_name = settings.DEFAULT_STORAGE_CLASS.rsplit(".", 1)
        args, kwargs = settings.DEFAULT_STORAGE_ARGS
        cls = getattr(__import__(module, {}, {}, cls_name), cls_name)
        _default_storage = cls(*args, **kwargs)
    return _default_storage
