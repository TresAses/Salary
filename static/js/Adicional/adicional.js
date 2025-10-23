const idStrong = document.getElementById("id-a");
const idLegajo = document.getElementById("selector_legajos");
const idConcepto = document.getElementById("selector_conceptos");
const idCentro = document.getElementById("selector_centros");
const fecha = document.getElementById("fecha");
const importe = document.getElementById("importe");
const detalle = document.getElementById("detalle");

window.addEventListener("load", async () => {
    await listarDatosAdicional();
});


flatpickr('#fecha', {
    dateFormat: 'Y-m-d',
    altInput: true,
    altFormat: 'F j, Y',
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

const choiceCentros = new Choices('#selector_centros', {
    allowHTML: true,
    shouldSort: false,
    searchPlaceholderValue: 'Escriba para buscar..',
    itemSelectText: ''
});


selector_legajos.addEventListener("change", (event) => {
    const centroInput = document.getElementById("selector_centros");
    const parsedCustomProperties = JSON.parse(event.currentTarget.selectedOptions[0].dataset.customProperties);
    const selectedCentro = parsedCustomProperties.centro;
    choiceCentros.setChoiceByValue(selectedCentro);
});

document.getElementById('importe').addEventListener('input', function() {
    const value = parseInt(this.value, 10);
    if (value % 100 !== 0) {
        this.classList.add('invalid');
    } else {
        this.classList.remove('invalid');
    }
});

const listarDatosAdicional = async () => {
    try {
        const response = await fetch("llenar-comboxs-adicional/");
        const data = await response.json();
        if (data.Message === "Success") {

            let resultLegajos = [];
            data.Legajos.forEach((datos) => {
                resultLegajos.push({
                    value: datos.Legajo,
                    label: datos.Nombre,
                    customProperties: JSON.stringify({ centro: datos.Abrev })

                });
            });
            choiceLegajos.clearChoices();
            choiceLegajos.setChoices(resultLegajos, 'value', 'label', true);

            let resultConceptos = [];
            resultConceptos.push();
            data.Conceptos.forEach((datos) => {
                resultConceptos.push({ value: datos.IdConcepto, label: datos.Descripcion });
            });
            choiceConceptos.setChoices(resultConceptos, 'value', 'label', true);

            let resultCentros = [];
            resultCentros.push();
            data.Centros.forEach((datos) => {
                resultCentros.push({ value: datos.Abrev, label: datos.Centro });
            });
            choiceCentros.setChoices(resultCentros, 'value', 'label', true);

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

document.getElementById('nuevo-adicional').addEventListener('click', function () {
    location.reload();
});

function validaciones() {
    const valueImporte = importe.value.trim();
    if (valueImporte === '') {
        return true;
    }
    if (idLegajo.value === "" || idLegajo.value === null) {
        return true;
    }
    if (idConcepto.value === "" || idConcepto.value === null) {
        return true;
    }
    if (valueImporte % 100 !== 0) {
        return true;
    }

    return false;
}

const guardarAdicional = async () => {
    if (validaciones()) {
        var nota = 'Debe completar los campos.';
        var color = "red";
        mostrarInfo(nota, color);
    } else if (idStrong.getAttribute('data-value') !== '0') {
        var nota = 'Debe generar un nuevo Adicional.';
        var color = "red";
        mostrarInfo(nota, color);
    } else {
        try {
            const formData = new FormData();
            formData.append("legajo", idLegajo.value);
            formData.append("concepto", idConcepto.value);
            formData.append("abrev", idCentro.value);
            formData.append("fecha", fecha.value);
            formData.append("importe", importe.value);
            formData.append("detalle", detalle.value);
            const options = {
                method: 'POST',
                headers: {
                },
                body: formData
            };
            const response = await fetch("guarda-adicional/", options);
            const data = await response.json();
            if (data.Message === "Success") {
                idStrong.textContent = 'ID: ' + data.ID
                idStrong.setAttribute('data-value', data.ID);
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
    }
};









































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
