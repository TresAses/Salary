const selectAllCheckbox = document.getElementById("selectAll");
const idConcepto = document.getElementById("selector_conceptos");
const idCentroAbrev = document.getElementById("selector_centros_abrev");
const fecha = document.getElementById("fecha");
const importe = document.getElementById("importe");
const detalle = document.getElementById("detalle");
const idStrong = document.getElementById("id-am");

window.addEventListener("load", async () => {
    await listarDatosAdicionalMasivo();
});

selector_centros.addEventListener("change", (event) => {
    llenaTablaLegajos();
});


document.getElementById('nuevo-adicional').addEventListener('click', function () {
    location.reload();
});

function validaciones() {
    const valueImporte = importe.value.trim();
    if (valueImporte === '') {
        return true;
    }
    if (idConcepto.value === "" || idConcepto.value === null) {
        return true;
    }
    if (isAnyCheckboxChecked()) {
        return true;
    }
    if (valueImporte % 100 !== 0) {
        return true;
    }
    if (idCentroAbrev.value === "" || idCentroAbrev.value === null) {
        return true;
    }

    return false;
}

const guardarAdicional = async () => {
    if (validaciones()) {
        var nota = 'Debe completar los campos y/o tildar al menos un legajo.';
        var color = "red";
        mostrarInfo(nota, color);
    } else if (idStrong.getAttribute('data-value') !== '0') {
        var nota = 'Debe generar un nuevo Adicional.';
        var color = "red";
        mostrarInfo(nota, color);
    } else {
        try {
            const formData = new FormData();
            formData.append("concepto", idConcepto.value);
            formData.append("abrev", idCentroAbrev.value);
            formData.append("fecha", fecha.value);
            formData.append("importe", importe.value);
            formData.append("detalle", detalle.value);

            const checkboxes = document.querySelectorAll('.input-checkbox:not(#selectAll):checked');
            checkboxes.forEach(checkbox => {
                if (checkbox.checked) {
                    formData.append('legajos', checkbox.value);
                }
            });
            const options = {
                method: 'POST',
                headers: {
                },
                body: formData
            };
            const response = await fetch("guarda-adicional-masivo/", options);
            const data = await response.json();
            if (data.Message === "Success") {
                idStrong.textContent = 'ÚLTIMO ID: ' + data.ID
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


const listarDatosAdicionalMasivo = async () => {
    try {
        const response = await fetch("llenar-comboxs-adicional-masivo/");
        const data = await response.json();
        if (data.Message === "Success") {

            let resultCentros = [];
            data.Centros.forEach((datos) => {
                resultCentros.push({
                    value: datos.Abrev,
                    label: datos.Centro,
                });
            });
            choiceCentros.clearChoices();
            choiceCentros.setChoices(resultCentros, 'value', 'label', true);
            choiceCentrosAbrev.setChoices(resultCentros, 'value', 'label', true);

            let resultConceptos = [];
            resultConceptos.push();
            data.Conceptos.forEach((datos) => {
                resultConceptos.push({ value: datos.IdConcepto, label: datos.Descripcion });
            });
            choiceConceptos.setChoices(resultConceptos, 'value', 'label', true);

        } else {
            var nota = data.Nota;
            var color = "red";
            mostrarInfo(nota, color);
        }
    } catch (error) {
        var nota = "Se produjo un error al procesar la solicitud.";
        var color = "red";
        mostrarInfo(nota, color);
    }
}

const llenaTablaLegajos = async () => {
    try {
        const formData = new FormData();
        const Abrev = document.getElementById("selector_centros").value;
        formData.append("Abrev", Abrev);
        const options = {
            method: 'POST',
            headers: {
            },
            body: formData
        };

        const response = await fetch("listado-tabla/", options);
        const data = await response.json();
        if (data.Message == "Success") {
            let dato = ``;
            data.Datos.forEach((datos) => {
                dato += `
                <tr>
                    <th><input class="input-checkbox checkbox" type="checkbox" id="idCheck" name="idCheck"
                            value="${datos.Legajo}"></th>
                    <td>${datos.Legajo}</td>
                    <td>${datos.Nombre}</td>
                </tr>
                `
            });
            document.getElementById('tabla-masivo-adicional').innerHTML = dato;
        } else {
            document.getElementById('tabla-masivo-adicional').innerHTML = ``;
            var nota = data.Nota
            var color = "red";
            mostrarInfo(nota, color);
        }
    } catch (error) {
        var nota = "Se produjo un error al procesar la solicitud.";
        var color = "red";
        mostrarInfo(nota, color);
    }
};

document.getElementById('importe').addEventListener('input', function() {
    const value = parseInt(this.value, 10);
    if (value % 100 !== 0) {
        this.classList.add('invalid');
    } else {
        this.classList.remove('invalid');
    }
});


flatpickr('#fecha', {
    dateFormat: 'Y-m-d',
    altInput: true,
    altFormat: 'F j, Y',
    defaultDate: 'today',
    placeholder: 'Selecciona una fecha',
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

const choiceCentrosAbrev = new Choices('#selector_centros_abrev', {
    allowHTML: true,
    shouldSort: false,
    searchPlaceholderValue: 'Escriba para buscar..',
    itemSelectText: ''
});


selectAllCheckbox.addEventListener("change", function () {
    if (selectAllCheckbox.checked) {
        const checkboxes = document.querySelectorAll(".input-checkbox");
        checkboxes.forEach(checkbox => {
            checkbox.checked = true;
        });
    } else {
        const checkboxes = document.querySelectorAll(".input-checkbox");
        checkboxes.forEach(checkbox => {
            checkbox.checked = false;
        });

    }
});

function isAnyCheckboxChecked() {
    const checkboxes = document.querySelectorAll('#tabla-masivo-adicional .input-checkbox');

    for (const checkbox of checkboxes) {
        if (checkbox.checked) {
            return false;
        }
    }
    return true;
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
