django-fsfield
==============

Scalable file storage fields for your Django models.

The files are stored on disk in a tree structure that ensures not too many
files end up in the same directory, to maintain things fast when the number of
files grows. The structure is as follows::

    `~app_name/
      `~ModelName/
        `~N/
          `~W/
            `~o/
              `~Z/
                `~K/
                  `~NWoZK3kTsExUV00Ywo1G5jlUKKs/
                    |-field_name
                    `-other_field_name

Where ``NWoZK3kTsExUV00Ywo1G5jlUKKs`` is a hash made from the model instance's
primary key.

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

.. note::
    The model instance must be saved to the database before accessing the field.

You can customize the way data is loaded and saved with the ``load`` and
``dump`` parameters::

    from django.db import models
    from django.utils import simplejson as json
    from fsfield import FileStorageField

    class MyModel(models.Model):
        
        json_field = FileStorageField(load=json.load, dump=json.dump)

``json_field`` can then be used to store JSON data directly::

    >>> obj = MyModel.objects.create()
    >>> obj.json_field = {"data": 1}
    >>> obj.json_field
    {"data": 1}

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
    The number of sub paths used to distribute the files in directories.

.. warning::
    Changing this setting will make old files unreachable. The default of 5
    should be enough for most uses (average 93 files per directory for 100
    billion files)
