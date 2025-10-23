const idStrong = document.getElementById("id-l");
const liquidacion = document.getElementById("carpeta");
const fechaA = document.getElementById("fechaA");
const userA = document.getElementById("userA");
const fechaM = document.getElementById("fechaM");
const userM = document.getElementById("userM");


function validaciones() {
    const valueL = liquidacion.value.trim();
    if (valueL === '') {
        return true;
    }
    return false;
}

const guardarLiquidacion = async () => {
    if (validaciones()) {
        var nota = 'Debe completar los campos.';
        var color = "red";
        mostrarInfo(nota, color);
    } else if (idStrong.getAttribute('data-value') !== '0') {
        var nota = 'Debe generar un nueva Liquidación.';
        var color = "red";
        mostrarInfo(nota, color);
    } else {
        try {
            const formData = new FormData();
            formData.append("carpeta", liquidacion.value);
            formData.append("estado", 'A');
            const options = {
                method: 'POST',
                headers: {
                },
                body: formData
            };
            const response = await fetch("guarda-liquidacion/", options);
            const data = await response.json();
            if (data.Message === "Success") {
                idStrong.textContent = 'ID: ' + data.ID
                idStrong.setAttribute('data-value', data.ID);
                fechaA.value = data.FechaAlta;
                userA.value = data.Usuario;
                fechaM.value = data.FechaModifica;
                userM.value = data.UserModifica;
                var nota = data.Nota;
                var color = "green";
                mostrarInfo(nota, color);
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

document.getElementById('nueva-liquidacion').addEventListener('click', function () {
    location.reload();
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
