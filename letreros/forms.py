from django import forms

from .models import SolicitudDiseno


class SolicitudDisenoForm(forms.ModelForm):
    class Meta:
        model = SolicitudDiseno
        fields = [
            "nombre",
            "whatsapp",
            "correo",
            "texto_letrero",
            "tipo_neon",
            "material",
            "tipo_proyecto",
            "tipografia",
            "nivel_detalle",
            "ancho_cm",
            "alto_cm",
            "color_letras",
            "mensaje",
        ]
        widgets = {
            "nombre": forms.TextInput(attrs={"placeholder": "Tu nombre"}),
            "whatsapp": forms.TextInput(attrs={"placeholder": "Ej. 9222275962"}),
            "correo": forms.EmailInput(attrs={"placeholder": "correo@ejemplo.com"}),
            "texto_letrero": forms.TextInput(attrs={"placeholder": "Ej. Micheladas La 22"}),
            "color_letras": forms.TextInput(attrs={"type": "color"}),
            "mensaje": forms.Textarea(attrs={"rows": 4}),
        }
