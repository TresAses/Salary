
window.addEventListener("load", async () => {
    await listarCentros();
});

selector_centros.addEventListener("change", (event) => {
    document.getElementById('tabla-listado-legajos').innerHTML = ``;
    listarLegajos();
});

selector_legajos.addEventListener("change", (event) => {
    llenarTablaLegajos();
});


const choices = new Choices('#selector_centros', {
    allowHTML: true,
    shouldSort: false,
    searchPlaceholderValue: 'Escriba para buscar..',
    itemSelectText: ''
});

const listarCentros = async () => {
    try {
        const response = await fetch("llenar-combox-centros/");
        const data = await response.json();
        if (data.Message === "Success") {
            let result = [];
            result.push();
            data.Datos.forEach((datos) => {
                result.push({ value: datos.IdAbrev, label: datos.Descripcion });
            });
            choices.setChoices(result, 'value', 'label', true);
        } else {
            var nota = data.Nota;
            var color = "red";
            mostrarInfo(nota, color);
        }
    } catch (error) {
        console.log(error)
        var nota = "Se produjo un error al procesar la solicitud.";
        var color = "red";
        mostrarInfo(nota, color);
    }
}

const choicesLegajos = new Choices('#selector_legajos', {
    allowHTML: true,
    shouldSort: false,
    placeholder: true,
    placeholderValue: 'SELECCIONE UN LEGAJO',
    searchPlaceholderValue: 'Escriba para buscar..',
    itemSelectText: ''
});

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
        const response = await fetch("llenar-combox-legajos/", options);
        const data = await response.json();
        if (data.Message === "Success") {
            let result = [];
            data.Datos.forEach((datos) => {
                result.push({ value: datos.Legajo, label: datos.Nombre });
            });
            choicesLegajos.clearChoices();
            choicesLegajos.setChoices(result, 'value', 'label', true);
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

const llenarTablaLegajos = async () => {
    showSpinner();
    try {
        const formData = new FormData();
        const IdLegajo = document.getElementById("selector_legajos").value;
        let idCentro = document.getElementById("selector_centros").value;
        formData.append("IdLegajo", IdLegajo);
        formData.append("Abrev", idCentro);
        const options = {
            method: 'POST',
            headers: {
            },
            body: formData
        };

        const response = await fetch("llenar-tabla-legajos/", options);
        const data = await response.json();
        if (data.Message == "Success") {
            let dato = ``;
            data.Datos.forEach((datos) => {
                dato += `
                <tr>
                    <td class="fila-legajo">${datos.Legajo}</td>
                    <td class="fila-nombres">${datos.Nombre}</td>
                    <td class="fila-tipo">${datos.Tipo}</td>
                    <td class="fila-numero">${datos.DNI}</td>
                    <td class="fila-fecha-nac">${datos.Nac}</td>
                    <td class="fila-sexo">${datos.Sexo}</td>
                    <td class="fila-abrev">${datos.Abrev}</td>
                    <td class="fila-centro">${datos.Centro}</td>
                </tr>
                `
            });
            document.getElementById('tabla-listado-legajos').innerHTML = dato;
            hideSpinner();
        } else {
            document.getElementById('tabla-listado-legajos').innerHTML = ``;
            hideSpinner();
            var nota = data.Nota
            var color = "red";
            mostrarInfo(nota, color);
        }
    } catch (error) {
        hideSpinner();
        var nota = "Se produjo un error al procesar la solicitud.";
        var color = "red";
        mostrarInfo(nota, color);
    }
};
























































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
