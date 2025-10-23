const excelFilePath = document.getElementById('excelFilePath');
const excelFileUpload = document.getElementById('excelFileUpload');
const importButton = document.getElementById('importButton');
const popupCierra = document.getElementById('popup_duplicado');


document.getElementById('excelFilePath').addEventListener('click', function () {
    excelFileUpload.click();
});

document.getElementById('btn-confirmar-aceptar').addEventListener('click', function () {
    ocultarPopupCerrar();
});

excelFileUpload.addEventListener('change', function (event) {
    const file = event.target.files[0];
    if (file) {
        excelFilePath.value = file.name;
    }
});

importButton.addEventListener('click', function () {
    importaAdicionales();
});

const importaAdicionales = async () => {
    showSpinner();
    try {
        const formData = new FormData();
        const archivo = excelFileUpload.files[0];
        formData.append("excel", archivo);
        const options = {
            method: 'POST',
            headers: {},
            body: formData
        };
        const response = await fetch("subir-excel/", options);
        const data = await response.json();
        if (data.Message === "Success") {
            hideSpinner();
            var nota = data.Nota;
            var color = "green";
            showInfo(nota, color);
            excelFilePath.value = '';
            excelFileUpload.value = ''; 
        } else if (data.Message === "Duplicado") {
            hideSpinner();
            excelFilePath.value = '';
            excelFileUpload.value = ''; 
            document.getElementById('info_content').innerHTML = `
                <p>${data.Nota}</p>
            `;
            mostrarPopupCerrar();
        }else {
            hideSpinner();
            var nota = data.Nota;
            var color = "red";
            showInfo(nota, color);
        }
    } catch (error) {
        hideSpinner();
        var nota = "Se produjo un error al procesar la solicitud. " + error;
        var color = "red";
        showInfo(nota, color);
    }
}

function mostrarPopupCerrar() {
    popupCierra.style.display = 'flex';
}

function ocultarPopupCerrar() {
    popupCierra.style.display = 'none';
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

function showInfo(Message,Color) {
    document.getElementById("popup").classList.add("active");
    const colorBorderMsg = document.getElementById("popup");
    const mensaje = document.getElementById("mensaje-pop-up");
    colorBorderMsg.style.border = `2px solid ${Color}`;
    mensaje.innerHTML = `<p style="color: black; font-size: 13px;"><b>${Message}</b></p>`;

    setTimeout(() => {
        document.getElementById("popup").classList.remove("active");
    }, 5000);
}