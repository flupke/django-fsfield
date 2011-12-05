import os.path as op
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.utils import simplejson as json
from fsfield import FileStorageField


tmp_dir = op.join(op.dirname(__file__), "tmp")
storage = FileSystemStorage(tmp_dir)

class StorageModel(models.Model):

    normal_field = models.CharField(max_length=255)
    simple_file_field = FileStorageField(storage)
    json_file_field = FileStorageField(storage, load=json.load, dump=json.dump)
