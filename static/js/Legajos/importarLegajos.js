document.getElementById('jsonFilePath').addEventListener('click', function () {
    document.getElementById('jsonFileUpload').click();
});

document.getElementById('jsonFileUpload').addEventListener('change', function (event) {
    const file = event.target.files[0];
    if (file) {
        document.getElementById('jsonFilePath').value = file.name;
    }
});

document.getElementById('importButton').addEventListener('click', function () {
    const fileInput = document.getElementById('jsonFileUpload');
    const file = fileInput.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function (e) {
            const jsonContent = e.target.result;
            importaLegajos();
        };
        reader.readAsText(file);
    } else {
        var nota = 'Por favor, seleccione un archivo JSON.';
        var color = "red";
        mostrarInfo(nota, color);   
    }
});


const importaLegajos = async () => {
    showSpinner();
    try {
        const formData = new FormData();
        const archivoJSON = document.getElementById("jsonFileUpload").files[0];
        formData.append("archivoJSON", archivoJSON);
        const options = {
            method: 'POST',
            headers: {
                },
            body: formData
        };
        const response = await fetch("surbir-json/", options);
        const data = await response.json();
        if(data.Message === "Success"){
            hideSpinner();
            var nota = data.Nota;
            var color = "green";
            mostrarInfo(nota, color);   
        } else {
            hideSpinner();
            var nota = data.Nota;
            var color = "red";
            mostrarInfo(nota, color);
        }
    } catch (error) {
        hideSpinner();
        var nota = "Se produjo un error al procesar la solicitud. "  + error;
        var color = "red";
        mostrarInfo(nota, color);
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





function mostrarInfo(Message,Color) {
    document.getElementById("popup").classList.add("active");
    const colorBorderMsg = document.getElementById("popup");
    const mensaje = document.getElementById("mensaje-pop-up");
    colorBorderMsg.style.border = `2px solid ${Color}`;
    mensaje.innerHTML = `<p style="color: black; font-size: 13px;"><b>${Message}</b></p>`;

    setTimeout(() => {
        document.getElementById("popup").classList.remove("active");
    }, 5000);
}