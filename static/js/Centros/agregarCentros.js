const abrevInput = document.getElementById("abrev");
const descripcionInput = document.getElementById("descripcion");
const fechaAltaInput = document.getElementById("fecha-alta");
const usuarioAltaInput = document.getElementById("usuario-alta");
const fechaModificaInput = document.getElementById("fecha-modifica");
const usuarioModificaInput = document.getElementById("usuario-modifica");
const id = document.getElementById("id");

document.getElementById('nuevo-centro').addEventListener('click', function() {
    location.reload(); 
});

function validaciones() {
    const descripcionValor = descripcionInput.value.trim();
    const abrevValor = abrevInput.value.trim();
    if (descripcionValor === '') {
        return true;
    } 
    if (abrevValor === '') {
        return true;
    } 
    return false;
}

const guardarCentro = async () => {
    if (validaciones()) {
        var nota = 'Debe completar los campos.';
        var color = "red";
        mostrarInfo(nota, color);
    } else if (id.getAttribute('data-value') !== '0') {
        var nota = 'Debe generar un nuevo Centro de Costo.';
        var color = "red";
        mostrarInfo(nota, color);
    } else {
        try {
            const formData = new FormData();
            const abrev = document.getElementById("abrev").value.trim();
            const descripcion = document.getElementById("descripcion").value.trim();
            formData.append("abrev", abrev);
            formData.append("descripcion", descripcion);
            const options = {
                method: 'POST',
                headers: {
                    },
                body: formData
            };
            const response = await fetch("guarda-centro/", options);
            const data = await response.json();
            if(data.Message === "Success"){
                data.Datos.forEach((datos) => {
                    fechaAltaInput.value = datos.Fecha;
                    usuarioAltaInput.value = datos.Usuario;
                    fechaModificaInput.value = datos.FechaModifica;
                    usuarioModificaInput.value = datos.UserModifica;
                    id.textContent = 'ID: ' + datos.Id;
                    id.setAttribute('data-value', datos.Id);
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




