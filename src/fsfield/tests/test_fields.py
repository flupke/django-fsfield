import os.path as op
import shutil
from django.conf import settings
from fsfield.tests.base import SettingsTestCase
from fsfield.tests.models import StorageModel


tmp_dir = op.join(op.dirname(__file__), "tmp")


class FileStorageFieldTests(SettingsTestCase):

    def setUp(self):
        new_apps = settings.INSTALLED_APPS + ["fsfield.tests"]
        self.settings_manager.set(
            INSTALLED_APPS=new_apps,
        )
        if op.isdir(tmp_dir):
            shutil.rmtree(tmp_dir)

    def test_access(self):
        # Simple field
        obj = StorageModel.objects.create()
        self.assertEqual(obj.simple_file_field, None)
        obj.simple_file_field = "foo"
        obj = StorageModel.objects.get(pk=obj.pk)
        self.assertEqual(obj.simple_file_field, "foo")
        # Field with custom accessors
        obj.json_file_field = {"foo": 12}
        self.assertEqual(obj.json_file_field, {"foo": 12})
