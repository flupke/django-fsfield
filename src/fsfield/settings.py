from django.conf import settings


DEFAULT_STORAGE_CLASS = getattr(settings, "FSFIELD_DEFAULT_STORAGE_CLASS",
        "django.core.files.storage.FileSystemStorage")
DEFAULT_STORAGE_ARGS = getattr(settings, "FSFIELD_DEFAULT_STORAGE_ARGS", 
        ((), {}))
PATHS_DEPTH = getattr(settings, "FSFIELD_PATHS_DEPTH", 5)
