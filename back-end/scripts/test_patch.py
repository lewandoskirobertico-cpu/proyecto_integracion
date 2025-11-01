import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','mi_api.settings')
import django
django.setup()
from django.test import Client
c = Client()
# Attempt to patch user 2
resp = c.patch('/api/usuarios/2/', {'nombre':'AnaPatched'}, content_type='application/json')
print('status', resp.status_code)
print(resp.content)
