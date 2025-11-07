from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import timedelta
import uuid
# ================================================================
# 1. USUARIO PERSONALIZADO (PROFESIONAL)
# ================================================================

class Especialidad(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre



class Establecimiento(models.Model):
    nombre = models.CharField(max_length=200)
    rbd = models.CharField(max_length=20, unique=True, blank=True, null=True)
    direccion = models.CharField(max_length=200, blank=True, null=True)
    comuna = models.CharField(max_length=100, blank=True, null=True)
    region = models.CharField(max_length=100, blank=True, null=True)
    telefono = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    tipo_dependencia = models.CharField(
        max_length=50,
        choices=[
            ('Municipal', 'Municipal'),
            ('Particular Subvencionado', 'Particular Subvencionado'),
            ('Particular Pagado', 'Particular Pagado'),
            ('Corporación', 'Corporación'),
        ],
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.nombre} ({self.comuna})"

class Usuario(AbstractUser):
    telefono = models.CharField(max_length=20, blank=True, null=True)
    tipo = models.CharField(
        max_length=20,
        choices=[('Interno', 'Interno'), ('Externo', 'Externo')],
        default='Interno'
    )
    especialidad = models.ForeignKey(
        Especialidad, on_delete=models.SET_NULL, null=True, blank=True
    )
    establecimiento = models.ForeignKey(
        Establecimiento, on_delete=models.SET_NULL, null=True, blank=True, related_name='usuarios'
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.especialidad or 'Sin especialidad'})"



# ================================================================
# 2. CONTEXTO INSTITUCIONAL Y FAMILIAR
# ================================================================

class Curso(models.Model):
    nombre = models.CharField(max_length=50)
    nivel = models.CharField(max_length=30, blank=True, null=True)
    anio_escolar = models.PositiveIntegerField(blank=True, null=True)
    establecimiento = models.ForeignKey(
        Establecimiento, on_delete=models.CASCADE, related_name='cursos'
    )

    def __str__(self):
        return f"{self.nombre} - {self.anio_escolar or ''}"

class Apoderado(models.Model):
    nombres_apellidos = models.CharField(max_length=100)
    run = models.CharField(max_length=12, unique=True, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    correo = models.EmailField(blank=True, null=True)
    direccion = models.CharField(max_length=200, blank=True, null=True)
    parentesco = models.CharField(max_length=50, blank=True, null=True)
    ocupacion = models.CharField(max_length=100, blank=True, null=True)
    escolaridad = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.nombres_apellidos

class Estudiante(models.Model):
    nombres_apellidos = models.CharField(max_length=100)
    nombre_social = models.CharField(max_length=100, blank=True, null=True)
    run = models.CharField(max_length=12, unique=True, blank=True, null=True)
    genero = models.CharField(max_length=1, blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    nacionalidad = models.CharField(max_length=50, blank=True, null=True)
    lengua_origen = models.CharField(max_length=50, blank=True, null=True)
    lengua_uso = models.CharField(max_length=50, blank=True, null=True)
    curso = models.ForeignKey(Curso, on_delete=models.SET_NULL, null=True, blank=True, related_name='estudiantes')
    apoderado = models.ForeignKey(Apoderado, on_delete=models.SET_NULL, null=True, blank=True, related_name='estudiantes')
    establecimiento = models.ForeignKey(
        Establecimiento, on_delete=models.SET_NULL, null=True, blank=True, related_name='estudiantes'
    )

    def __str__(self):
        return self.nombres_apellidos

# ================================================================
# 3. EVALUACIÓN INTEGRAL
# ================================================================

class EvaluacionIntegral(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE, related_name='evaluaciones_integrales')
    fecha_inicio = models.DateField(blank=True, null=True)
    fecha_cierre = models.DateField(blank=True, null=True)
    estado = models.CharField(
        max_length=20,
        choices=[('En proceso', 'En proceso'), ('Finalizada', 'Finalizada')],
        default='En proceso'
    )
    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Evaluación de {self.estudiante} ({self.estado})"

# ================================================================
# 4. ANAMNESIS
# ================================================================
class Anamnesis(models.Model):
    evaluacion_integral = models.ForeignKey(EvaluacionIntegral, on_delete=models.CASCADE, related_name='anamnesis')
    fecha = models.DateField(blank=True, null=True)
    definicion_problema = models.TextField(blank=True, null=True)
    observaciones_generales = models.TextField(blank=True, null=True)
    pdf_generado = models.FileField(upload_to='anamnesis_pdfs/', blank=True, null=True)

    def __str__(self):
        return f"Anamnesis de {self.evaluacion_integral.estudiante}"


class Informante(models.Model):
    anamnesis = models.ForeignKey(Anamnesis, on_delete=models.CASCADE, related_name='informantes')
    fecha_entrevista = models.DateField(blank=True, null=True)
    nombre = models.CharField(max_length=100)
    relacion_estudiante = models.CharField(max_length=50)
    presencia = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} ({self.relacion_estudiante})"


class Entrevistador(models.Model):
    anamnesis = models.ForeignKey(Anamnesis, on_delete=models.CASCADE, related_name='entrevistadores')
    nombre = models.CharField(max_length=100)
    rol_cargo = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.nombre


class AntecedenteSalud(models.Model):
    anamnesis = models.ForeignKey(Anamnesis, on_delete=models.CASCADE, related_name='antecedentes_salud')
    diagnostico_prev = models.CharField(max_length=255, blank=True, null=True)
    tipo_parto = models.CharField(max_length=50, blank=True, null=True)
    asistencia_parto = models.BooleanField(default=False)
    peso = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    talla = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    antecedentes_embarazo = models.TextField(blank=True, null=True)
    hospitalizaciones = models.BooleanField(default=False)
    vacunas = models.BooleanField(default=True)
    observaciones = models.TextField(blank=True, null=True)

# ================================================================
# 5. EVALUACIÓN PSICOPEDAGÓGICA
# ================================================================

class EvaluacionPsicopedagogica(models.Model):
    evaluacion_integral = models.ForeignKey(EvaluacionIntegral, on_delete=models.CASCADE, related_name='evaluacion_psicopedagogica')
    evaluador = models.CharField(max_length=100, blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Evaluación Psico de {self.evaluacion_integral.estudiante}"


class SubdimensionItem(models.Model):
    evaluacion = models.ForeignKey(EvaluacionPsicopedagogica, on_delete=models.CASCADE, related_name='items')
    area = models.CharField(max_length=50)
    descripcion = models.TextField()
    valor = models.PositiveSmallIntegerField()

    def __str__(self):
        return f"{self.area} ({self.valor})"


class Subsector(models.Model):
    evaluacion = models.ForeignKey(EvaluacionPsicopedagogica, on_delete=models.CASCADE, related_name='subsectores')
    subsector = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50, choices=[('destacado', 'Destacado'), ('dificultad', 'Dificultad')])

    def __str__(self):
        return f"{self.subsector} ({self.tipo})"


class EstrategiaApoyo(models.Model):
    evaluacion = models.ForeignKey(EvaluacionPsicopedagogica, on_delete=models.CASCADE, related_name='estrategias_apoyo')
    descripcion = models.TextField()
    aplicada = models.BooleanField(default=False)
    exitosa = models.BooleanField(default=False)


class ApoyoAdicional(models.Model):
    evaluacion = models.ForeignKey(EvaluacionPsicopedagogica, on_delete=models.CASCADE, related_name='apoyos_adicionales')
    tipo = models.CharField(max_length=20, choices=[('interno', 'Interno'), ('externo', 'Externo')])
    profesional = models.CharField(max_length=100)
    recibido = models.BooleanField(default=False)

# ================================================================
# 6. EVALUACIÓN DE SALUD
# ================================================================

class EvaluacionSalud(models.Model):
    evaluacion_integral = models.ForeignKey(EvaluacionIntegral, on_delete=models.CASCADE, related_name='evaluacion_salud')
    fecha_evaluacion = models.DateField(blank=True, null=True)
    fecha_reevaluacion = models.DateField(blank=True, null=True)
    motivo_consulta = models.CharField(max_length=255)
    descripcion_diagnostico = models.TextField(blank=True, null=True)
    estado_salud_general = models.TextField(blank=True, null=True)
    indicaciones = models.TextField(blank=True, null=True)
    profesional = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True, related_name='evaluaciones_salud')
    especialidad = models.CharField(max_length=100, blank=True, null=True)
    procedencia = models.CharField(max_length=100, blank=True, null=True)
    contacto = models.CharField(max_length=100, blank=True, null=True)

# ================================================================
# 7. INFORME PARA LA FAMILIA
# ================================================================

class InformeFamilia(models.Model):
    evaluacion_integral = models.ForeignKey(EvaluacionIntegral, on_delete=models.CASCADE, related_name='informes_familia')
    fecha_entrega = models.DateField()
    motivo = models.CharField(max_length=50, choices=[('Ingreso', 'Ingreso'), ('Reevaluación', 'Reevaluación')])
    diagnostico_nee = models.TextField(blank=True, null=True)
    trabajo_colaborativo = models.TextField(blank=True, null=True)
    apoyos_requeridos_hogar = models.TextField(blank=True, null=True)
    acuerdos_compromisos = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Informe Familia de {self.evaluacion_integral.estudiante}"


class InformeFamiliaInstrumento(models.Model):
    informe = models.ForeignKey(InformeFamilia, on_delete=models.CASCADE, related_name='instrumentos')
    nombre = models.CharField(max_length=200)
    fecha_aplicacion = models.DateField(blank=True, null=True)


class InformeFamiliaAmbito(models.Model):
    informe = models.ForeignKey(InformeFamilia, on_delete=models.CASCADE, related_name='ambitos')
    ambito = models.CharField(max_length=30, choices=[('Pedagógico', 'Pedagógico'), ('Social/Afectivo', 'Social/Afectivo')])
    fortalezas = models.TextField(blank=True, null=True)
    necesidades_apoyo = models.TextField(blank=True, null=True)


class InformeFamiliaSeguimiento(models.Model):
    informe = models.ForeignKey(InformeFamilia, on_delete=models.CASCADE, related_name='seguimientos')
    fecha_seguimiento = models.DateField()
    nota = models.TextField(blank=True, null=True)


class InformeFamiliaEntrega(models.Model):
    informe = models.ForeignKey(InformeFamilia, on_delete=models.CASCADE, related_name='entrega')
    profesional = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True, related_name='entregas')
    nombre_identidad = models.CharField(max_length=120, blank=True, null=True)
    rut = models.CharField(max_length=15, blank=True, null=True)
    rol_cargo = models.CharField(max_length=120, blank=True, null=True)
    telefono = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)


class InformeFamiliaReceptor(models.Model):
    informe = models.ForeignKey(InformeFamilia, on_delete=models.CASCADE, related_name='receptores')
    apoderado = models.ForeignKey(Apoderado, on_delete=models.SET_NULL, null=True, blank=True)
    nombre_identidad = models.CharField(max_length=120, blank=True, null=True)
    rut_pasaporte = models.CharField(max_length=20, blank=True, null=True)
    nombre_social = models.CharField(max_length=120, blank=True, null=True)
    telefono = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    relacion = models.CharField(max_length=60, blank=True, null=True)
    es_apoderado_titular = models.BooleanField(default=False)
    es_apoderado_suplente = models.BooleanField(default=False)
    poder_simple = models.BooleanField(default=False)
    en_presencia_de = models.CharField(max_length=200, blank=True, null=True)





class PasswordResetToken(models.Model):
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='tokens_recuperacion'
    )
    token = models.CharField(max_length=64, unique=True, default=uuid.uuid4)
    creado_en = models.DateTimeField(auto_now_add=True)
    expira_en = models.DateTimeField()

    def save(self, *args, **kwargs):
        # Expira automáticamente en 10 minutos si no se define otra fecha
        if not self.expira_en:
            self.expira_en = timezone.now() + timedelta(minutes=10)
        super().save(*args, **kwargs)

    def is_valido(self):
        return timezone.now() < self.expira_en

    def __str__(self):
        return f"Token para {self.usuario.username} - válido hasta {self.expira_en}"






# ================================================================
# REGISTRO PIE – Registro de planificación y evaluación del curso
# ================================================================


class RegistroPIE(models.Model):
    """
    Registro general del Programa de Integración Escolar (PIE) por curso.
    """
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='registros_pie')
    responsable = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True, related_name='registros_pie')
    fecha_creacion = models.DateField(auto_now_add=True)
    periodo = models.CharField(max_length=50, blank=True, null=True, help_text="Ej: Primer semestre, Segundo semestre, etc.")
    observaciones_generales = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Registro PIE - {self.curso.nombre} ({self.periodo or 'Sin periodo'})"


class EquipoAula(models.Model):
    """
    Equipo de aula y profesionales PIE asociados al curso.
    """
    registro = models.ForeignKey(RegistroPIE, on_delete=models.CASCADE, related_name='equipo_aula')
    nombre = models.CharField(max_length=100)
    rol = models.CharField(
        max_length=100,
        choices=[
            ('Profesor Regular', 'Profesor Regular'),
            ('Educador Diferencial', 'Educador Diferencial'),
            ('Psicólogo', 'Psicólogo'),
            ('Fonoaudiólogo', 'Fonoaudiólogo'),
            ('Terapeuta Ocupacional', 'Terapeuta Ocupacional'),
            ('Asistente de Aula', 'Asistente de Aula'),
            ('Coordinador PIE', 'Coordinador PIE'),
            ('Otro', 'Otro')
        ]
    )
    telefono = models.CharField(max_length=50, blank=True, null=True)
    correo = models.EmailField(blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} - {self.rol}"


class PlanificacionPIE(models.Model):
    """
    Planificación general del curso y diagnóstico pedagógico.
    """
    registro = models.OneToOneField(RegistroPIE, on_delete=models.CASCADE, related_name='planificacion')
    descripcion_curso = models.TextField(blank=True, null=True)
    fortalezas = models.TextField(blank=True, null=True)
    necesidades_apoyo = models.TextField(blank=True, null=True)
    estrategias_generales = models.TextField(blank=True, null=True)
    recursos_apoyo = models.TextField(blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Planificación PIE - {self.registro.curso.nombre}"


class TrabajoColaborativo(models.Model):
    """
    Registra instancias de trabajo colaborativo docente y PIE.
    """
    registro = models.ForeignKey(RegistroPIE, on_delete=models.CASCADE, related_name='trabajos_colaborativos')
    fecha = models.DateField(blank=True, null=True)
    tipo = models.CharField(
        max_length=100,
        choices=[
            ('Co-enseñanza', 'Co-enseñanza'),
            ('Planificación compartida', 'Planificación compartida'),
            ('Reunión de equipo', 'Reunión de equipo'),
            ('Trabajo con familia', 'Trabajo con familia'),
            ('Trabajo con comunidad', 'Trabajo con comunidad'),
            ('Otro', 'Otro'),
        ]
    )
    descripcion = models.TextField(blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.tipo} ({self.fecha or 'sin fecha'})"


class ActividadComunidad(models.Model):
    """
    Actividades realizadas con familias o comunidad educativa.
    """
    registro = models.ForeignKey(RegistroPIE, on_delete=models.CASCADE, related_name='actividades_comunidad')
    fecha = models.DateField()
    participantes = models.TextField(blank=True, null=True)
    objetivos = models.TextField(blank=True, null=True)
    resultados = models.TextField(blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Actividad Comunidad ({self.fecha}) - {self.registro.curso.nombre}"


class LogroAprendizaje(models.Model):
    """
    Logros o avances observados en los estudiantes con NEE.
    """
    registro = models.ForeignKey(RegistroPIE, on_delete=models.CASCADE, related_name='logros')
    estudiante = models.ForeignKey(Estudiante, on_delete=models.SET_NULL, null=True, blank=True)
    fecha = models.DateField(blank=True, null=True)
    logros = models.TextField(blank=True, null=True)
    dificultades = models.TextField(blank=True, null=True)
    estrategias_utilizadas = models.TextField(blank=True, null=True)
    comentarios = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Logros {self.estudiante or 'Sin estudiante'} ({self.fecha or 'sin fecha'})"


class EvaluacionPIE(models.Model):
    """
    Evaluación final del proceso PIE en el curso.
    """
    registro = models.OneToOneField(RegistroPIE, on_delete=models.CASCADE, related_name='evaluacion')
    fecha_evaluacion = models.DateField(blank=True, null=True)
    resultados = models.TextField(blank=True, null=True)
    conclusiones = models.TextField(blank=True, null=True)
    proyecciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Evaluación PIE - {self.registro.curso.nombre}"
