try:
    from importlib import import_module
    from django.template.defaulttags import url
    from django.contrib.contenttypes import admin as ct_admin
except (ImportError, ModuleNotFoundError) as ex:
    print(f'ModuleNotFoundError: {ex}')
