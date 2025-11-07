from rest_framework import viewsets
from .models import *
from .serializers import *
from .utils.pdf_generator import generar_pdf_anamnesis
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
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




Usuario = get_user_model()

@api_view(['POST'])
def password_reset_request(request):
    email = request.data.get('email')
    try:
        user = Usuario.objects.get(email=email)
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        reset_link = f"http://tusitio.cl/password-reset/confirm/{uid}/{token}/"

        send_mail(
            '🔐 Restablecer contraseña',
            f'Hola {user.first_name}, usa este enlace para restablecer tu contraseña:\n{reset_link}',
            'tucorreo@gmail.com',
            [user.email],
            fail_silently=False,
        )
        return Response({'message': 'Correo de recuperación enviado correctamente.'})
    except Usuario.DoesNotExist:
        return Response({'error': 'No existe un usuario con ese correo.'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def password_reset_verify(request):
    uidb64 = request.data.get('uid')
    token = request.data.get('token')
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Usuario.objects.get(pk=uid)
        if default_token_generator.check_token(user, token):
            return Response({'message': 'Token válido.'})
        return Response({'error': 'Token inválido o expirado.'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception:
        return Response({'error': 'Solicitud inválida.'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def password_reset_confirm(request):
    uidb64 = request.data.get('uid')
    token = request.data.get('token')
    new_password = request.data.get('new_password')

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Usuario.objects.get(pk=uid)
        if default_token_generator.check_token(user, token):
            user.set_password(new_password)
            user.save()
            return Response({'message': 'Contraseña restablecida correctamente.'})
        return Response({'error': 'Token inválido o expirado.'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception:
        return Response({'error': 'Error al restablecer la contraseña.'}, status=status.HTTP_400_BAD_REQUEST)






# ================================================================
# VIEWS – REGISTRO PIE
# ================================================================

from rest_framework import viewsets
from .models import (
    RegistroPIE, EquipoAula, PlanificacionPIE, TrabajoColaborativo,
    ActividadComunidad, LogroAprendizaje, EvaluacionPIE
)
from .serializers import (
    RegistroPIESerializer, EquipoAulaSerializer, PlanificacionPIESerializer,
    TrabajoColaborativoSerializer, ActividadComunidadSerializer,
    LogroAprendizajeSerializer, EvaluacionPIESerializer
)


class RegistroPIEViewSet(viewsets.ModelViewSet):
    queryset = RegistroPIE.objects.all().order_by('-fecha_creacion')
    serializer_class = RegistroPIESerializer


class EquipoAulaViewSet(viewsets.ModelViewSet):
    queryset = EquipoAula.objects.all()
    serializer_class = EquipoAulaSerializer


class PlanificacionPIEViewSet(viewsets.ModelViewSet):
    queryset = PlanificacionPIE.objects.all()
    serializer_class = PlanificacionPIESerializer


class TrabajoColaborativoViewSet(viewsets.ModelViewSet):
    queryset = TrabajoColaborativo.objects.all()
    serializer_class = TrabajoColaborativoSerializer


class ActividadComunidadViewSet(viewsets.ModelViewSet):
    queryset = ActividadComunidad.objects.all()
    serializer_class = ActividadComunidadSerializer


class LogroAprendizajeViewSet(viewsets.ModelViewSet):
    queryset = LogroAprendizaje.objects.all()
    serializer_class = LogroAprendizajeSerializer


class EvaluacionPIEViewSet(viewsets.ModelViewSet):
    queryset = EvaluacionPIE.objects.all()
    serializer_class = EvaluacionPIESerializer


@api_view(['GET'])
def generar_registro_pie_pdf(request, registro_id):
    from core.utils.pdf_generator import generar_pdf_registro_pie
    try:
        registro = RegistroPIE.objects.get(pk=registro_id)
        pdf_path = generar_pdf_registro_pie(registro)
        return Response({"pdf": pdf_path})
    except RegistroPIE.DoesNotExist:
        return Response({"error": "Registro PIE no encontrado"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
