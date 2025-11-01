from rest_framework import routers
from .views import *

router = routers.DefaultRouter()

router.register('usuarios', UsuarioViewSet)
router.register('especialidades', EspecialidadViewSet)
router.register('cursos', CursoViewSet)
router.register('apoderados', ApoderadoViewSet)
router.register('estudiantes', EstudianteViewSet)
router.register('evaluaciones-integrales', EvaluacionIntegralViewSet)
router.register('anamnesis', AnamnesisViewSet)
router.register('evaluaciones-psicopedagogicas', EvaluacionPsicopedagogicaViewSet)
router.register('evaluaciones-salud', EvaluacionSaludViewSet)
router.register('informes-familia', InformeFamiliaViewSet)
router.register('establecimientos', EstablecimientoViewSet)


urlpatterns = router.urls
