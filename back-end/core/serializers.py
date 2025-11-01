from rest_framework import serializers
from .models import *

# ================================================================
# 1. SERIALIZADORES BASE
# ================================================================

class EstablecimientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Establecimiento
        fields = '__all__'

class EspecialidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Especialidad
        fields = '__all__'


class UsuarioSerializer(serializers.ModelSerializer):
    especialidad = EspecialidadSerializer(read_only=True)
    especialidad_id = serializers.PrimaryKeyRelatedField(
        source='especialidad', queryset=Especialidad.objects.all(), write_only=True, required=False
    )

    class Meta:
        model = Usuario
        fields = '__all__'


class CursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso
        fields = '__all__'


class ApoderadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Apoderado
        fields = '__all__'


class EstudianteSerializer(serializers.ModelSerializer):
    curso = CursoSerializer(read_only=True)
    curso_id = serializers.PrimaryKeyRelatedField(
        source='curso', queryset=Curso.objects.all(), write_only=True, required=False
    )
    apoderado = ApoderadoSerializer(read_only=True)
    apoderado_id = serializers.PrimaryKeyRelatedField(
        source='apoderado', queryset=Apoderado.objects.all(), write_only=True, required=False
    )

    class Meta:
        model = Estudiante
        fields = '__all__'

# ================================================================
# 2. EVALUACIÓN INTEGRAL
# ================================================================

class EvaluacionIntegralSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvaluacionIntegral
        fields = '__all__'

# ================================================================
# 3. ANAMNESIS
# ================================================================

class InformanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Informante
        fields = '__all__'

class EntrevistadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entrevistador
        fields = '__all__'

class AntecedenteSaludSerializer(serializers.ModelSerializer):
    class Meta:
        model = AntecedenteSalud
        fields = '__all__'

class AnamnesisSerializer(serializers.ModelSerializer):
    informantes = InformanteSerializer(many=True, read_only=True)
    entrevistadores = EntrevistadorSerializer(many=True, read_only=True)
    antecedentes_salud = AntecedenteSaludSerializer(many=True, read_only=True)

    class Meta:
        model = Anamnesis
        fields = '__all__'

# ================================================================
# 4. EVALUACIÓN PSICOPEDAGÓGICA
# ================================================================

class SubdimensionItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubdimensionItem
        fields = '__all__'

class SubsectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subsector
        fields = '__all__'

class EstrategiaApoyoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstrategiaApoyo
        fields = '__all__'

class ApoyoAdicionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApoyoAdicional
        fields = '__all__'

class EvaluacionPsicopedagogicaSerializer(serializers.ModelSerializer):
    items = SubdimensionItemSerializer(many=True, read_only=True)
    subsectores = SubsectorSerializer(many=True, read_only=True)
    estrategias_apoyo = EstrategiaApoyoSerializer(many=True, read_only=True)
    apoyos_adicionales = ApoyoAdicionalSerializer(many=True, read_only=True)

    class Meta:
        model = EvaluacionPsicopedagogica
        fields = '__all__'

# ================================================================
# 5. EVALUACIÓN DE SALUD
# ================================================================

class EvaluacionSaludSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvaluacionSalud
        fields = '__all__'

# ================================================================
# 6. INFORME PARA LA FAMILIA
# ================================================================

class InformeFamiliaInstrumentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = InformeFamiliaInstrumento
        fields = '__all__'

class InformeFamiliaAmbitoSerializer(serializers.ModelSerializer):
    class Meta:
        model = InformeFamiliaAmbito
        fields = '__all__'

class InformeFamiliaSeguimientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = InformeFamiliaSeguimiento
        fields = '__all__'

class InformeFamiliaEntregaSerializer(serializers.ModelSerializer):
    class Meta:
        model = InformeFamiliaEntrega
        fields = '__all__'

class InformeFamiliaReceptorSerializer(serializers.ModelSerializer):
    class Meta:
        model = InformeFamiliaReceptor
        fields = '__all__'

class InformeFamiliaSerializer(serializers.ModelSerializer):
    instrumentos = InformeFamiliaInstrumentoSerializer(many=True, read_only=True)
    ambitos = InformeFamiliaAmbitoSerializer(many=True, read_only=True)
    seguimientos = InformeFamiliaSeguimientoSerializer(many=True, read_only=True)
    entrega = InformeFamiliaEntregaSerializer(many=True, read_only=True)
    receptores = InformeFamiliaReceptorSerializer(many=True, read_only=True)

    class Meta:
        model = InformeFamilia
        fields = '__all__'
