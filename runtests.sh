coverage run --source fsfield test_project/manage.py test fsfield
coverage report --omit="src/fsfield/tests*" -m
