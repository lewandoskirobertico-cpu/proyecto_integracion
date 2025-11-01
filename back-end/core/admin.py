from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    Usuario, Especialidad, Curso, Apoderado, Estudiante,
    EvaluacionIntegral, Anamnesis, Informante, Entrevistador, AntecedenteSalud,
    EvaluacionPsicopedagogica, SubdimensionItem, Subsector,
    EstrategiaApoyo, ApoyoAdicional,
    EvaluacionSalud,
    InformeFamilia, InformeFamiliaInstrumento, InformeFamiliaAmbito,
    InformeFamiliaSeguimiento, InformeFamiliaEntrega, InformeFamiliaReceptor
)

# ================================================================
# ADMIN PERSONALIZADO: Usuario (Profesional del sistema)
# ================================================================
@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    model = Usuario
    list_display = ('username', 'email', 'first_name', 'last_name', 'especialidad', 'tipo', 'is_active', 'is_staff')
    list_filter = ('especialidad', 'tipo', 'is_active', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)

    fieldsets = (
        ('Credenciales', {'fields': ('username', 'password')}),
        ('Información personal', {
            'fields': (
                'first_name', 'last_name', 'email', 'telefono', 'establecimiento',
                'tipo', 'especialidad'
            )
        }),
        ('Permisos', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'
            )
        }),
        ('Fechas', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'tipo', 'especialidad', 'is_staff', 'is_active'),
        }),
    )

# ================================================================
# REGISTROS SIMPLES
# ================================================================

modelos_simples = [
    Especialidad,
    Curso,
    Apoderado,
    Estudiante,
    EvaluacionIntegral,
    Anamnesis,
    Informante,
    Entrevistador,
    AntecedenteSalud,
    EvaluacionPsicopedagogica,
    SubdimensionItem,
    Subsector,
    EstrategiaApoyo,
    ApoyoAdicional,
    EvaluacionSalud,
    InformeFamilia,
    InformeFamiliaInstrumento,
    InformeFamiliaAmbito,
    InformeFamiliaSeguimiento,
    InformeFamiliaEntrega,
    InformeFamiliaReceptor,
]

for modelo in modelos_simples:
    try:
        admin.site.register(modelo)
    except admin.sites.AlreadyRegistered:
        pass
