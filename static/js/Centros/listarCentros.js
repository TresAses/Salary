const popupEliminacion = document.getElementById('popup-eliminacion');



window.addEventListener("load", async () => {
    await listarCentros();
});

selector_centros.addEventListener("change", (event) => {
    llenaTablaCentros();
});

document.getElementById('btn_buscar_centros').addEventListener('click', function () {
    llenaTablaCentros();
});


document.getElementById('btn_cancelar').addEventListener('click', function () {
    ocultarPopupEliminacion();
});

document.getElementById('btn_confirmar').addEventListener('click', function () {
    removeCentro();
});

const choiceCentros = new Choices('#selector_centros', {
    allowHTML: true,
    shouldSort: false,
    searchPlaceholderValue: 'Escriba para buscar..',
    itemSelectText: ''
});


const listarCentros = async () => {
    try {
        const response = await fetch("llenar-combox/");
        const data = await response.json();
        if (data.Message === "Success") {
            let result = [];
            result.push();
            data.Datos.forEach((datos) => {
                result.push({ value: datos.Id, label: datos.Descripcion });
            });
            choiceCentros.setChoices(result, 'value', 'label', true);
        } else {
            var nota = data.Nota
            var color = "red";
            mostrarInfo(nota, color);
        }
    } catch (error) {
        var nota = "Se produjo un error al procesar la solicitud. " + error;
        var color = "red";
        mostrarInfo(nota, color);
    }
}

const llenaTablaCentros = async () => {
    try {
        const formData = new FormData();
        const Abrev = document.getElementById("selector_centros").value;
        formData.append("Centro", Abrev);
        const options = {
            method: 'POST',
            headers: {
            },
            body: formData
        };

        const response = await fetch("completa-tabla/", options);
        const data = await response.json();
        if (data.Message == "Success") {
            let dato = ``;
            data.Datos.forEach((datos) => {
                dato += `
                <tr>
                    <td class="fila-abrev">${datos.Abrev}</td>
                    <td class="fila-descripcion">${datos.Descripcion}</td>
                    <td class="fila-fecha-alta">${datos.Alta}</td>
                    <td class="fila-usuario">${datos.Usuario}</td>
                    <td class="fila-fecha-modificacion">${datos.FechaModifica}</td>
                    <td class="fila-usuario-modificacion">${datos.UserModifica}</td>
                    <td class="fila-opciones">
                        <button class="btn-icon delete-btn" onclick="mostrarPopupEliminacion(${datos.ID})";>
                            <i class="fas fa-trash-alt"></i>
                        </button>
                    </td>
                </tr>
                `
            });
            document.getElementById('tabla_centros').innerHTML = dato;
        } else {
            document.getElementById('tabla_centros').innerHTML = ``;
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


const removeCentro = async () => {
    try {
        const formData = new FormData();
        const Abrev = document.getElementById("idCentroElimina").value;
        formData.append("Centro", Abrev);
        const options = {
            method: 'POST',
            headers: {
            },
            body: formData
        };

        const response = await fetch("elimina-centro/", options);
        const data = await response.json();
        if (data.Message == "Success") {
            llenaTablaCentros();
            ocultarPopupEliminacion();
            var nota = data.Nota
            var color = "green";
            mostrarInfo(nota, color);
        } else {
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


function mostrarPopupEliminacion(id) {
    popupEliminacion.style.display = 'flex';
    document.getElementById('idElimina').innerHTML = `<input type="hidden" id="idCentroElimina" name="idCentroElimina" value="${id}">`;
}

function ocultarPopupEliminacion() {
    popupEliminacion.style.display = 'none';
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