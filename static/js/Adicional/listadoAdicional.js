const inicio = document.getElementById("fechaInicio");
const final = document.getElementById("fechaFinal");
const centro = document.getElementById("selector_centros");
const legajo = document.getElementById("selector_legajos");
const concepto = document.getElementById("selector_conceptos");
const estado = document.getElementById("selector_estados");
const popupEliminacion = document.getElementById('popup-eliminacion');

const idDatosMod = document.getElementById('id-a_act');
const legajoDatosMod = document.getElementById('user_act');
const centroDatosMod = document.getElementById('centro-user_act');
const selectorDatosMod = document.getElementById('selector_conceptos_act');
const fechaDatosMod = document.getElementById('fecha_act');
const importeDatosMod = document.getElementById('importe_act');
const detalleDatosMod = document.getElementById('detalle_act');

const detallesAdcionales = document.getElementById('cant_importe');


window.addEventListener("load", async () => {
    await listarDatosAdicionalMasivo();
});

selector_centros.addEventListener("change", (event) => {
    listarLegajos();
    llenarTablaAdicionales();
});

selector_legajos.addEventListener("change", (event) => {
    llenarTablaAdicionales();
});

selector_conceptos.addEventListener("change", (event) => {
    llenarTablaAdicionales();
});

selector_estados.addEventListener("change", (event) => {
    llenarTablaAdicionales();
});

fechaInicio.addEventListener("change", (event) => {
    llenarTablaAdicionales();
});

fechaFinal.addEventListener("change", (event) => {
    llenarTablaAdicionales();
});


const today = new Date();
const firstDayOfMonth = new Date(today.getFullYear(), today.getMonth(), 1);

flatpickr('#fechaInicio', {
    dateFormat: 'Y-m-d',
    altInput: true,
    altFormat: 'j F, Y',
    defaultDate: firstDayOfMonth, // Pasar el objeto Date directamente
    placeholder: 'Selecciona una fecha',
});

flatpickr('#fecha_act', {
    dateFormat: 'Y-m-d',
    altInput: true,
    altFormat: 'j F, Y',
    defaultDate: '',
    placeholder: 'Selecciona una fecha',
});

flatpickr('#fechaFinal', {
    dateFormat: 'Y-m-d',
    altInput: true,
    altFormat: 'j F , Y',
    defaultDate: 'today',
    placeholder: 'Selecciona una fecha',
});

const choiceLegajos = new Choices('#selector_legajos', {
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

const choiceEstados = new Choices('#selector_estados', {
    allowHTML: true,
    shouldSort: false,
    searchPlaceholderValue: 'Escriba para buscar..',
    itemSelectText: ''
});

const choiceCentros = new Choices('#selector_centros', {
    allowHTML: true,
    shouldSort: false,
    searchPlaceholderValue: 'Escriba para buscar..',
    itemSelectText: ''
});

const choiceConceptosAct = new Choices('#selector_conceptos_act', {
    allowHTML: true,
    shouldSort: false,
    searchPlaceholderValue: 'Escriba para buscar..',
    itemSelectText: ''
});

document.getElementById('importe_act').addEventListener('input', function() {
    const value = parseInt(this.value, 10);
    if (value % 100 !== 0) {
        this.classList.add('invalid');
    } else {
        this.classList.remove('invalid');
    }
});

const listarDatosAdicionalMasivo = async () => {
    try {
        const response = await fetch("carga-datos-inicio/");
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

            let resultEstados = [];
            resultEstados.push();
            data.Estados.forEach((datos) => {
                resultEstados.push({
                    value: datos.IDestado,
                    label: datos.Estado
                });
            });
            choiceEstados.clearChoices();
            choiceEstados.setChoices(resultEstados, 'value', 'label', true);

        } else {
            var nota = data.Nota;
            var color = "red";
            mostrarInfo(nota, color);
        }
    } catch (error) {
        var nota = "Se produjo un error al procesar la solicitud. "  + error;
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
        const response = await fetch("centro-legajos/", options);
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

const llenarTablaAdicionales = async () => {
    showSpinner();
    try {
        const formData = new FormData();
        formData.append("Inicio", inicio.value);
        formData.append("Final", final.value);
        formData.append("Centro", centro.value);
        formData.append("Legajo", legajo.value);
        formData.append("Concepto", concepto.value);
        formData.append("Estado", estado.value);
        const options = {
            method: 'POST',
            headers: {
            },
            body: formData
        };

        const response = await fetch("llenar-tabla-adicional/", options);
        const data = await response.json();
        if (data.Message == "Success") {
            let dato = ``;
            data.Datos.forEach((datos) => {
                dato += `
                <tr>
                    <td class="fila-legajo">${datos.Legajo}</td>
                    <td class="fila-nombres">${datos.Nombre}</td>
                    <td class="fila-centro">${datos.Abrev2}</td>
                    <td class="fila-concepto">${datos.Concepto}</td>
                    <td class="fila-fecha">${datos.Fecha}</td>
                    <td class="fila-importe">$ ${datos.Importe}</td>
                    <td class="fila-estado">
                        <div class="estado" style="background-color: ${datos.Color};">${datos.Estado}</div>
                    </td>
                    <td class="fila-alta">${datos.Alta}</td>
                    <td class="fila-usuario">${datos.Usuario}</td>
                    <td class="fila-opciones">
                        <button class="btn-icon edit-btn" onclick="activo(${datos.IdAdicional});" ${datos.IdEstado === 'L' || datos.IdEstado === 'A' ? 'disabled' : ''}>
                            <i class="fas fa-edit" style="${datos.IdEstado !== 'P' ? 'color: grey;' : ''}"></i>
                        </button>
                        <button class="btn-icon delete-btn" onclick="mostrarPopupEliminacion(${datos.IdAdicional});" ${datos.IdEstado === 'L' || datos.IdEstado === 'A' ? 'disabled' : ''}>
                            <i class="fas fa-trash-alt" style="${datos.IdEstado !== 'P' ? 'color: grey;' : ''}"></i>
                        </button>
                    </td>
                </tr>
                `
            });
            detallesAdcionales.style.backgroundColor = data.Color;
            if (data.Color == "orange"){
                detallesAdcionales.style.color = 'black';
            }else {
                detallesAdcionales.style.color = 'white';
            }
            detallesAdcionales.innerHTML = `<div>Cant.: ${data.Cantidad}  -  Importe Total: ${data.Total}</div>`;
            document.getElementById('listado-tabla-adicionales').innerHTML = dato;
            hideSpinner();
        } else {
            hideSpinner();
            document.getElementById('listado-tabla-adicionales').innerHTML = ``;
            detallesAdcionales.style.color = 'white';
            detallesAdcionales.style.backgroundColor = 'white';
            detallesAdcionales.innerHTML = `<div>*</div>`;
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


const eliminaAdicional = async () => {
    try {
        const formData = new FormData();
        const idAdicional = document.getElementById("idAdicionalElimina").value;
        formData.append("IdAdicional", idAdicional);
        const options = {
            method: 'POST',
            headers: {},
            body: formData
        };
        const response = await fetch("elimina-adicional/", options);
        const data = await response.json();
        if (data.Message === "Success") {
            var nota = data.Nota;
            var color = "green";
            mostrarInfo(nota, color);
            ocultarPopupEliminacion();
            llenarTablaAdicionales();
        } else {
            var nota = data.Nota;
            var color = "red";
            mostrarInfo(nota, color);
        }
    } catch (error) {
        ocultarPopupEliminacion();
        var nota = "Se produjo un error al procesar la solicitud. " + error;
        var color = "red";
        mostrarInfo(nota, color);
    }
};


const activo = async (idAdicional) => {
    try {
        const formData = new FormData();
        formData.append("IdAdicional", idAdicional);
        const options = {
            method: 'POST',
            headers: {},
            body: formData
        };
        const response = await fetch("datos-modifica-adicional/", options);
        const data = await response.json();
        if (data.Message === "Success") {
            let resultConceptos = [];
            resultConceptos.push();
            data.Conceptos.forEach((datos) => {
                resultConceptos.push({ value: datos.IdConcepto, label: datos.Descripcion });
            });
            choiceConceptosAct.setChoices(resultConceptos, 'value', 'label', true);
            choiceConceptosAct.setChoiceByValue(data.IdConcepto.toString()); 
                    
            idDatosMod.textContent = 'ID: ' + data.IdAdicional;
            idDatosMod.setAttribute('data-value', data.IdAdicional);
            legajoDatosMod.value = data.Nombre;
            centroDatosMod.value = data.Centro;
            selectorDatosMod.value = data.IdConcepto;
            importeDatosMod.value = data.Importe;
            importeDatosMod.setAttribute('data-value', data.Importe);
            detalleDatosMod.value = data.Detalle;
            const flatpickrInstance = flatpickr(fechaDatosMod);
            flatpickrInstance.setDate(data.Fecha);  
            document.getElementById('pop-up-actualizaAdicional').classList.add('active');
            document.getElementById('pop-up-overlay').classList.add('active');
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

const actualizaAdicional = async () => {
    try {
        const formData = new FormData();
        formData.append("IdAdicional", idDatosMod.getAttribute('data-value'));
        formData.append("IdConcepto", selectorDatosMod.value);
        formData.append("IdFecha", fechaDatosMod.value);
        formData.append("IdImporte", importeDatosMod.value);
        formData.append("IdDetalle", detalleDatosMod.value);
        const options = {
            method: 'POST',
            headers: {},
            body: formData
        };
        const response = await fetch("actualiza-adicional/", options);
        const data = await response.json();
        if (data.Message === "Success") {
            llenarTablaAdicionales();
            var nota = data.Nota;
            var color = "green";
            mostrarInfo(nota, color);
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

function inactivo() {
    document.getElementById('pop-up-actualizaAdicional').classList.remove('active');
    document.getElementById('pop-up-overlay').classList.remove('active');
}




function mostrarPopupEliminacion(idAdicional) {
    idAdicionalAEliminar = idAdicional;
    popupEliminacion.style.display = 'flex';
    document.getElementById('idElimina').innerHTML = `<input type="hidden" id="idAdicionalElimina" name="idAdicionalElimina" value="${idAdicional}">`;
}

function ocultarPopupEliminacion() {
    popupEliminacion.style.display = 'none';
    idAdicionalAEliminar = null;
}






























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
