from django.db import models


class SolicitudDiseno(models.Model):
    TIPO_NEON_CHOICES = [
        ("primera", "Primera Generacion"),
        ("segunda", "Segunda Generacion"),
        ("pixel", "Neon Pixel"),
        ("rayo", "Neon Rayo"),
        ("rgb", "Neon RGB"),
    ]

    MATERIAL_CHOICES = [
        ("mdf", "MDF"),
        ("pvc", "PVC"),
        ("acrilico", "Acrilico"),
    ]
    TIPO_PROYECTO_CHOICES = [
        ("texto", "Solo texto"),
        ("texto_figura", "Texto + figura"),
        ("logo", "Logo o ilustracion detallada"),
    ]
    TIPOGRAFIA_CHOICES = [
        ("script", "Script fluida"),
        ("bold", "Bloque gruesa"),
        ("tech", "Tecnica futurista"),
        ("classic", "Clasica limpia"),
    ]
    DETALLE_CHOICES = [
        ("bajo", "Bajo"),
        ("medio", "Medio"),
        ("alto", "Alto"),
    ]

    nombre = models.CharField(max_length=120)
    whatsapp = models.CharField(max_length=30)
    correo = models.EmailField(blank=True)
    texto_letrero = models.CharField(max_length=140)
    tipo_neon = models.CharField(max_length=20, choices=TIPO_NEON_CHOICES)
    material = models.CharField(max_length=20, choices=MATERIAL_CHOICES)
    tipo_proyecto = models.CharField(
        max_length=20, choices=TIPO_PROYECTO_CHOICES, default="texto"
    )
    tipografia = models.CharField(
        max_length=20, choices=TIPOGRAFIA_CHOICES, default="script"
    )
    nivel_detalle = models.CharField(
        max_length=20, choices=DETALLE_CHOICES, default="medio"
    )
    ancho_cm = models.PositiveIntegerField(default=60)
    alto_cm = models.PositiveIntegerField(default=30)
    color_letras = models.CharField(max_length=20, default="#ff4fd8")
    mensaje = models.TextField(blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-creado_en"]

    def __str__(self):
        return f"{self.nombre} - {self.texto_letrero}"
