import os.path as op
import shutil
from django.conf import settings
from fsfield.tests.base import SettingsTestCase
from fsfield.tests.models import StorageModel
from fsfield.core import model_instance_field_path
from fsfield.tests.models import storage


tmp_dir = op.join(op.dirname(__file__), "tmp")


class FileStorageFieldTests(SettingsTestCase):

    def setUp(self):
        new_apps = settings.INSTALLED_APPS + ["fsfield.tests"]
        self.settings_manager.set(
            INSTALLED_APPS=new_apps,
        )
        if op.isdir(tmp_dir):
            shutil.rmtree(tmp_dir)

    def test_class_access(self):
        self.assertEqual(StorageModel.simple_file_field, None)

    def test_simple_field(self):
        obj = StorageModel.objects.create()
        self.assertEqual(obj.simple_file_field, None)
        obj.simple_file_field = "foo"
        obj.save()
        obj = StorageModel.objects.get(pk=obj.pk)
        self.assertEqual(obj.simple_file_field, "foo")

    def test_field_with_accessors(self):
        obj = StorageModel.objects.create()
        obj.json_file_field = {"foo": 12}
        obj.save()
        obj = StorageModel.objects.get(pk=obj.pk)
        self.assertEqual(obj.json_file_field, {"foo": 12})

    def test_errors(self):
        obj = StorageModel()
        self.assertRaises(AttributeError, getattr, obj, "simple_file_field")
    
    def test_custom_filename_field(self):
        obj = StorageModel.objects.create()
        obj.custom_name_file_field = "flap"
        obj.save()
        path = storage.path(model_instance_field_path(obj, "custom"))
        self.assertEqual(op.exists(path), True)
        self.assertEqual(open(path).read(), "flap")
