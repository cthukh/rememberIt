// Bitácora: filtros de la línea de tiempo

// Elementos de la página
var selResidente = document.getElementById("filtro-residente");
var selTipo = document.getElementById("filtro-tipo");
var inputDesde = document.getElementById("filtro-desde");
var inputHasta = document.getElementById("filtro-hasta");
var btnLimpiar = document.getElementById("btn-limpiar");
var registros = document.querySelectorAll(".registro");
var contador = document.getElementById("contador");
var sinResultados = document.getElementById("sin-resultados");

// Números del resumen
var resTotal = document.getElementById("res-total");
var resNotas = document.getElementById("res-notas");
var resIncidentes = document.getElementById("res-incidentes");
var resGraves = document.getElementById("res-graves");

function filtrar() {
    var total = 0;
    var notas = 0;
    var incidentes = 0;
    var graves = 0;

    for (var i = 0; i < registros.length; i++) {
        var r = registros[i];
        var mostrar = true;

        if (selResidente.value !== "" && r.dataset.residente !== selResidente.value) {
            mostrar = false;
        }
        if (selTipo.value !== "" && r.dataset.tipo !== selTipo.value) {
            mostrar = false;
        }
        // Las fechas en formato AAAA-MM-DD se pueden comparar como texto
        if (inputDesde.value !== "" && r.dataset.fecha < inputDesde.value) {
            mostrar = false;
        }
        if (inputHasta.value !== "" && r.dataset.fecha > inputHasta.value) {
            mostrar = false;
        }

        r.hidden = !mostrar;

        if (mostrar) {
            total++;
            if (r.dataset.tipo === "nota") {
                notas++;
            }
            if (r.dataset.tipo === "incidente") {
                incidentes++;
            }
            if (r.dataset.gravedad === "grave") {
                graves++;
            }
        }
    }

    resTotal.textContent = total;
    resNotas.textContent = notas;
    resIncidentes.textContent = incidentes;
    resGraves.textContent = graves;

    contador.textContent = "Mostrando " + total + " de " + registros.length + " registros";
    sinResultados.hidden = total !== 0;
}

function limpiar() {
    document.getElementById("form-filtros").reset();
    filtrar();
}

selResidente.addEventListener("change", filtrar);
selTipo.addEventListener("change", filtrar);
inputDesde.addEventListener("change", filtrar);
inputHasta.addEventListener("change", filtrar);
btnLimpiar.addEventListener("click", limpiar);

// Al cargar la página
filtrar();