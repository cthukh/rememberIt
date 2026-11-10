// Recepción: buscar visitas del día y marcar ingreso y salida

// Estados de una visita: "programada", "dentro" y "finalizada"

// Elementos de la página
var listaVisitas = document.getElementById("lista-visitas");
var buscador = document.getElementById("buscador");
var chips = document.querySelectorAll(".chip");
var contador = document.getElementById("contador");
var sinResultados = document.getElementById("sin-resultados");

var relojHora = document.getElementById("reloj-hora");
var relojFecha = document.getElementById("reloj-fecha");

var resTotal = document.getElementById("res-total");
var resProgramadas = document.getElementById("res-programadas");
var resDentro = document.getElementById("res-dentro");
var resFinalizadas = document.getElementById("res-finalizadas");

var estadoActual = "";

// ---------- Horas ----------

// Devuelve una hora como HH:MM:SS
function horaTexto(fecha) {
    var h = String(fecha.getHours()).padStart(2, "0");
    var m = String(fecha.getMinutes()).padStart(2, "0");
    var s = String(fecha.getSeconds()).padStart(2, "0");
    return h + ":" + m + ":" + s;
}

// Devuelve una fecha de hace "minutos" minutos
function haceMinutos(minutos) {
    return new Date(new Date().getTime() - minutos * 60 * 1000);
}

// Cuánto tiempo estuvo la visita (ej: "25 min" o "1 h 05 min")
function duracion(entrada, salida) {
    var minutos = Math.floor((salida - entrada) / 60000);
    if (minutos < 1) {
        return "menos de 1 min";
    }
    if (minutos < 60) {
        return minutos + " min";
    }
    var h = Math.floor(minutos / 60);
    var m = String(minutos % 60).padStart(2, "0");
    return h + " h " + m + " min";
}

// ---------- Datos de ejemplo (después vendrán de la base de datos) ----------
var visitas = [
    { nombre: "Carla Muñoz Díaz", rut: "15.234.567-8", parentesco: "Hijo/a", residente: "Rosa Muñoz", bloque: "10:00 - 11:00", estado: "finalizada", ingreso: haceMinutos(95), salida: haceMinutos(40) },
    { nombre: "Lucía Vega Rojas", rut: "17.111.222-3", parentesco: "Nieto/a", residente: "Marta Vega", bloque: "10:00 - 11:00", estado: "dentro", ingreso: haceMinutos(25), salida: null },
    { nombre: "Pedro Soto Vera", rut: "9.876.543-2", parentesco: "Hijo/a", residente: "Luis Soto", bloque: "11:00 - 12:00", estado: "programada", ingreso: null, salida: null },
    { nombre: "Jorge Muñoz Paz", rut: "12.222.333-4", parentesco: "Hermano/a", residente: "Rosa Muñoz", bloque: "15:00 - 16:00", estado: "programada", ingreso: null, salida: null },
    { nombre: "Ana Soto Mena", rut: "11.333.444-5", parentesco: "Cónyuge", residente: "Luis Soto", bloque: "15:00 - 16:00", estado: "programada", ingreso: null, salida: null },
    { nombre: "Paula Vega Núñez", rut: "16.444.555-6", parentesco: "Hijo/a", residente: "Marta Vega", bloque: "16:00 - 17:00", estado: "programada", ingreso: null, salida: null },
    { nombre: "Dr. Felipe Araya", rut: "14.555.666-K", parentesco: "Visita profesional", residente: "Luis Soto", bloque: "16:00 - 17:00", estado: "programada", ingreso: null, salida: null }
];

// ---------- Buscador ----------

// Quita tildes y pasa a minúsculas ("Muñoz" -> "munoz")
function normalizar(texto) {
    return texto.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase().trim();
}

// Quita puntos, guion y espacios ("15.234.567-8" -> "152345678")
function limpiarRut(texto) {
    return texto.replace(/[.\-\s]/g, "").toLowerCase();
}

// Dice si la visita coincide con lo que se escribió y con el estado elegido
function coincide(v) {
    if (estadoActual !== "" && v.estado !== estadoActual) {
        return false;
    }

    var q = normalizar(buscador.value);
    if (q === "") {
        return true;
    }

    var porNombre = normalizar(v.nombre).indexOf(q) !== -1;
    var qRut = limpiarRut(q);
    var porRut = qRut !== "" && limpiarRut(v.rut).indexOf(qRut) !== -1;

    return porNombre || porRut;
}

// ---------- Mostrar en pantalla ----------

function textoEstado(estado) {
    if (estado === "programada") {
        return "Por llegar";
    }
    if (estado === "dentro") {
        return "Dentro";
    }
    return "Finalizada";
}

// Crea un texto pequeño con título y valor (ej: "Ingreso" / "10:32:05")
function crearDato(titulo, valor) {
    var caja = document.createElement("div");
    caja.className = "dato";
    var t = document.createElement("span");
    t.className = "dato-titulo";
    t.textContent = titulo;
    var v = document.createElement("strong");
    v.textContent = valor;
    caja.appendChild(t);
    caja.appendChild(v);
    return caja;
}

// Crea la tarjeta de una visita
function crearTarjeta(v) {
    var item = document.createElement("li");
    item.className = "visita visita-" + v.estado;

    // Bloque horario
    var bloque = document.createElement("div");
    bloque.className = "visita-bloque";
    var bloqueTitulo = document.createElement("span");
    bloqueTitulo.textContent = "Bloque";
    var bloqueHora = document.createElement("strong");
    bloqueHora.textContent = v.bloque;
    bloque.appendChild(bloqueTitulo);
    bloque.appendChild(bloqueHora);

    // Datos del visitante
    var info = document.createElement("div");
    info.className = "visita-info";

    var nombre = document.createElement("h3");
    nombre.textContent = v.nombre;

    var rut = document.createElement("p");
    rut.className = "visita-rut";
    rut.textContent = "RUT " + v.rut + " · " + v.parentesco;

    var residente = document.createElement("p");
    residente.className = "visita-residente";
    residente.textContent = "Visita a " + v.residente;

    var estado = document.createElement("span");
    estado.className = "estado estado-" + v.estado;
    estado.textContent = textoEstado(v.estado);

    info.appendChild(nombre);
    info.appendChild(rut);
    info.appendChild(residente);
    info.appendChild(estado);

    // Horas registradas
    var horas = document.createElement("div");
    horas.className = "visita-horas";
    if (v.ingreso !== null) {
        horas.appendChild(crearDato("Ingreso", horaTexto(v.ingreso)));
    }
    if (v.salida !== null) {
        horas.appendChild(crearDato("Salida", horaTexto(v.salida)));
        horas.appendChild(crearDato("Permanencia", duracion(v.ingreso, v.salida)));
    }

    // Botón de acción
    var accion = document.createElement("div");
    accion.className = "visita-accion";

    if (v.estado === "programada") {
        var botonIngreso = document.createElement("button");
        botonIngreso.type = "button";
        botonIngreso.className = "btn-accion btn-ingreso";
        botonIngreso.textContent = "Marcar ingreso";
        botonIngreso.setAttribute("aria-label", "Marcar ingreso de " + v.nombre);
        botonIngreso.addEventListener("click", function () {
            marcarIngreso(v);
        });
        accion.appendChild(botonIngreso);
    } else if (v.estado === "dentro") {
        var botonSalida = document.createElement("button");
        botonSalida.type = "button";
        botonSalida.className = "btn-accion btn-salida";
        botonSalida.textContent = "Marcar salida";
        botonSalida.setAttribute("aria-label", "Marcar salida de " + v.nombre);
        botonSalida.addEventListener("click", function () {
            marcarSalida(v);
        });
        accion.appendChild(botonSalida);
    } else {
        var cerrada = document.createElement("span");
        cerrada.className = "visita-cerrada";
        cerrada.textContent = "Visita cerrada";
        accion.appendChild(cerrada);
    }

    item.appendChild(bloque);
    item.appendChild(info);
    item.appendChild(horas);
    item.appendChild(accion);
    return item;
}

// Dibuja la lista, los contadores y el mensaje de "sin resultados"
function mostrar() {
    listaVisitas.innerHTML = "";
    var mostradas = 0;

    for (var i = 0; i < visitas.length; i++) {
        if (coincide(visitas[i])) {
            listaVisitas.appendChild(crearTarjeta(visitas[i]));
            mostradas++;
        }
    }

    // Resumen (cuenta todas las visitas del día)
    var programadas = 0;
    var dentro = 0;
    var finalizadas = 0;
    for (var j = 0; j < visitas.length; j++) {
        if (visitas[j].estado === "programada") {
            programadas++;
        } else if (visitas[j].estado === "dentro") {
            dentro++;
        } else {
            finalizadas++;
        }
    }
    resTotal.textContent = visitas.length;
    resProgramadas.textContent = programadas;
    resDentro.textContent = dentro;
    resFinalizadas.textContent = finalizadas;

    contador.textContent = "Mostrando " + mostradas + " de " + visitas.length + " visitas";
    sinResultados.hidden = mostradas !== 0;
}

// ---------- Acciones ----------

// Registra la hora exacta de entrada
function marcarIngreso(v) {
    v.ingreso = new Date();
    v.estado = "dentro";
    mostrar();
}

// Registra la hora exacta de salida y cierra la visita
function marcarSalida(v) {
    v.salida = new Date();
    v.estado = "finalizada";
    mostrar();
}

// ---------- Reloj ----------
function actualizarReloj() {
    var ahora = new Date();
    relojHora.textContent = horaTexto(ahora);
    relojFecha.textContent = ahora.toLocaleDateString("es-CL", {
        weekday: "long",
        day: "numeric",
        month: "long",
        year: "numeric"
    });
}

// ---------- Eventos ----------
buscador.addEventListener("input", mostrar);

for (var i = 0; i < chips.length; i++) {
    chips[i].addEventListener("click", function () {
        for (var j = 0; j < chips.length; j++) {
            chips[j].classList.remove("chip-activo");
        }
        this.classList.add("chip-activo");
        estadoActual = this.dataset.estado;
        mostrar();
    });
}

// ---------- Al cargar la página ----------
actualizarReloj();
setInterval(actualizarReloj, 1000);
mostrar();