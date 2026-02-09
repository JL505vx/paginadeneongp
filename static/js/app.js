const textInput = document.getElementById("id_texto_letrero");
const tipoNeonInput = document.getElementById("id_tipo_neon");
const materialInput = document.getElementById("id_material");
const tipoProyectoInput = document.getElementById("id_tipo_proyecto");
const tipografiaInput = document.getElementById("id_tipografia");
const detalleInput = document.getElementById("id_nivel_detalle");
const anchoInput = document.getElementById("id_ancho_cm");
const altoInput = document.getElementById("id_alto_cm");
const colorLetrasInput = document.getElementById("id_color_letras");

const previewText = document.getElementById("previewText");
const previewPrice = document.getElementById("previewPrice");
const previewMeters = document.getElementById("previewMeters");

const claseTipografia = {
    script: "font-script",
    bold: "font-bold",
    tech: "font-tech",
    classic: "font-classic",
};

let timerCotizacion = null;

function normalizarColor(valor, respaldo) {
    const txt = String(valor || "").trim();
    if (!txt) return respaldo;
    const hex = /^#([0-9a-fA-F]{3}){1,2}$/;
    const rgb = /^rgb(a)?\(/i;
    const simpleName = /^[a-zA-Z]+$/;
    if (hex.test(txt) || rgb.test(txt) || simpleName.test(txt)) {
        return txt;
    }
    return respaldo;
}

function getCookie(name) {
    const cookieValue = document.cookie
        .split(";")
        .map((cookie) => cookie.trim())
        .find((cookie) => cookie.startsWith(`${name}=`));
    return cookieValue ? decodeURIComponent(cookieValue.split("=")[1]) : "";
}

function actualizarTipografiaPreview() {
    previewText.classList.remove("font-script", "font-bold", "font-tech", "font-classic");
    previewText.classList.add(claseTipografia[tipografiaInput?.value] || "font-script");
}

function actualizarVisualPreview() {
    const texto = (textInput?.value || "Tu idea aqui").trim();
    const colorLetras = normalizarColor(colorLetrasInput?.value, "#ff4fd8");

    previewText.textContent = texto || "Tu idea aqui";
    previewText.style.color = "#ffffff";
    previewText.style.textShadow = `0 0 8px #fff, 0 0 16px #fff, 0 0 28px ${colorLetras}, 0 0 52px ${colorLetras}`;
    actualizarTipografiaPreview();
}

function payloadCotizacion() {
    return {
        texto_letrero: textInput?.value || "",
        tipo_neon: tipoNeonInput?.value || "primera",
        material: materialInput?.value || "acrilico",
        tipo_proyecto: tipoProyectoInput?.value || "texto",
        nivel_detalle: detalleInput?.value || "medio",
        ancho_cm: anchoInput?.value || 60,
        alto_cm: altoInput?.value || 30,
    };
}

async function cotizar() {
    try {
        const response = await fetch("/api/cotizar/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie("csrftoken"),
            },
            body: JSON.stringify(payloadCotizacion()),
        });
        if (!response.ok) {
            return;
        }
        const data = await response.json();
        const precio = Number(data.precio_estimado || 0);
        const metros = Number(data.metros_estimados || 0);
        if (precio > 0) {
            previewPrice.textContent = `$${precio.toLocaleString("es-MX")} MXN`;
        }
        if (metros > 0 && previewMeters) {
            previewMeters.textContent = `${metros.toFixed(2)} m`;
        }
    } catch (error) {
        // Silencioso: si falla el endpoint no se rompe la experiencia.
    }
}

function actualizarTodo() {
    actualizarVisualPreview();
    clearTimeout(timerCotizacion);
    timerCotizacion = setTimeout(cotizar, 220);
}

[
    textInput,
    tipoNeonInput,
    materialInput,
    tipoProyectoInput,
    tipografiaInput,
    detalleInput,
    anchoInput,
    altoInput,
    colorLetrasInput,
].forEach((element) => {
    element?.addEventListener("input", actualizarTodo);
    element?.addEventListener("change", actualizarTodo);
});

actualizarTodo();
