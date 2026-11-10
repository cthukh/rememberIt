// Agenda de visitas: validar datos, controlar cupos y mostrar la agenda

// Máximo de visitas al mismo tiempo en un bloque
var LIMITE = 3;

var BLOQUES = [
    "10:00 - 11:00",
    "11:00 - 12:00",
    "15:00 - 16:00",
    "16:00 - 17:00",
    "17:00 - 18:00"
];

// Elementos de la página
var form = document.getElementById("form-visita");
var selResidente = document.getElementById("visita-residente");
var inputNombre = document.getElementById("visita-nombre");
var inputRut = document.getElementById("visita-rut");
var inputTelefono = document.getElementById("visita-telefono");
var selParentesco = document.getElementById("visita-parentesco");
var inputFecha = document.getElementById("visita-fecha");
var selBloque = document.getElementById("visita-bloque");
var mensaje = document.getElementById("mensaje");

var listaCupos = document.getElementById("lista-cupos");
var cuposFecha = document.getElementById("cupos-fecha");
var limiteTexto = document.getElementById("limite-texto");

var filtroResidente = document.getElementById("filtro-residente");
var listaAgenda = document.getElementById("lista-agenda");
var contadorVisitas = document.getElementById("contador-visitas");
var sinVisitas = document.getElementById("sin-visitas");

// ---------- Fechas ----------

// Devuelve una fecha como AAAA-MM-DD (hoy + dias)
function fechaISO(dias) {
    var d = new Date();
    d.setDate(d.getDate() + dias);
    var mes = String(d.getMonth() + 1).padStart(2, "0");
    var dia = String(d.getDate()).padStart(2, "0");
    return d.getFullYear() + "-" + mes + "-" + dia;
}

// Cambia AAAA-MM-DD a DD/MM/AAAA
function fechaBonita(iso) {
    var partes = iso.split("-");
    return partes[2] + "/" + partes[1] + "/" + partes[0];
}

// ---------- Datos de ejemplo (después vendrán de la base de datos) ----------
var visitas = [
    { residente: "Rosa Muñoz", nombre: "Carla Muñoz Díaz", rut: "15.234.567-8", telefono: "+56 9 5555 1111", parentesco: "Hijo/a", fecha: fechaISO(0), bloque: "15:00 - 16:00" },
    { residente: "Luis Soto", nombre: "Pedro Soto Vera", rut: "9.876.543-2", telefono: "+56 9 5555 2222", parentesco: "Hijo/a", fecha: fechaISO(0), bloque: "15:00 - 16:00" },
    { residente: "Marta Vega", nombre: "Lucía Vega Rojas", rut: "17.111.222-3", telefono: "+56 9 5555 3333", parentesco: "Nieto/a", fecha: fechaISO(0), bloque: "16:00 - 17:00" },
    { residente: "Rosa Muñoz", nombre: "Jorge Muñoz Paz", rut: "12.222.333-4", telefono: "+56 9 5555 4444", parentesco: "Hermano/a", fecha: fechaISO(0), bloque: "16:00 - 17:00" },
    { residente: "Luis Soto", nombre: "Ana Soto Mena", rut: "11.333.444-5", telefono: "+56 9 5555 5555", parentesco: "Cónyuge", fecha: fechaISO(0), bloque: "16:00 - 17:00" },
    { residente: "Marta Vega", nombre: "Paula Vega Núñez", rut: "16.444.555-6", telefono: "+56 9 5555 6666", parentesco: "Hijo/a", fecha: fechaISO(1), bloque: "10:00 - 11:00" }
];

// ---------- Validaciones ----------

// Revisa el RUT con el dígito verificador. Devuelve el RUT formateado o "" si es inválido
function validarRut(texto) {
    var limpio = texto.replace(/[.\-\s]/g, "").toUpperCase();
    if (!/^\d{7,8}[0-9K]$/.test(limpio)) {
        return "";
    }

    var cuerpo = limpio.slice(0, -1);
    var dv = limpio.slice(-1);

    var suma = 0;
    var multiplicador = 2;
    for (var i = cuerpo.length - 1; i >= 0; i--) {
        suma += Number(cuerpo[i]) * multiplicador;
        multiplicador++;
        if (multiplicador > 7) {
            multiplicador = 2;
        }
    }

    var resto = 11 - (suma % 11);
    var esperado = String(resto);
    if (resto === 11) {
        esperado = "0";
    }
    if (resto === 10) {
        esperado = "K";
    }

    if (dv !== esperado) {
        return "";
    }
    return cuerpo + "-" + dv;
}

// El teléfono debe tener entre 8 y 11 números
function telefonoValido(texto) {
    var numeros = texto.replace(/\D/g, "");
    return numeros.length >= 8 && numeros.length <= 11;
}

// Cuenta cuántas visitas hay en una fecha y bloque
function contarVisitas(fecha, bloque) {
    var total = 0;
    for (var i = 0; i < visitas.length; i++) {
        if (visitas[i].fecha === fecha && visitas[i].bloque === bloque) {
            total++;
        }
    }
    return total;
}

// ---------- Mostrar en pantalla ----------

function mostrarMensaje(texto, tipo) {
    mensaje.textContent = texto;
    mensaje.className = "mensaje mensaje-" + tipo;
    mensaje.hidden = false;
}

// Llena el select de bloques y el panel de cupos según la fecha elegida
function mostrarCupos() {
    var fecha = inputFecha.value;
    var elegido = selBloque.value;

    selBloque.innerHTML = "";
    listaCupos.innerHTML = "";

    var opcionVacia = document.createElement("option");
    opcionVacia.value = "";
    opcionVacia.textContent = "Selecciona un bloque";
    selBloque.appendChild(opcionVacia);

    if (fecha === "") {
        cuposFecha.textContent = "día elegido";
        return;
    }
    cuposFecha.textContent = fechaBonita(fecha);

    for (var i = 0; i < BLOQUES.length; i++) {
        var usados = contarVisitas(fecha, BLOQUES[i]);
        var libres = LIMITE - usados;

        // Opción del select
        var opcion = document.createElement("option");
        opcion.value = BLOQUES[i];
        if (libres <= 0) {
            opcion.textContent = BLOQUES[i] + " (completo)";
            opcion.disabled = true;
        } else {
            opcion.textContent = BLOQUES[i] + " (" + libres + " cupos)";
        }
        selBloque.appendChild(opcion);

        // Tarjeta del panel de cupos
        var item = document.createElement("li");
        item.className = "cupo";
        if (libres <= 0) {
            item.classList.add("cupo-lleno");
        } else if (libres === 1) {
            item.classList.add("cupo-casi");
        }

        var hora = document.createElement("span");
        hora.className = "cupo-hora";
        hora.textContent = BLOQUES[i];

        var barra = document.createElement("span");
        barra.className = "cupo-barra";
        var relleno = document.createElement("span");
        relleno.className = "cupo-relleno";
        relleno.style.width = (usados / LIMITE) * 100 + "%";
        barra.appendChild(relleno);

        var estado = document.createElement("span");
        estado.className = "cupo-estado";
        if (libres <= 0) {
            estado.textContent = "Completo";
        } else {
            estado.textContent = usados + " de " + LIMITE;
        }

        item.appendChild(hora);
        item.appendChild(barra);
        item.appendChild(estado);
        listaCupos.appendChild(item);
    }

    // Mantiene el bloque elegido si todavía tiene cupos
    if (elegido !== "" && contarVisitas(fecha, elegido) < LIMITE) {
        selBloque.value = elegido;
    }
}

// Muestra la agenda (ordenada por fecha y hora) según el residente filtrado
function mostrarAgenda() {
    var filtro = filtroResidente.value;
    var lista = [];

    for (var i = 0; i < visitas.length; i++) {
        if (filtro === "" || visitas[i].residente === filtro) {
            lista.push(visitas[i]);
        }
    }

    lista.sort(function (a, b) {
        return (a.fecha + a.bloque).localeCompare(b.fecha + b.bloque);
    });

    listaAgenda.innerHTML = "";

    for (var j = 0; j < lista.length; j++) {
        listaAgenda.appendChild(crearTarjeta(lista[j]));
    }

    if (lista.length === 1) {
        contadorVisitas.textContent = "1 visita";
    } else {
        contadorVisitas.textContent = lista.length + " visitas";
    }
    sinVisitas.hidden = lista.length !== 0;
}

// Crea la tarjeta de una visita
function crearTarjeta(v) {
    var item = document.createElement("li");
    item.className = "visita";
    if (v.fecha === fechaISO(0)) {
        item.classList.add("visita-hoy");
    }

    var cuando = document.createElement("div");
    cuando.className = "visita-cuando";
    var fecha = document.createElement("strong");
    fecha.textContent = fechaBonita(v.fecha);
    var hora = document.createElement("span");
    hora.textContent = v.bloque;
    cuando.appendChild(fecha);
    cuando.appendChild(hora);

    var info = document.createElement("div");
    info.className = "visita-info";

    var residente = document.createElement("h3");
    residente.textContent = v.residente;

    var visitante = document.createElement("p");
    visitante.className = "visita-visitante";
    visitante.textContent = v.nombre;

    var etiqueta = document.createElement("span");
    etiqueta.className = "visita-parentesco";
    etiqueta.textContent = v.parentesco;

    var contacto = document.createElement("p");
    contacto.className = "visita-contacto";
    contacto.textContent = "RUT " + v.rut + " · " + v.telefono;

    info.appendChild(residente);
    info.appendChild(visitante);
    info.appendChild(etiqueta);
    info.appendChild(contacto);

    var boton = document.createElement("button");
    boton.type = "button";
    boton.className = "btn-cancelar";
    boton.textContent = "Cancelar";
    boton.addEventListener("click", function () {
        if (confirm("¿Cancelar la visita de " + v.nombre + "?")) {
            visitas.splice(visitas.indexOf(v), 1);
            mostrarCupos();
            mostrarAgenda();
        }
    });

    item.appendChild(cuando);
    item.appendChild(info);
    item.appendChild(boton);
    return item;
}

// ---------- Agendar ----------

form.addEventListener("submit", function (e) {
    e.preventDefault();
    mensaje.hidden = true;

    var nombre = inputNombre.value.trim();
    var rut = validarRut(inputRut.value);
    var telefono = inputTelefono.value.trim();
    var fecha = inputFecha.value;

    // Se revisa cada campo y se marca en rojo si está mal
    var okResidente = selResidente.value !== "";
    var okNombre = nombre.split(/\s+/).length >= 2;
    var okRut = rut !== "";
    var okTelefono = telefonoValido(telefono);
    var okParentesco = selParentesco.value !== "";
    var okFecha = fecha !== "" && fecha >= fechaISO(0);
    var okBloque = selBloque.value !== "";

    selResidente.classList.toggle("is-invalid", !okResidente);
    inputNombre.classList.toggle("is-invalid", !okNombre);
    inputRut.classList.toggle("is-invalid", !okRut);
    inputTelefono.classList.toggle("is-invalid", !okTelefono);
    selParentesco.classList.toggle("is-invalid", !okParentesco);
    inputFecha.classList.toggle("is-invalid", !okFecha);
    selBloque.classList.toggle("is-invalid", !okBloque);

    if (!(okResidente && okNombre && okRut && okTelefono && okParentesco && okFecha && okBloque)) {
        mostrarMensaje("Revisa los campos marcados en rojo.", "error");
        return;
    }

    // Validación de cupos: no se puede superar el límite de visitas simultáneas
    if (contarVisitas(fecha, selBloque.value) >= LIMITE) {
        mostrarMensaje("El bloque " + selBloque.value + " ya está completo (máximo " + LIMITE + " visitas). Elige otro horario.", "error");
        mostrarCupos();
        return;
    }

    visitas.push({
        residente: selResidente.value,
        nombre: nombre,
        rut: rut,
        telefono: telefono,
        parentesco: selParentesco.value,
        fecha: fecha,
        bloque: selBloque.value
    });

    mostrarMensaje("Visita agendada para " + selResidente.value + " el " + fechaBonita(fecha) + " de " + selBloque.value + ".", "exito");

    // Se muestra la agenda del residente que acaba de recibir la visita
    filtroResidente.value = selResidente.value;

    var fechaGuardada = fecha;
    form.reset();
    inputFecha.value = fechaGuardada;
    mostrarCupos();
    mostrarAgenda();
});

// Quita el rojo cuando la persona corrige un campo
form.addEventListener("input", function (e) {
    e.target.classList.remove("is-invalid");
});

inputFecha.addEventListener("change", mostrarCupos);
filtroResidente.addEventListener("change", mostrarAgenda);

// ---------- Al cargar la página ----------
limiteTexto.textContent = LIMITE;
inputFecha.min = fechaISO(0);
inputFecha.value = fechaISO(0);
mostrarCupos();
mostrarAgenda();