# Documentacion Tecnica - LetrerosGP

## 1. Objetivo del Sistema
Este proyecto implementa una web dinamica para LetrerosGP con 4 objetivos:
- exhibir trabajos reales de neon,
- educar al cliente sobre opciones tecnicas (tipos y materiales),
- captar clientes con formulario y WhatsApp,
- entregar cotizacion rapida sin exponer costos internos del negocio.

## 2. Arquitectura General
- Backend: Django (vistas por funcion).
- Frontend: template Django + CSS + JS vanilla.
- Persistencia: SQLite (migrable a PostgreSQL/SQL Server).
- Media: carpeta local `imagenes/` servida en desarrollo.

Flujo:
1. Usuario abre `/`.
2. Django renderiza `inicio.html` con datos de galeria, tipos, materiales, FAQ y formulario.
3. JS actualiza la vista previa del letrero en tiempo real.
4. JS consulta `/api/cotizar/` para precio y metros estimados.
5. Al enviar formulario, Django guarda `SolicitudDiseno`.

## 3. Estructura de Archivos Clave
- `core/settings.py`: configuracion global, static/media y DB.
- `core/urls.py`: enrutamiento principal.
- `letreros/urls.py`: rutas app (`/` y `/api/cotizar/`).
- `letreros/models.py`: modelo de solicitudes.
- `letreros/forms.py`: `SolicitudDisenoForm`.
- `letreros/views.py`: logica de contenido + cotizador.
- `templates/letreros/inicio.html`: layout completo del sitio.
- `static/css/styles.css`: sistema visual y responsive.
- `static/js/app.js`: preview + API quote.

## 4. Modelo de Datos
Archivo: `letreros/models.py`

Modelo `SolicitudDiseno`:
- Contacto: `nombre`, `whatsapp`, `correo`.
- Diseno: `texto_letrero`, `tipo_neon`, `material`, `tipo_proyecto`, `tipografia`, `nivel_detalle`.
- Medidas: `ancho_cm`, `alto_cm`.
- Apariencia: `color_letras`.
- Contexto: `mensaje`, `creado_en`.

`Meta.ordering = ["-creado_en"]` para mostrar primero solicitudes recientes.

## 5. Catalogos y Contenido Dinamico
Archivo: `letreros/views.py`

Estructuras principales:
- `NEON_TIPOS`: descripcion comercial + estructura tecnica por tipo.
- `MATERIALES_INFO`: propiedades de MDF, PVC y Acrilico.
- `ASESORIA_PUNTOS`: bullets de asesoria personalizada.
- `FAQS`: preguntas/respuestas visibles al cliente.

## 6. Galeria Dinamica
Funciones:
- `_limpiar_nombre_archivo(nombre)`: limpia patrones de nombres exportados de WhatsApp.
- `_galeria_desde_media()`: recorre `MEDIA_ROOT`, filtra imagenes validas, asigna titulos comerciales y construye URL.

Entradas permitidas:
- `.jpg`, `.jpeg`, `.png`, `.webp`

## 7. Cotizador (Backend)
Endpoint:
- `POST /api/cotizar/`

Respuesta JSON:
- `precio_estimado` (MXN)
- `metros_estimados` (metros lineales de neon estimados)

Reglas:
- Parametros de entrada: tipo neon, material, tipo proyecto, detalle, ancho, alto, texto.
- Ajuste por complejidad segun keywords.
- Costo interno calculado en backend.
- Frontend solo recibe resultado final.

Funciones:
- `_keyword_complexity_factor(texto)`
- `_estimate_price(payload)`
- `cotizar_api(request)`

## 8. Vista Principal
Funcion: `inicio(request)`

Responsabilidades:
- Manejar GET/POST del formulario.
- Guardar solicitud valida.
- Exponer contexto para:
  - hero background,
  - parallax background,
  - secciones de contenido.

Template:
- `templates/letreros/inicio.html`

Secciones:
- Topbar + Header
- Hero
- Asesoria personalizada
- Galeria
- Parallax con fondo en movimiento
- Tipos y materiales
- Disenador (preview + formulario)
- FAQ
- Boton flotante WhatsApp

## 9. Frontend JS
Archivo: `static/js/app.js`

Responsabilidades:
- Leer inputs del formulario.
- Aplicar tipografia y color a preview.
- Construir payload de cotizacion.
- Llamar API `/api/cotizar/` con CSRF token.
- Pintar `precio_estimado` y `metros_estimados`.

Funciones:
- `normalizarColor`
- `getCookie`
- `actualizarTipografiaPreview`
- `actualizarVisualPreview`
- `payloadCotizacion`
- `cotizar`
- `actualizarTodo`

## 10. Estilos y UX
Archivo: `static/css/styles.css`

Incluye:
- sistema de color con variables CSS,
- layout por secciones,
- hero/parallax con animacion,
- cards y grids para contenido,
- diseno responsive para tablet/movil,
- estilos de formulario y mensajes de estado.

## 11. Operacion y Comandos
Instalacion:
```bash
pip install -r requirements.txt
```

Migraciones:
```bash
python manage.py makemigrations
python manage.py migrate
```

Verificacion:
```bash
python manage.py check
python manage.py test
```

Ejecucion:
```bash
python manage.py runserver 8023
```

## 12. Migracion de Base de Datos
Para pasar de SQLite a PostgreSQL/SQL Server:
1. Actualizar `DATABASES` en `core/settings.py`.
2. Instalar driver correspondiente.
3. Ejecutar `python manage.py migrate`.

## 13. Notas de Seguridad y Producto
- El cliente no ve desglose interno de costos de produccion.
- La cotizacion mostrada es orientativa.
- El precio final se valida por asesoria en WhatsApp.
