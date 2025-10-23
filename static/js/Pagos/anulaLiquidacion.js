const inicio = document.getElementById("fechaInicio");
const final = document.getElementById("fechaFinal");
const liquidaciones = document.getElementById("selector_liquidacion");
const centro = document.getElementById("selector_centros");
const legajo = document.getElementById("selector_legajos");

window.addEventListener("load", async () => {
    listarLiquidaciones();
});

selector_liquidacion.addEventListener("change", (event) => {
    listarLegajosCentros();
    llenarTablaAnulaLiquidacion();
});

selector_centros.addEventListener("change", (event) => {
    llenarTablaAnulaLiquidacion();
});

selector_legajos.addEventListener("change", (event) => {
    llenarTablaAnulaLiquidacion();
});

document.getElementById('buscaAnular').addEventListener('click', function () {
    listarLiquidaciones();
});

fechaInicio.addEventListener("change", (event) => {
    listarLiquidaciones();
});

fechaFinal.addEventListener("change", (event) => {
    listarLiquidaciones();
});


const today = new Date();
const firstDayOfMonth = new Date(today.getFullYear(), today.getMonth(), 1);


const formatDate = (date) => {
    const day = String(date.getDate()).padStart(2, '0');
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const year = date.getFullYear();
    return `${year}-${month}-${day}`;
};

flatpickr('#fechaInicio', {
    dateFormat: 'Y-m-d',
    altInput: true,
    altFormat: 'j F , Y',
    defaultDate: formatDate(firstDayOfMonth),
    placeholder: 'Selecciona una fecha',
});
flatpickr('#fechaFinal', {
    dateFormat: 'Y-m-d',
    altInput: true,
    altFormat: 'j F , Y',
    defaultDate: 'today',
    placeholder: 'Selecciona una fecha',
});

const choiceCentros = new Choices('#selector_centros', {
    allowHTML: true,
    shouldSort: false,
    searchPlaceholderValue: 'Escriba para buscar..',
    itemSelectText: ''
});

const choiceLegajos = new Choices('#selector_legajos', {
    allowHTML: true,
    shouldSort: false,
    searchPlaceholderValue: 'Escriba para buscar..',
    itemSelectText: ''
});

const choiceLiquidacion = new Choices('#selector_liquidacion', {
    allowHTML: true,
    shouldSort: false,
    searchPlaceholderValue: 'Escriba para buscar..',
    itemSelectText: ''
});



const listarLiquidaciones = async () => {
    try {
        const formData = new FormData();
        formData.append("Inicio", inicio.value);
        formData.append("Final", final.value);
        const options = {
            method: 'POST',
            headers: {},
            body: formData
        };
        const response = await fetch("listar-liquidaciones-anular/", options);
        const data = await response.json();
        if (data.Message === "Success") {

            let resultLiquidaciones = [];
            resultLiquidaciones.push();
            data.Liquidaciones.forEach((datos) => {
                resultLiquidaciones.push({
                    value: datos.IdLiquidacion,
                    label: datos.Liquidacion
                });
            });
            choiceLiquidacion.clearChoices();
            choiceLiquidacion.setChoices(resultLiquidaciones, 'value', 'label', true);
            
        } else {
            var nota = data.Nota;
            var color = "red";
            mostrarInfo(nota, color);
        }
    } catch (error) {
        var nota = "Se produjo un error al procesar la solicitud. " + error;
        var color = "red";
        mostrarInfo(nota, color);
    }
};


const listarLegajosCentros = async () => {
    try {
        const formData = new FormData();
        formData.append("IdLiquidacion", liquidaciones.value);
        const options = {
            method: 'POST',
            headers: {},
            body: formData
        };
        const response = await fetch("lista-personal-centros/", options);
        const data = await response.json();
        if (data.Message === "Success") {

            let result = [];
            data.Legajos.forEach((datos) => {
                result.push({ value: datos.Legajo, label: datos.Nombre });
            });
            choiceLegajos.removeActiveItems();
            choiceLegajos.clearChoices();
            choiceLegajos.setChoices([{ value: '', label: 'SELECCIONE UN LEGAJO', selected: true, disabled: true }].concat(result), 'value', 'label', true);

            let resultCentros = [];
            data.Centros.forEach((datos) => {
                resultCentros.push({
                    value: datos.Abrev,
                    label: datos.Centro
                });
            });
            choiceCentros.removeActiveItems();
            choiceCentros.clearChoices();
            choiceCentros.setChoices([{ value: '', label: 'SELECCIONE UN CENTRO', selected: true, disabled: true }].concat(resultCentros), 'value', 'label', true);

        } else {
            var nota = data.Nota;
            var color = "red";
            mostrarInfo(nota, color);
        }
    } catch (error) {
        var nota = "Se produjo un error al procesar la solicitud. " + error;
        var color = "red";
        mostrarInfo(nota, color);
    }
};

const llenarTablaAnulaLiquidacion = async () => {
    try {
        const formData = new FormData();
        formData.append("Liquidacion", liquidaciones.value);
        formData.append("Centro", centro.value);
        formData.append("Legajo", legajo.value);
        const options = {
            method: 'POST',
            headers: {
            },
            body: formData
        };

        const response = await fetch("lista-data-tabla-liquidaciones/", options);
        const data = await response.json();
        if (data.Message == "Success") {
            let dato = ``;
            data.Datos.forEach((datos) => {
                dato += `
                <tr>
                    <td class="fila-id">${datos.IdAdicional}</td>
                    <td class="fila-legajo">${datos.Legajo}</td>
                    <td class="fila-nombres">${datos.Nombre}</td>
                    <td class="fila-centro">${datos.Abrev2}</td>
                    <td class="fila-concepto">${datos.Concepto}</td>
                    <td class="fila-concepto">${datos.Detalle}</td>
                    <td class="fila-fecha">${datos.Fecha}</td>
                    <td class="fila-importe">$ ${datos.Importe}</td>
                    <td class="fila-opciones">
                        <button class="btn-icon delete-btn" onclick="activo(${datos.IdAdicional})"; >
                            <i class="fas fa-trash-alt"></i>
                        </button>
                    </td>
                </tr>
                `
            });
            document.getElementById('listado-tabla-anula-liquidaciones').innerHTML = dato;
        } else {
            document.getElementById('listado-tabla-anula-liquidaciones').innerHTML = ``;
            var nota = data.Nota
            var color = "red";
            mostrarInfo(nota, color);
        }
    } catch (error) {
        var nota = "Se produjo un error al procesar la solicitud. "  + error;
        var color = "red";
        mostrarInfo(nota, color);
    }
};

const eliminaAdicional = async () => {
    try {
        const formData = new FormData();
        const idAdicional_remove = document.getElementById("idAdicionalElimina");
        formData.append("IdAdicional", idAdicional_remove.value);
        const options = {
            method: 'POST',
            headers: {
            },
            body: formData
        };

        const response = await fetch("quita-de-liquidacion/", options);
        const data = await response.json();
        if (data.Message == "Success") {
            document.getElementById('popup-liquida').classList.remove('active');
            var nota = data.Nota
            var color = "green";
            mostrarInfo(nota, color);
            llenarTablaAnulaLiquidacion();
        } else {
            var nota = data.Nota
            var color = "red";
            mostrarInfo(nota, color);
        }
    } catch (error) {
        var nota = "Se produjo un error al procesar la solicitud. "  + error;
        var color = "red";
        mostrarInfo(nota, color);
    }
};

function activo(IdAdicional){
    document.getElementById('idAdicional_remove').innerHTML = `
    <input type="hidden" id="idAdicionalElimina" name="idAdicionalElimina" value="${IdAdicional}">
    `;
    document.getElementById('popup-liquida').classList.add('active');
}

document.getElementById('btn-cancelar-eliminacion').addEventListener('click', function() {
    document.getElementById('popup-liquida').classList.remove('active');
});

document.getElementById('btn-confirmar-quitar').addEventListener('click', function() {
    eliminaAdicional();
});
















































function mostrarInfo(Message, Color) {
    document.getElementById("popup").classList.add("active");
    const colorBorderMsg = document.getElementById("popup");
    const mensaje = document.getElementById("mensaje-pop-up");
    colorBorderMsg.style.border = `2px solid ${Color}`;
    mensaje.innerHTML = `<p style="color: black; font-size: 13px;"><b>${Message}</b></p>`;

    setTimeout(() => {
        document.getElementById("popup").classList.remove("active");
    }, 5000);
}
