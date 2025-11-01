from rest_framework import viewsets
from .models import *
from .serializers import *
from .utils.pdf_generator import generar_pdf_anamnesis
# ================================================================
# CRUDs Automáticos
# ================================================================

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

class EspecialidadViewSet(viewsets.ModelViewSet):
    queryset = Especialidad.objects.all()
    serializer_class = EspecialidadSerializer

class CursoViewSet(viewsets.ModelViewSet):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer

class ApoderadoViewSet(viewsets.ModelViewSet):
    queryset = Apoderado.objects.all()
    serializer_class = ApoderadoSerializer

class EstudianteViewSet(viewsets.ModelViewSet):
    queryset = Estudiante.objects.all()
    serializer_class = EstudianteSerializer

class EvaluacionIntegralViewSet(viewsets.ModelViewSet):
    queryset = EvaluacionIntegral.objects.all()
    serializer_class = EvaluacionIntegralSerializer

class AnamnesisViewSet(viewsets.ModelViewSet):
    queryset = Anamnesis.objects.all()
    serializer_class = AnamnesisSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        pdf_path = generar_pdf_anamnesis(instance)
        instance.pdf_generado = pdf_path
        instance.save()

    def perform_update(self, serializer):
        instance = serializer.save()
        pdf_path = generar_pdf_anamnesis(instance)
        instance.pdf_generado = pdf_path
        instance.save()


class EvaluacionPsicopedagogicaViewSet(viewsets.ModelViewSet):
    queryset = EvaluacionPsicopedagogica.objects.all()
    serializer_class = EvaluacionPsicopedagogicaSerializer

class EvaluacionSaludViewSet(viewsets.ModelViewSet):
    queryset = EvaluacionSalud.objects.all()
    serializer_class = EvaluacionSaludSerializer

class InformeFamiliaViewSet(viewsets.ModelViewSet):
    queryset = InformeFamilia.objects.all()
    serializer_class = InformeFamiliaSerializer


class EstablecimientoViewSet(viewsets.ModelViewSet):
    """
    Vista CRUD para la gestión de establecimientos (colegios/escuelas)
    """
    queryset = Establecimiento.objects.all().order_by('nombre')
    serializer_class = EstablecimientoSerializer
