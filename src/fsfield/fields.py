import os
import os.path as op
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.files.storage import FileSystemStorage
from django.core.files import locks
from fsfield.core import model_instance_field_path, default_storage


class FileStorageFieldDescriptor(object):

    def __init__(self, name, filename, storage, default, load, dump):
        self.name = name
        self.filename = filename
        self.storage = storage
        self.default = default
        self.load = load
        self.dump = dump

    def path(self, obj):
        if obj.pk is None:
            raise AttributeError("you must save the object to the database "
                    "before accessing this field")
        return model_instance_field_path(obj, self.filename)

    def __get__(self, obj, type=None):
        if obj is None:
            return
        if self.name not in obj.__dict__:
            # Load data from disk
            path = self.path(obj)
            if not self.storage.exists(path):
                value = self.default
            else:
                # Open the file for reading and acquire a lock on it if
                # possible
                fp = self.storage.open(path, "r+b")
                if isinstance(self.storage, FileSystemStorage):
                    locks.lock(fp.file, locks.LOCK_EX)
                try:
                    # Read file content
                    if self.load is not None:
                        value = self.load(fp)
                    else:
                        value = fp.read().decode("utf8")
                finally:
                    # Release lock
                    if isinstance(self.storage, FileSystemStorage):
                        locks.unlock(fp.file)
                    # Close file
                    fp.close()
            obj.__dict__[self.name] = value
        return obj.__dict__[self.name]

    def __set__(self, obj, value):
        obj.__dict__[self.name] = value


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

    *filename* may be used to customize the name of the files corresponding to
    this field. The field name is used by default.
    """

    def __init__(self, storage=None, load=None, dump=None, default=None,
            filename=None):
        self.load = load
        self.dump = dump
        if storage is None:
            self.storage = default_storage()
        else:
            self.storage = storage
        self.default = default
        self.filename = filename

    def contribute_to_class(self, cls, name):
        if self.filename is not None:
            filename = self.filename
        else:
            filename = name

        # Create a post_save signal handler to write data to disk 
        @receiver(post_save, sender=cls, weak=False,
                dispatch_uid="fsfield_write_data_%s_%s_%s" % 
                (cls.__module__, cls.__name__, name))
        def write_data(sender, instance, created, raw, using, **kwargs):
            if (name not in instance.__dict__ or
                    instance.__dict__[name] is None):
                # Nothing to save
                return
            # Open the file for writing and acquire a lock on it if
            # possible
            path = model_instance_field_path(instance, filename)
            fs_storage = isinstance(self.storage, FileSystemStorage)
            if fs_storage:
                full_path = self.storage.path(path)
                directory = op.dirname(full_path)
                if not op.exists(directory):
                    try:
                        os.makedirs(directory)
                    except OSError, err:
                        # Another thread may have created the directory since
                        # the check
                        if err.errno == 17:
                            pass
            fp = self.storage.open(path, "wb")
            if fs_storage:
                locks.lock(fp.file, locks.LOCK_EX)
            # Write data
            try:
                value = instance.__dict__[name]
                if self.dump is None:
                    fp.write(value.encode("utf8"))
                else:
                    self.dump(value, fp)
            finally:
                # Release lock
                if fs_storage:
                    locks.unlock(fp.file)
                # Close file
                fp.close()

        # Install field descriptor
        descriptor = FileStorageFieldDescriptor(name, filename, self.storage,
                self.default, self.load, self.dump)
        setattr(cls, name, descriptor)
