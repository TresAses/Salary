const inicio = document.getElementById("fechaInicio");
const final = document.getElementById("fechaFinal");
const centro = document.getElementById("selector_centros");
const legajo = document.getElementById("selector_legajos");
const concepto = document.getElementById("selector_conceptos");
const liquidaciones = document.getElementById("selector_liquidacion");

const selectAllCheckbox = document.getElementById("selectAll");
const liquidarButton = document.getElementById("pagos-liquidar");

window.addEventListener("load", async () => {
    updateButtonState();
    listarDatosPagos();
});

document.getElementById('buscar_liquidar').addEventListener('click', function () {
    llenarTablaLiquidar();
});

document.getElementById('buscar_liquidar').addEventListener('click', function () {
    llenarTablaLiquidar();
});

fechaInicio.addEventListener("change", (event) => {
    llenarTablaLiquidar();
});

fechaFinal.addEventListener("change", (event) => {
    llenarTablaLiquidar();
});

selector_legajos.addEventListener("change", (event) => {
    llenarTablaLiquidar();
});


selector_centros.addEventListener("change", (event) => {
    listarLegajos();
    llenarTablaLiquidar();
});

selector_conceptos.addEventListener("change", (event) => {
    llenarTablaLiquidar();
});

const choiceCentros = new Choices('#selector_centros', {
    allowHTML: true,
    shouldSort: false,
    searchPlaceholderValue: 'Escriba para buscar..',
    itemSelectText: ''
});

const choiceConceptos = new Choices('#selector_conceptos', {
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



function updateButtonState() {
    const checkboxes = document.querySelectorAll(".input-checkbox");
    const anyChecked = Array.from(checkboxes).some(checkbox => checkbox.checked);
    if (anyChecked) {
        liquidarButton.disabled = false;
        liquidarButton.classList.add("enabled");
    } else {
        liquidarButton.disabled = true;
        liquidarButton.classList.remove("enabled");
    }
}

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

const listarDatosPagos = async () => {
    try {
        const response = await fetch("listar-conceptos-centros/");
        const data = await response.json();
        if (data.Message === "Success") {

            let resultCentros = [];
            data.Centros.forEach((datos) => {
                resultCentros.push({
                    value: datos.Abrev,
                    label: datos.Centro
                });
            });
            choiceCentros.clearChoices();
            choiceCentros.setChoices(resultCentros, 'value', 'label', true);

            let resultConceptos = [];
            resultConceptos.push();
            data.Conceptos.forEach((datos) => {
                resultConceptos.push({
                    value: datos.IdConcepto,
                    label: datos.Descripcion
                });
            });
            choiceConceptos.clearChoices();
            choiceConceptos.setChoices(resultConceptos, 'value', 'label', true);

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
}

const listarLegajos = async () => {
    try {
        const formData = new FormData();
        const idCentro = document.getElementById("selector_centros").value;
        formData.append("idCentro", idCentro);
        const options = {
            method: 'POST',
            headers: {},
            body: formData
        };
        const response = await fetch("listar-legajos-centros/", options);
        const data = await response.json();
        if (data.Message === "Success") {
            let result = [];
            data.Datos.forEach((datos) => {
                result.push({ value: datos.Legajo, label: datos.Nombre });
            });
            choiceLegajos.removeActiveItems();
            choiceLegajos.clearChoices();
            choiceLegajos.setChoices([{ value: '', label: 'SELECCIONE UN LEGAJO', selected: true, disabled: true }].concat(result), 'value', 'label', true);

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


const llenarTablaLiquidar = async () => {
    showSpinner();
    try {
        const formData = new FormData();
        formData.append("Inicio", inicio.value);
        formData.append("Final", final.value);
        formData.append("Centro", centro.value);
        formData.append("Legajo", legajo.value);
        formData.append("Concepto", concepto.value);
        formData.append("Estado", 'P');
        const options = {
            method: 'POST',
            headers: {
            },
            body: formData
        };

        const response = await fetch("listar-tabla-liquidar/", options);
        const data = await response.json();
        if (data.Message == "Success") {
            let dato = ``;
            data.Datos.forEach((datos) => {
                dato += `
                <tr>
                    <td><input class="input-checkbox checkbox" type="checkbox" id="idCheck" name="idCheck" value="${datos.IdAdicional}"></td>
                    <td class="fila-legajo">${datos.Legajo}</td>
                    <td class="fila-nombres">${datos.Nombre}</td>
                    <td class="fila-centro">${datos.Abrev2}</td>
                    <td class="fila-concepto">${datos.Concepto}</td>
                    <td class="fila-fecha">${datos.Fecha}</td>
                    <td class="fila-importe">$ ${datos.Importe}</td>
                    <td class="fila-estado"><div class="estado" style="background-color: ${datos.Color};">${datos.Estado}</div></td>
                    <td class="fila-alta">${datos.Alta}</td>
                    <td class="fila-usuario">${datos.Usuario}</td>
                    <td class="fila-opciones">
                        <button class="btn-icon edit-btn" onclick="activo(${datos.IdAdicional});" ${datos.IdEstado === 'L' || datos.IdEstado === 'A' ? 'disabled' : ''}>
                            <i class="fas fa-edit" style="${datos.IdEstado !== 'P' ? 'color: grey;' : 'color: grey;'}"></i>
                        </button>
                        <button class="btn-icon delete-btn" onclick="mostrarPopupEliminacion(${datos.IdAdicional});" ${datos.IdEstado === 'L' || datos.IdEstado === 'A' ? 'disabled' : ''}>
                            <i class="fas fa-trash-alt" style="${datos.IdEstado !== 'P' ? 'color: grey;' : 'color: grey;'}"></i>
                        </button>
                    </td>
                </tr>
                `
            });
            document.getElementById('listado-tabla-liquidar').innerHTML = dato;

            const checkboxes = document.querySelectorAll('.input-checkbox');
            checkboxes.forEach(checkbox => {
                checkbox.addEventListener("change", function () {
                updateButtonState();
                });
            });
            
            selectAllCheckbox.addEventListener("change", function () {
                checkboxes.forEach(checkbox => {
                    checkbox.checked = selectAllCheckbox.checked;
                });
                updateButtonState();
            });
            hideSpinner();
        } else {
            hideSpinner();
            document.getElementById('listado-tabla-liquidar').innerHTML = ``;
            var nota = data.Nota
            var color = "red";
            mostrarInfo(nota, color);
        }
    } catch (error) {
        hideSpinner();
        var nota = "Se produjo un error al procesar la solicitud. "  + error;
        var color = "red";
        mostrarInfo(nota, color);
    }
};

const asignaLiquidacion = async () => {
    showSpinner();
    try {
        const formData = new FormData();
        const checkboxes = document.querySelectorAll('.input-checkbox:not(#selectAll):checked');
        checkboxes.forEach(checkbox => {
            if (checkbox.checked) {
                formData.append('adicionales', checkbox.value);
            }
            formData.append('liquidacion', liquidaciones.value);
        });
        const options = {
            method: 'POST',
            headers: {
            },
            body: formData
        };
        const response = await fetch("aisgna-liquidacion/", options);
        const data = await response.json();
        if (data.Message === "Success") {
            llenarTablaLiquidar();
            var nota = data.Nota;
            var color = "green";
            mostrarInfo(nota, color);
            document.getElementById('popup-liquida').classList.remove('active');
            hideSpinner();
        } else {
            hideSpinner();
            var nota = data.Nota;
            var color = "red";
            mostrarInfo(nota, color);
        }
    } catch (error) {
        hideSpinner();
        var nota = "Se produjo un error al procesar la solicitud. " + error;
        var color = "red";
        mostrarInfo(nota, color);
    }
};


document.getElementById('pagos-liquidar').addEventListener('click', function() {
    document.getElementById('popup-liquida').classList.add('active');
});

document.getElementById('btn-cancelar-eliminacion').addEventListener('click', function() {
    document.getElementById('popup-liquida').classList.remove('active');
});

document.getElementById('btn-confirmar-liquidacion').addEventListener('click', function() {
    asignaLiquidacion();
});












function hideSpinner() {
    const spinnerWrapper = document.getElementById('spinner-wrapper');
    if (spinnerWrapper) {
        spinnerWrapper.style.display = 'none';
    }
}


function showSpinner() {
    const spinnerWrapper = document.getElementById('spinner-wrapper');
    if (spinnerWrapper) {
        spinnerWrapper.style.display = 'block';
    }
}













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
