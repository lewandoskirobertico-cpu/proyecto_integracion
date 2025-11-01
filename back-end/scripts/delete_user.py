import os
import django
import traceback

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mi_api.settings')
django.setup()

from core.models import Usuario

TARGET_ID = 2

try:
    u = Usuario.objects.get(id_usuario=TARGET_ID)
    print('Encontrado usuario:', u)
    u.delete()
    print('Eliminado OK')
except Exception as e:
    print('EXCEPTION:', repr(e))
    traceback.print_exc()
