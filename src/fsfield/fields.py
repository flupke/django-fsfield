import os
import os.path as op
from fsfield import settings
from fsfield.core import hashed_path


class FileStorageFieldDescriptor(object):

    def __init__(self, model, name, storage, default, load, dump):
        self.model = model
        self.name = name
        self.storage = storage
        self.default = default
        self.load = load
        self.dump = dump

    def path(self, obj):
        return op.join(
                self.model._meta.app_label,
                self.model._meta.object_name, 
                hashed_path(obj.pk, settings.PATHS_DEPTH),
                self.name)

    def __get__(self, obj, type=None):
        if obj is None:
            raise AttributeError("can only be accessed via instances")
        if obj.pk is None:
            raise ValueError("%s primary key is None, you must save it to "
                    "the database before accessing this field")
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
            raise ValueError("%s primary key is None, you must save it to "
                    "the database before accessing this field")
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
    """

    def __init__(self, storage=None, load=None, dump=None, default=None):
        self.load = load
        self.dump = dump
        if storage is None:
            self.storage = settings.DEFAULT_STORAGE
        else:
            self.storage = storage
        self.default = default

    def contribute_to_class(self, cls, name):
        descriptor = FileStorageFieldDescriptor(cls, name, self.storage,
                self.default, self.load, self.dump)
        setattr(cls, name, descriptor)
