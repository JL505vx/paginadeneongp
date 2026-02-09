# LetrerosGP - Sitio Web Dinamico (Django)

Sitio web profesional para LetrerosGP, construido con Django, enfocado en:
- mostrar portafolio real,
- explicar tipos de neon y materiales,
- ofrecer asesoria personalizada,
- permitir diseno/cotizacion rapida desde la web.

## Stack
- Python 3.11
- Django 5.2.6
- SQLite (actual)
- HTML + CSS + JavaScript

## Funcionalidades Actuales
- Home totalmente redisenado (hero, asesoria, parallax, galeria, tipos, materiales, FAQ).
- Galeria automatica desde carpeta `imagenes/`.
- Titulos de galeria limpios (sin nombres tipo descarga).
- Disenador de letrero con:
  - texto del letrero,
  - tipo de neon,
  - material base,
  - tipo de proyecto,
  - tipografia,
  - nivel de detalle,
  - ancho y alto,
  - selector real de color de letras (`input type="color"`).
- Vista previa en vivo del texto con tipografia y color.
- Cotizacion por API backend (`/api/cotizar/`) sin exponer costos internos en frontend.
- Resultado visible para cliente:
  - precio estimado,
  - metros estimados de neon.
- Envio de solicitud a BD (modelo `SolicitudDiseno`).
- Contacto directo por WhatsApp: `9222275962`.

## Ejecutar Local
1. Instalar dependencias:
```bash
pip install -r requirements.txt
```
2. Migraciones:
```bash
python manage.py migrate
```
3. Servidor en puerto `8023`:
```bash
python manage.py runserver 8023
```
4. Abrir:
`http://127.0.0.1:8023/`

## Rutas Principales
- `/` -> pagina principal.
- `/api/cotizar/` -> endpoint POST para cotizacion dinamica.
- `/admin/` -> panel Django admin.

## Estructura Clave
- `core/settings.py` -> configuracion general.
- `core/urls.py` -> rutas globales.
- `letreros/models.py` -> modelo de solicitudes.
- `letreros/forms.py` -> formulario del disenador.
- `letreros/views.py` -> logica del sitio y cotizador.
- `letreros/urls.py` -> rutas de app.
- `templates/letreros/inicio.html` -> template principal.
- `static/css/styles.css` -> estilos.
- `static/js/app.js` -> preview + llamada API cotizacion.
- `DOCUMENTACION_TECNICA.md` -> documentacion tecnica detallada.

## Base de Datos Futura
Para migrar a PostgreSQL o SQL Server:
1. Cambiar `DATABASES` en `core/settings.py`.
2. Ejecutar:
```bash
python manage.py migrate
```

## Deploy en Render
Usa un servicio `Web Service` (Python) y configura:

- `Build Command`:
```bash
bash build.sh
```
- `Start Command`:
```bash
gunicorn core.wsgi:application
```

Variables de entorno recomendadas en Render:
- `SECRET_KEY` = clave segura de Django.
- `DEBUG` = `False`
- `ALLOWED_HOSTS` = `tu-app.onrender.com`
- `CSRF_TRUSTED_ORIGINS` = `https://tu-app.onrender.com`

Opcional para PostgreSQL en Render:
- `DATABASE_URL` = se autoconfigura al conectar una Postgres instance.
