from pathlib import Path
import json
import math
import re
from urllib.parse import quote

from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from .forms import SolicitudDisenoForm


NEON_TIPOS = [
    {
        "clave": "primera",
        "titulo": "Primera Generacion",
        "descripcion": (
            "Ideal para proyectos economicos, decorativos o personales con gran "
            "detalle visual."
        ),
        "estructura": "Acrilico 3mm, PVC 3mm, MDF 5mm",
    },
    {
        "clave": "segunda",
        "titulo": "Segunda Generacion",
        "descripcion": (
            "Enfoque premium para instalaciones comerciales que requieren mayor "
            "durabilidad y uniformidad."
        ),
        "estructura": "Acrilico 10mm, PVC 10mm, MDF 6mm",
    },
    {
        "clave": "pixel",
        "titulo": "Neon Pixel",
        "descripcion": "Estilo grafico por segmentos, ideal para conceptos modernos.",
        "estructura": "Base de Primera Generacion",
    },
    {
        "clave": "rayo",
        "titulo": "Neon Rayo",
        "descripcion": "Mayor impacto visual para conceptos llamativos y contrastantes.",
        "estructura": "Base de Primera Generacion",
    },
    {
        "clave": "rgb",
        "titulo": "Neon RGB",
        "descripcion": "Cambio de color para experiencias dinamicas en interior o evento.",
        "estructura": "Disponible en Primera y Segunda Generacion",
    },
]

MATERIALES_INFO = [
    {
        "nombre": "MDF",
        "descripcion": "Madera procesada rigida para fondos, paneles y bases decorativas.",
        "calibres": "1ra gen: 5mm | 2da gen: 6mm",
        "uso": "Proyectos de interior con excelente costo-beneficio.",
    },
    {
        "nombre": "PVC",
        "descripcion": "Material ligero y limpio, facil de mantener y con buena resistencia.",
        "calibres": "1ra gen: 3mm | 2da gen: 10mm",
        "uso": "Locales y espacios con polvo o humedad moderada.",
    },
    {
        "nombre": "Acrilico",
        "descripcion": "Acabado premium, alta presencia visual y gran calidad de exhibicion.",
        "calibres": "1ra gen: 3mm | 2da gen: 10mm",
        "uso": "Marcas de alto impacto, fachadas y piezas protagonistas.",
    },
]

ASESORIA_PUNTOS = [
    "Analisis del espacio antes de fabricar.",
    "Recomendacion de tipo de neon segun uso real.",
    "Ajuste de diseno para legibilidad y recordacion.",
    "Sugerencia de materiales para mayor durabilidad.",
    "Acompanamiento por WhatsApp durante todo el proceso.",
]

FAQS = [
    {
        "pregunta": "Como se calcula el precio aproximado?",
        "respuesta": (
            "Tomamos en cuenta tamano, tipo de neon, complejidad del diseno y tiempos de "
            "fabricacion."
        ),
    },
    {
        "pregunta": "En cuanto tiempo entregan normalmente?",
        "respuesta": (
            "El tiempo promedio de entrega es de 1 semana. Proyectos con mayor "
            "complejidad pueden requerir tiempo adicional."
        ),
    },
    {
        "pregunta": "Es igual cotizar texto que una figura detallada?",
        "respuesta": (
            "No. Un logo complejo o una ilustracion detallada requiere mas trabajo que "
            "una frase simple."
        ),
    },
    {
        "pregunta": "Puedo elegir tipografia y color?",
        "respuesta": "Si. Puedes personalizar la tipografia y el color de letras en tiempo real.",
    },
]

PRICING_RULES = {
    "base_m2": {
        "primera": 714,
        "pixel": 714,
        "rayo": 714,
        "rgb": 714,
        "segunda": 1468,
    },
    "material_factor": {"acrilico": 1.0, "pvc": 0.87, "mdf": 0.82},
    "neon_factor": {"primera": 1.0, "pixel": 1.12, "rayo": 1.16, "rgb": 1.25, "segunda": 1.35},
    "project_factor": {"texto": 1.0, "texto_figura": 1.3, "logo": 1.6},
    "detail_factor": {"bajo": 1.0, "medio": 1.2, "alto": 1.45},
    "keywords_complex": ("spiderman", "personaje", "logo", "detallado", "calavera", "mascota"),
    "keywords_medium": ("michelada", "vaso", "botella", "coctel", "bar"),
    "neon_meter_cost": 190,
    "supplies_meter_cost": 65,
    "supplies_fixed": 220,
    "profit_factor": 1.8,
}

_GALERIA_TITULOS = [
    "Unicornio Neon Multicolor",
    "Startup 360 con Foco",
    "Figura Minimal Neon",
    "Letrero Soy Deire",
    "Calavera Pirate Neon",
    "Sistema Chat Neon",
    "Botella Gym Neon",
]


def _limpiar_nombre_archivo(nombre):
    texto = re.sub(r"whatsapp image \d{4} \d{2} \d{2} at ", "", nombre, flags=re.I)
    texto = re.sub(r"\(\d+\)", "", texto)
    texto = re.sub(r"\d+\.\d+\.\d+ [ap]m", "", texto, flags=re.I)
    texto = re.sub(r"\s+", " ", texto).strip(" -_")
    return texto


def _galeria_desde_media():
    imagenes = []
    base = Path(settings.MEDIA_ROOT)
    if not base.exists():
        return imagenes

    archivos = sorted(base.glob("*"))
    idx_imagen = 0
    for archivo in archivos:
        if archivo.suffix.lower() not in {".jpg", ".jpeg", ".png", ".webp"}:
            continue
        nombre_auto = _limpiar_nombre_archivo(archivo.stem)
        titulo = _GALERIA_TITULOS[idx_imagen] if idx_imagen < len(_GALERIA_TITULOS) else ""
        nombre = titulo or nombre_auto or f"Proyecto Neon {idx_imagen + 1:02d}"
        url = f"{settings.MEDIA_URL}{quote(archivo.name)}"
        imagenes.append({"titulo": nombre, "url": url})
        idx_imagen += 1
    return imagenes


def _keyword_complexity_factor(texto):
    texto_normal = (texto or "").lower()
    if any(k in texto_normal for k in PRICING_RULES["keywords_complex"]):
        return 1.3
    if any(k in texto_normal for k in PRICING_RULES["keywords_medium"]):
        return 1.15
    return 1.0


def _estimate_price(payload):
    tipo_neon = payload.get("tipo_neon", "primera")
    material = payload.get("material", "acrilico")
    tipo_proyecto = payload.get("tipo_proyecto", "texto")
    nivel_detalle = payload.get("nivel_detalle", "medio")
    texto = payload.get("texto_letrero", "")

    try:
        ancho_cm = int(payload.get("ancho_cm", 60) or 60)
    except (TypeError, ValueError):
        ancho_cm = 60
    try:
        alto_cm = int(payload.get("alto_cm", 30) or 30)
    except (TypeError, ValueError):
        alto_cm = 30

    ancho_cm = max(ancho_cm, 20)
    alto_cm = max(alto_cm, 10)

    area_m2 = (ancho_cm / 100) * (alto_cm / 100)
    base_m2 = PRICING_RULES["base_m2"].get(tipo_neon, 714)
    material_factor = PRICING_RULES["material_factor"].get(material, 1.0)
    neon_factor = PRICING_RULES["neon_factor"].get(tipo_neon, 1.0)
    project_factor = PRICING_RULES["project_factor"].get(tipo_proyecto, 1.0)
    detail_factor = PRICING_RULES["detail_factor"].get(nivel_detalle, 1.2)
    text_factor = _keyword_complexity_factor(texto)

    base_text = max(len(texto.strip()), 3) * 0.11
    area_factor = area_m2 * 1.8
    neon_meters = max((base_text + area_factor) * project_factor * detail_factor * text_factor, 1.8)

    fabrication_cost = area_m2 * base_m2 * material_factor
    neon_cost = neon_meters * PRICING_RULES["neon_meter_cost"] * neon_factor
    supplies_cost = (neon_meters * PRICING_RULES["supplies_meter_cost"]) + PRICING_RULES["supplies_fixed"]

    production_cost = fabrication_cost + neon_cost + supplies_cost
    sale_price = math.ceil(production_cost * PRICING_RULES["profit_factor"])
    rounded_price = int(round(sale_price / 10.0) * 10)
    return {
        "precio_estimado": max(rounded_price, 650),
        "metros_estimados": round(neon_meters, 2),
    }


def inicio(request):
    form = SolicitudDisenoForm()

    if request.method == "POST":
        form = SolicitudDisenoForm(request.POST)
        if form.is_valid():
            solicitud = form.save()
            messages.success(request, "Solicitud enviada. Te contactaremos por WhatsApp.")
            return redirect(f"/?ok={solicitud.id}#disenador")
        messages.error(request, "Revisa el formulario. Hay campos pendientes.")

    galeria = _galeria_desde_media()
    hero_bg = galeria[0]["url"] if galeria else ""
    parallax_bg = galeria[1]["url"] if len(galeria) > 1 else hero_bg

    contexto = {
        "empresa": "LetrerosGP",
        "telefono_whatsapp": "529222275962",
        "telefono_legible": "922 227 5962",
        "neon_tipos": NEON_TIPOS,
        "materiales_info": MATERIALES_INFO,
        "asesoria_puntos": ASESORIA_PUNTOS,
        "faqs": FAQS,
        "galeria": galeria,
        "hero_bg": hero_bg,
        "parallax_bg": parallax_bg,
        "form": form,
    }
    return render(request, "letreros/inicio.html", contexto)


@require_POST
def cotizar_api(request):
    try:
        payload = json.loads(request.body.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({"error": "Solicitud invalida"}, status=400)

    resultado = _estimate_price(payload)
    return JsonResponse(resultado)
