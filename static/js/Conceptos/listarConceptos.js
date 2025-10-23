document.addEventListener("DOMContentLoaded", function () {
    const choices = new Choices('#selector_conceptos', {
        allowHTML: true,
        shouldSort: false,
        searchPlaceholderValue: 'Escriba para buscar..'
    });
    window.addEventListener("load", async () => {
        await listarConceptos();
    });

    const listarConceptos = async () => {
        try {
            const response = await fetch("llenar-combox/");
            const data = await response.json();
            if (data.Message === "Success") {
                let result = [];
                result.push();
                data.Datos.forEach((datos) => {
                    result.push({ value: datos.IdConcepto, label: datos.Descripcion });
                });
                choices.setChoices(result, 'value', 'label', true);
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
});


selector_conceptos.addEventListener("change", (event) => {
    listadoConceptos();
});

const listadoConceptos = async () => {
    try {
        const formData = new FormData();
        const idConcepto = document.getElementById("selector_conceptos").value;
        formData.append("selectorConcepto", idConcepto);
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
                <tr style="background-color: ${datos.Estado === 'I' ? '#e10126' : 'transparent'}; color: ${datos.Estado === 'I' ? 'white' : 'black'};">
                    <td class="fila-id">${datos.IdConcepto}</td>
                    <td class="fila-descripcion">${datos.Descripcion}</td>
                    <td class="fila-fecha-alta">${datos.Alta}</td>
                    <td class="fila-usuario">${datos.Usuario}</td>
                    <td class="fila-fecha-modificacion">${datos.FechaModifica}</td>
                    <td class="fila-usuario-modificacion">${datos.UserModifica}</td>
                    <td class="fila-opciones">
                        <button class="btn-icon edit-btn" onclick="actualizar(${datos.IdConcepto})">
                            <i class="fas fa-edit"></i>
                        </button>
                    </td>
                </tr>
                `
            });
            document.getElementById('tabla-listado-conceptos').innerHTML = dato;
        } else {
            document.getElementById('tabla-listado-conceptos').innerHTML = ``;
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

const actualizar = async (idConcepto) => {
    try {
        const formData = new FormData();
        formData.append("selectorConcepto", idConcepto);
        const options = {
            method: 'POST',
            headers: {
            },
            body: formData
        };

        const response = await fetch("listado-tabla/", options);
        const data = await response.json();
        if (data.Message == "Success") {
            document.getElementById('pop-up-actualizaconcepto').classList.add('active');
            document.getElementById('pop-up-overlay').classList.add('active');
            let dato = ``;
            data.Datos.forEach((datos) => {
                dato += `
                <div class="idAdicional" id="id-nuevo-concepto">
                    <span class="span-id" id="id-sc" data-value="${datos.IdConcepto}">ID: ${datos.IdConcepto}</span>
                </div>
                <div class="items-formulario">
                    <input type="text" id="descripcion-nuevo-concepto" class="input-liquidacion" value="${datos.Descripcion}"
                        placeholder="Descripción del Concepto" required>
                </div>
                <div class="items-formulario">
                    <button class="estado-btn" id="estado" onclick="toggleEstado(this)" style="background-color: ${datos.Estado === 'I' ? '#e10126' : 'green'};" value="${datos.Estado}">
                        ${datos.Estado === 'A' ? 'ACTIVO' : 'INACTIVO'}
                    </button>
                </div>
                <div class="input-container items-formulario">
                    <input type="text" id="fecha-alta" class="readonly-liquidacion" placeholder="Fecha Alta" value="${datos.Alta}" readonly>
                    <input type="text" id="usuario-alta" class="readonly-liquidacion margen" placeholder="Usuario Alta" value="${datos.Usuario}"
                        readonly>
                </div>
                <div class="input-container items-formulario">
                    <input type="text" id="fecha-modifica" class="readonly-liquidacion" placeholder="Fecha Modificación" value="${datos.FechaModifica}"
                        readonly>
                    <input type="text" id="usuario-modifica" class="readonly-liquidacion margen" value="${datos.UserModifica}"
                        placeholder="Usuario Modificación" readonly>
                </div>

                <div class="adicionalBotones items-formulario">
                    <button id="cierra-concepto" class="inverted-flatpickr-button" onclick="cierraActualiza();">CERRAR</button>
                    <button id="actualiza-concepto" class="flatpickr-button" onclick="actualizaConcepto(${datos.IdConcepto});">ACTUALIZAR</button>
                </div>
                `
            });
            document.getElementById('popup-actualizaconcepto').innerHTML = dato;

            document.getElementById('pop-up-actualizaconcepto').classList.add('active');
            document.getElementById('pop-up-overlay').classList.add('active');

        } else {
            document.getElementById('popup-actualizaconcepto').innerHTML = ``;
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


const fechaAltaInput = document.getElementById("fecha-alta");
const usuarioAltaInput = document.getElementById("usuario-alta");
const fechaModificaInput = document.getElementById("fecha-modifica");
const usuarioModificaInput = document.getElementById("usuario-modifica");
const idStrong = document.getElementById("id-sc");

function validaciones() {
    const descripcionInput = document.getElementById("descripcion-nuevo-concepto");
    const descripcionValor = descripcionInput.value.trim();
    if (descripcionValor === '') {
        return true;
    }
    return false;
}

const actualizaConcepto = async (idConcepto) => {
    const fechaAltaInput = document.getElementById("fecha-alta");
    const usuarioAltaInput = document.getElementById("usuario-alta");
    const fechaModificaInput = document.getElementById("fecha-modifica");
    const usuarioModificaInput = document.getElementById("usuario-modifica");
    const idStrong = document.getElementById("id-sc");
    if (validaciones()) {
        var nota = 'Debe Completar los Campos.';
        var color = "red";
        mostrarInfo(nota, color);
    } else {
        try {
            const formData = new FormData();
            const descripcion = document.getElementById("descripcion-nuevo-concepto").value.trim();
            const estado = document.getElementById("estado").value;
            formData.append("idConcepto", idConcepto);
            formData.append("descripcion", descripcion);
            formData.append("estado", estado);
            const options = {
                method: 'POST',
                headers: {
                },
                body: formData
            };
            const response = await fetch("actualiza-concepto/", options);
            const data = await response.json();
            if (data.Message === "Success") {
                data.Datos.forEach((datos) => {
                    fechaAltaInput.value = datos.Fecha;
                    usuarioAltaInput.value = datos.Usuario;
                    fechaModificaInput.value = datos.FechaModifica;
                    usuarioModificaInput.value = datos.UserModifica;
                    idStrong.textContent = 'ID: ' + datos.Id;
                    idStrong.setAttribute('data-value', datos.Id);
                });
                var nota = data.Nota;
                var color = "green";
                mostrarInfo(nota, color);
                listadoConceptos();
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
};



function cierraActualiza() {
    document.getElementById('pop-up-actualizaconcepto').classList.remove('active');
    document.getElementById('pop-up-overlay').classList.remove('active');
}

function toggleEstado(button) {
    if (button.value === "A") {
        button.value = "I";
        button.textContent = "INACTIVO";
        button.style.backgroundColor = "red";
    } else {
        button.value = "A";
        button.textContent = "ACTIVO";
        button.style.backgroundColor = "green";
    }
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












































