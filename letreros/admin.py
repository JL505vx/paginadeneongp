from django.contrib import admin

from .models import SolicitudDiseno


@admin.register(SolicitudDiseno)
class SolicitudDisenoAdmin(admin.ModelAdmin):
    list_display = (
        "nombre",
        "whatsapp",
        "tipo_neon",
        "material",
        "tipo_proyecto",
        "nivel_detalle",
        "creado_en",
    )
    list_filter = ("tipo_neon", "material", "tipo_proyecto", "nivel_detalle", "creado_en")
    search_fields = ("nombre", "whatsapp", "texto_letrero", "correo")
