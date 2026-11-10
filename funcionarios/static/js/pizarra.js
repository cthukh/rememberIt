// Pizarra digital: publicar, desactivar y eliminar avisos

var formAviso = document.getElementById("form-aviso");
var inputTitulo = document.getElementById("aviso-titulo");
var inputMensaje = document.getElementById("aviso-mensaje");
var selVigencia = document.getElementById("aviso-vigencia");
var contadorMensaje = document.getElementById("contador-mensaje");

var listaActivos = document.getElementById("lista-activos");
var listaInactivos = document.getElementById("lista-inactivos");
var contadorActivos = document.getElementById("contador-activos");
var sinActivos = document.getElementById("sin-activos");
var sinInactivos = document.getElementById("sin-inactivos");
var plantilla = document.getElementById("plantilla-aviso");

// Escribe cuándo vence el aviso (ej: "Vence 10/11 a las 15:00")
function textoVencimiento(fecha) {
    var dia = String(fecha.getDate()).padStart(2, "0");
    var mes = String(fecha.getMonth() + 1).padStart(2, "0");
    var hora = String(fecha.getHours()).padStart(2, "0");
    var min = String(fecha.getMinutes()).padStart(2, "0");
    return "Vence " + dia + "/" + mes + " a las " + hora + ":" + min;
}

// Guarda la fecha de vencimiento dentro del aviso
function ponerVencimiento(aviso, horas) {
    var vence = new Date().getTime() + horas * 60 * 60 * 1000;
    aviso.dataset.vence = vence;
    aviso.querySelector(".aviso-vence").textContent = textoVencimiento(new Date(vence));
}

// Actualiza los contadores y los mensajes de "vacío"
function actualizar() {
    var activos = listaActivos.children.length;
    var inactivos = listaInactivos.children.length;

    if (activos === 1) {
        contadorActivos.textContent = "1 aviso";
    } else {
        contadorActivos.textContent = activos + " avisos";
    }

    sinActivos.hidden = activos !== 0;
    sinInactivos.hidden = inactivos !== 0;
}

// Pasa un aviso a la lista de desactivados
function desactivar(aviso, vencido) {
    aviso.classList.add("aviso-inactivo");
    aviso.querySelector(".btn-desactivar").remove();
    if (vencido) {
        aviso.querySelector(".aviso-vence").textContent = "Vencido";
    } else {
        aviso.querySelector(".aviso-vence").textContent = "Desactivado";
    }
    listaInactivos.appendChild(aviso);
    actualizar();
}

// Elimina un aviso para siempre
function eliminar(aviso) {
    aviso.remove();
    actualizar();
}

// Revisa si algún aviso activo ya venció
function revisarVencidos() {
    var ahora = new Date().getTime();
    var avisos = Array.from(listaActivos.children);

    for (var i = 0; i < avisos.length; i++) {
        if (Number(avisos[i].dataset.vence) <= ahora) {
            desactivar(avisos[i], true);
        }
    }
}

// Botones de Desactivar y Eliminar (sirven para todos los avisos)
document.addEventListener("click", function (e) {
    var aviso = e.target.closest(".aviso");
    if (aviso === null) {
        return;
    }
    if (e.target.classList.contains("btn-desactivar")) {
        desactivar(aviso, false);
    }
    if (e.target.classList.contains("btn-eliminar")) {
        if (confirm("¿Eliminar este aviso?")) {
            eliminar(aviso);
        }
    }
});

// Contador de caracteres del mensaje
inputMensaje.addEventListener("input", function () {
    contadorMensaje.textContent = inputMensaje.value.length;
});

// Publicar un aviso nuevo
formAviso.addEventListener("submit", function (e) {
    e.preventDefault();

    var titulo = inputTitulo.value.trim();
    var mensaje = inputMensaje.value.trim();

    // Validación sencilla
    inputTitulo.classList.toggle("is-invalid", titulo === "");
    inputMensaje.classList.toggle("is-invalid", mensaje === "");
    if (titulo === "" || mensaje === "") {
        return;
    }

    // Se copia la plantilla y se llenan los datos
    var aviso = plantilla.content.firstElementChild.cloneNode(true);
    aviso.querySelector(".aviso-titulo").textContent = titulo;
    aviso.querySelector(".aviso-mensaje").textContent = mensaje;
    ponerVencimiento(aviso, Number(selVigencia.value));

    listaActivos.prepend(aviso);
    actualizar();

    formAviso.reset();
    contadorMensaje.textContent = "0";
});

// Al cargar: los avisos de ejemplo reciben su fecha de vencimiento
var ejemplos = listaActivos.children;
for (var i = 0; i < ejemplos.length; i++) {
    ponerVencimiento(ejemplos[i], Number(ejemplos[i].dataset.venceHoras));
}
actualizar();

// Cada 30 segundos se revisa si algún aviso venció
setInterval(revisarVencidos, 30000);