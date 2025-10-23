
const descripcionInput = document.getElementById("descripcion-nuevo-concepto");
const fechaAltaInput = document.getElementById("fecha-alta");
const usuarioAltaInput = document.getElementById("usuario-alta");
const fechaModificaInput = document.getElementById("fecha-modifica");
const usuarioModificaInput = document.getElementById("usuario-modifica");
const idStrong = document.getElementById("id-sc");

function validaciones() {
    const descripcionValor = descripcionInput.value.trim();
    if (descripcionValor === '') {
        return true;
    } 
    return false;
}


const guardarConcepto = async () => {
    if (validaciones()) {
        var nota = 'Debe completar los campos.';
        var color = "red";
        mostrarInfo(nota, color);
    } else if (idStrong.getAttribute('data-value') !== '0') {
        var nota = 'Debe generar un nuevo Concepto.';
        var color = "red";
        mostrarInfo(nota, color);
    } else {
        try {
            const formData = new FormData();
            const descripcionNuevoConcepto = document.getElementById("descripcion-nuevo-concepto").value.trim();
            formData.append("descripcionNuevoConcepto", descripcionNuevoConcepto);
            const options = {
                method: 'POST',
                headers: {
                    },
                body: formData
            };
            const response = await fetch("guarda-concepto/", options);
            const data = await response.json();
            if(data.Message === "Success"){
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



/// NUEVO CONCEPTO
document.getElementById('nuevo-concepto').addEventListener('click', function() {
    location.reload(); 
});




































