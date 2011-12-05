from django.core.files.storage import FileSystemStorage
from django.conf import settings


DEFAULT_STORAGE = getattr(settings, "FSFIELD_DEFAULT_STORAGE",
        FileSystemStorage())
PATHS_DEPTH = getattr(settings, "FSFIELD_PATHS_DEPTH", 5)
