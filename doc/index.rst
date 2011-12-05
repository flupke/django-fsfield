django-fsfield
==============

Scalabe file storage fields for your Django models.

The files are stored on disk by hashing the primary key of the model instance
that contains the field. 

Usage
-----

Simply add :class:`fsfield.fields.FileStorageField` to your models::

    from django.db import models
    from fsfield import FileStorageField

    class MyModel(models.Model):
        
        field = FileStorageField()

The field then acts as a :class:`django.db.models.fields.TextField`::

    >>> obj = MyModel.objects.create()
    >>> obj.field = "foo"
    >>> obj.field
    'foo'

The model instance must be saved to the database before accessing the field.

You can customize the way data is loaded and saved with the ``load`` and
``dump`` parameters of the field::

    from django.db import models
    from django.utils import simplejson as json
    from fsfield import FileStorageField

    class MyModel(models.Model):
        
        json_field = FileStorageField(load=json.load, dump=json.dump)

:class:`~fsfield.fields.FileStorageField` reference
---------------------------------------------------

.. autoclass:: fsfield.fields.FileStorageField
    :members:


Settings
--------

FSFIELD_DEFAULT_STORAGE
    The default :class:`django.core.files.storage.Storage` instance used to
    store files. The default is ``FileSystemStorage()``, storing files in your
    ``MEDIA_ROOT``.

FSFIELD_PATHS_DEPTH
    The number of sub paths used to distribute the files in directories. The
    default is 5, which should be sufficient for billions of files.

