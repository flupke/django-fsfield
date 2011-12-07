import os
import os.path as op
from fsfield.core import model_instance_field_path, default_storage


class FileStorageFieldDescriptor(object):

    def __init__(self, name, storage, default, load, dump):
        self.name = name
        self.storage = storage
        self.default = default
        self.load = load
        self.dump = dump

    def path(self, obj):
        return model_instance_field_path(obj, self.name)

    def __get__(self, obj, type=None):
        if obj is None:
            raise AttributeError("can only be accessed via instances")
        if obj.pk is None:
            raise ValueError("you must save the object the database before "
                    "accessing this field")
        path = self.path(obj)
        if not self.storage.exists(path):
            return self.default
        fp = self.storage.open(path, "rb")
        if self.load is not None:
            return self.load(fp)
        return fp.read()

    def __set__(self, obj, value):
        if obj is None:
            raise AttributeError("can only be accessed via instances")
        if obj.pk is None:
            raise ValueError("you must save the object the database before "
                    "accessing this field")
        path = self.path(obj)
        directory = op.dirname(self.storage.path(path))
        if not op.isdir(directory):
            os.makedirs(directory)
        fp = self.storage.open(path, "wb")
        if self.dump is not None:
            self.dump(value, fp)
        else:
            fp.write(value)


class FileStorageField(object):
    """
    This field type stores string data on the disk, bypassing entirely the
    database.

    *storage* may be a :class:`~django.core.files.storage.Storage` subclass to
    customize where the files are stored. The default storage is used if this
    is left unspecified.
    
    You may specify callables in *load* and *dump* to alter the way data is
    loaded from and saved to disk::

        load(fp)
        dump(data, fp)

    Where ``fp`` is a file-like object returned by the storage system.

    *default* is the value returned when the file associated to the field
    doesn't exist.
    """

    def __init__(self, storage=None, load=None, dump=None, default=None):
        self.load = load
        self.dump = dump
        if storage is None:
            self.storage = default_storage()
        else:
            self.storage = storage
        self.default = default

    def contribute_to_class(self, cls, name):
        descriptor = FileStorageFieldDescriptor(name, self.storage,
                self.default, self.load, self.dump)
        setattr(cls, name, descriptor)
