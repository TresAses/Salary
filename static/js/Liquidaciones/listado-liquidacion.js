const inicio = document.getElementById("fechaInicio");
const final = document.getElementById("fechaFinal");
const estados = document.getElementById("selector_estados");
const cerrar = document.getElementById("cerrar");
const checkboxes = document.querySelectorAll(".input-checkbox");
const popupCierra = document.getElementById('popup-Cierra');

const idMod = document.getElementById('id_a_act');
const carpetaMod = document.getElementById('carpeta_act');
const fechaAlta = document.getElementById('fechaA_act');
const userAlta = document.getElementById('userA_act');
const fechaMod = document.getElementById('fechaM_act');
const userMod = document.getElementById('userM_act');
const estadoBtn = document.getElementById('estado_act');
const today = new Date();
const firstDayOfMonth = new Date(today.getFullYear(), today.getMonth(), 1);

window.addEventListener("load", async () => {
    cerrar.disabled = true;
    cerrar.classList.remove("enabled");
});

selector_estados.addEventListener("change", (event) => {
    llenarTablaLiquidaciones();
});

fechaInicio.addEventListener("change", (event) => {
    llenarTablaLiquidaciones();
});

fechaFinal.addEventListener("change", (event) => {
    llenarTablaLiquidaciones();
});


const formatDate = (date) => {
    const day = String(date.getDate()).padStart(2, '0');
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const year = date.getFullYear();
    return `${year}-${month}-${day}`;
};

flatpickr('#fechaInicio', {
    dateFormat: 'Y-m-d',
    altInput: true,
    altFormat: 'j F , Y',
    defaultDate: formatDate(firstDayOfMonth),
    placeholder: 'Selecciona una fecha',
});
flatpickr('#fechaFinal', {
    dateFormat: 'Y-m-d',
    altInput: true,
    altFormat: 'j F , Y',
    defaultDate: 'today',
    placeholder: 'Selecciona una fecha',
});

const choiceEstados = new Choices('#selector_estados', {
    allowHTML: true,
    shouldSort: false,
    searchPlaceholderValue: 'Escriba para buscar..',
    itemSelectText: ''
});

document.getElementById('cerrar').addEventListener('click', function () {
    mostrarPopupCerrar();
});

const llenarTablaLiquidaciones = async () => {
    try {
        const formData = new FormData();
        formData.append("Inicio", inicio.value);
        formData.append("Final", final.value);
        formData.append("Estado", estados.value);
        const options = {
            method: 'POST',
            headers: {
            },
            body: formData
        };

        const response = await fetch("llenar-tabla-liquidacion/", options);
        const data = await response.json();
        if (data.Message == "Success") {
            let dato = ``;
            data.Datos.forEach((datos) => {
                dato += `
                
                <tr>
                <td><input class="input-checkbox checkbox" type="checkbox" id="idCheck" name="idCheck"
                    value="${datos.IdLiquidacion}" ${datos.Letra === 'L' || datos.Letra === 'C' ? 'disabled' : ''}></td>
                <td class="fila-id">${datos.IdLiquidacion}</td>
                <td class="fila-descripcion">${datos.Nombre}</td>
                <td class="fila-estado">
                    <div class="estado" style="background-color: ${datos.Color};">${datos.Estado}</div>
                </td>
                <td class="fila-alta">${datos.Fecha}</td>
                <td class="fila-user">${datos.Usuario}</td>
                <td class="fila-modificacion">${datos.FechaModifica}</td>
                <td class="fila-user-modifica">${datos.UsuarioModifica}</td>
                <td class="fila-opciones">
                    <button class="btn-icon edit-btn" onclick="activo(${datos.IdLiquidacion});">
                        <i class="fas fa-edit"></i>
                    </button>
                </td>
            </tr>
                `
            });
            document.getElementById('listado-tabla-liquidaciones').innerHTML = dato;
            const checkboxes = document.querySelectorAll(".input-checkbox");
            checkboxes.forEach(checkbox => {
                checkbox.addEventListener("change", function () {
                    const anyChecked = Array.from(checkboxes).some(checkbox => checkbox.checked);
                    if (anyChecked) {
                        cerrar.disabled = false;
                        cerrar.classList.add("enabled");
                    } else {
                        cerrar.disabled = true;
                        cerrar.classList.remove("enabled");
                    }
                });
            });
        } else {
            document.getElementById('listado-tabla-liquidaciones').innerHTML = ``;
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



function mostrarPopupCerrar() {
    popupCierra.style.display = 'flex';
}

function ocultarPopupCerrar() {
    popupCierra.style.display = 'none';
}


document.getElementById('cerrar-pop').addEventListener('click', function () {
    document.getElementById('pop-up-overlay').classList.remove('active');
    document.getElementById('pop-up-actualizaLiquidacion').classList.remove('active');
});


const activo = async (IdLiquidacion) => {
    try {
        const formData = new FormData();
        formData.append("IdLiquidacion", IdLiquidacion);
        const options = {
            method: 'POST',
            headers: {},
            body: formData
        };
        const response = await fetch("datos-modifica-liquidacion/", options);
        const data = await response.json();
        if (data.Message === "Success") {
            idMod.textContent = 'ID: ' + data.IdLiquidacion;
            idMod.setAttribute('data-value', data.IdLiquidacion);
            carpetaMod.value = data.Nombre;
            fechaAlta.value = data.FechaAlta;
            userAlta.value = data.UsuarioAlta;
            fechaMod.value = data.FechaModifica;
            userMod.value = data.UsuarioModifica;
            estadoBtn.style.backgroundColor = data.Color;
            estadoBtn.value = data.Estado;
            estadoBtn.textContent = data.Letras;
            document.getElementById('pop-up-actualizaLiquidacion').classList.add('active');
            document.getElementById('pop-up-overlay').classList.add('active');
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

function toggleEstado(button) {
    if (button.value === "C") {
        button.value = "A";
        button.textContent = "ABIERTA";
        button.style.backgroundColor = "green";
    } else {
        button.value = "C";
        button.textContent = "CERRADA";
        button.style.backgroundColor = "red";
    }

}

document.getElementById('btn-confirmar-cierre').addEventListener('click', function () {
    cierraLiquidaciones();
});


const cierraLiquidaciones = async () => {
    try {
        const formData = new FormData();
        const checkboxes = document.querySelectorAll('.input-checkbox:not(#selectAll):checked');
        checkboxes.forEach(checkbox => {
            if (checkbox.checked) {
                formData.append('liquidaciones', checkbox.value);
            }
        });
        const options = {
            method: 'POST',
            headers: {
            },
            body: formData
        };
        const response = await fetch("cierre-masivo-liquidacion/", options);
        const data = await response.json();
        if (data.Message === "Success") {
            ocultarPopupCerrar();
            var nota = data.Nota;
            var color = "green";
            mostrarInfo(nota, color);
            cerrar.disabled = true;
            cerrar.classList.remove("enabled");
            llenarTablaLiquidaciones();
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
};

document.getElementById('actualiza-pop').addEventListener('click', function () {
    actualizaLiquidacion();
});

const actualizaLiquidacion = async () => {
    if (carpetaMod.value.trim() === '') {
        var nota = 'Debe Completar los Campos.';
        var color = "red";
        mostrarInfo(nota, color);
    } else {
        try {
            const formData = new FormData();
            formData.append("IdLiquidacion", idMod.getAttribute('data-value'));
            formData.append("Carpeta", carpetaMod.value);
            formData.append("Estado", estadoBtn.value);
            const options = {
                method: 'POST',
                headers: {},
                body: formData
            };
            const response = await fetch("actualiza-liquidacion/", options);
            const data = await response.json();
            if (data.Message === "Success") {
                idMod.textContent = 'ID: ' + data.IdLiquidacion;
                idMod.setAttribute('data-value', data.IdLiquidacion);
                carpetaMod.value = data.Nombre;
                fechaAlta.value = data.FechaAlta;
                userAlta.value = data.UsuarioAlta;
                fechaMod.value = data.FechaModifica;
                userMod.value = data.UsuarioModifica;
                estadoBtn.style.backgroundColor = data.Color;
                estadoBtn.value = data.Estado;
                estadoBtn.textContent = data.Letras;
                var nota = data.Nota;
                var color = "green";
                mostrarInfo(nota, color);
                llenarTablaLiquidaciones();
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
