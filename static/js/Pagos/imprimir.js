const selectAllCheckbox = document.getElementById("selectAll");
const inicio = document.getElementById("fechaInicio");
const final = document.getElementById("fechaFinal");
const liquidaciones = document.getElementById("selector_liquidacion");
const imprimirPlanilla = document.getElementById("imprimir_planilla");
const imprimirMemo = document.getElementById("imprimir_memo");
const imprimirRecibo = document.getElementById("imprimir_recibo");
const cantidadTotal = document.getElementById("cantidad_total");
const importeTotal = document.getElementById("importe_total");

window.addEventListener("load", async () => {
    listarLiquidaciones();
});

document.getElementById('imprimir_planilla').addEventListener('click', function () {
    const codigo = 'P';
    retornaPlanillas(codigo);
});

document.getElementById('imprimir_memo').addEventListener('click', function () {
    const codigo = 'M';
    retornaMemo(codigo);
});

document.getElementById('imprimir_recibo').addEventListener('click', function () {
    const codigo = 'R';
    retornaRecibos(codigo);
});

selector_liquidacion.addEventListener("change", (event) => {
    llenarTablaContenidoLiquidaciones();
    document.getElementById('detalles_contenido_liquidaciones').innerHTML = ``;
    cantidadTotal.textContent = 'CANTIDAD TOTAL: ' + ' ';
    cantidadTotal.setAttribute('data-value', '');
    importeTotal.textContent = 'IMPORTE TOTAL: ' + ' ';
    importeTotal.setAttribute('data-value', ' ');
});

document.getElementById('buscaImprimir').addEventListener('click', function () {
    listarLiquidaciones();
    document.getElementById('detalles_contenido_liquidaciones').innerHTML = ``;
    cantidadTotal.textContent = 'CANTIDAD TOTAL: ' + ' ';
    cantidadTotal.setAttribute('data-value', '');
    importeTotal.textContent = 'IMPORTE TOTAL: ' + ' ';
    importeTotal.setAttribute('data-value', ' ');
    selectAllCheckbox.checked = false;
});

fechaInicio.addEventListener("change", (event) => {
    listarLiquidaciones();
    document.getElementById('detalles_contenido_liquidaciones').innerHTML = ``;
    cantidadTotal.textContent = 'CANTIDAD TOTAL: ' + ' ';
    cantidadTotal.setAttribute('data-value', '');
    importeTotal.textContent = 'IMPORTE TOTAL: ' + ' ';
    importeTotal.setAttribute('data-value', ' ');
    selectAllCheckbox.checked = false;
});

fechaFinal.addEventListener("change", (event) => {
    listarLiquidaciones();
    document.getElementById('detalles_contenido_liquidaciones').innerHTML = ``;
    cantidadTotal.textContent = 'CANTIDAD TOTAL: ' + ' ';
    cantidadTotal.setAttribute('data-value', '');
    importeTotal.textContent = 'IMPORTE TOTAL: ' + ' ';
    importeTotal.setAttribute('data-value', ' ');
    selectAllCheckbox.checked = false;
});

const choiceLiquidacion = new Choices('#selector_liquidacion', {
    allowHTML: true,
    shouldSort: false,
    searchPlaceholderValue: 'Escriba para buscar..',
    itemSelectText: ''
});

function updateButtonState() {
    const checkboxes = document.querySelectorAll(".input-checkbox:not(#selectAll):checked");
    const anyChecked = Array.from(checkboxes).some(checkbox => checkbox.checked);
    if (anyChecked) {
        imprimirPlanilla.disabled = false;
        imprimirPlanilla.classList.add("enabled");
        imprimirMemo.disabled = false;
        imprimirMemo.classList.add("enabled");
        imprimirRecibo.disabled = false;
        imprimirRecibo.classList.add("enabled");
        llenarItemsTablaContenido();
    } else {
        imprimirPlanilla.disabled = true;
        imprimirPlanilla.classList.remove("enabled");
        imprimirMemo.disabled = true;
        imprimirMemo.classList.remove("enabled");
        imprimirRecibo.disabled = true;
        imprimirRecibo.classList.remove("enabled");
        document.getElementById('detalles_contenido_liquidaciones').innerHTML = ``;
        cantidadTotal.textContent = 'CANTIDAD TOTAL: ' + ' ';
        cantidadTotal.setAttribute('data-value', '');
        importeTotal.textContent = 'IMPORTE TOTAL: ' + ' ';
        importeTotal.setAttribute('data-value', ' ');
    }
}

selectAllCheckbox.addEventListener("change", function () {
    const checkboxes = document.querySelectorAll(".input-checkbox");
    checkboxes.forEach(checkbox => {
        checkbox.checked = selectAllCheckbox.checked;
    });
});


const today = new Date();
const firstDayOfMonth = new Date(today.getFullYear(), today.getMonth(), 1);


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

const listarLiquidaciones = async () => {
    try {
        const formData = new FormData();
        formData.append("Inicio", inicio.value);
        formData.append("Final", final.value);
        const options = {
            method: 'POST',
            headers: {},
            body: formData
        };
        const response = await fetch("listar-liquidaciones/", options);
        const data = await response.json();
        if (data.Message === "Success") {
            let resultLiquidaciones = [];
            resultLiquidaciones.push();
            data.Liquidaciones.forEach((datos) => {
                resultLiquidaciones.push({
                    value: datos.IdLiquidacion,
                    label: datos.Liquidacion
                });
            });
            choiceLiquidacion.clearChoices();
            choiceLiquidacion.setChoices([{ value: '', label: 'SELECCIONE UNA LIQUIDACIÓN', selected: true, disabled: true }].concat(resultLiquidaciones), 'value', 'label', true);
            document.getElementById('imprimir-lista-liquidaciones').innerHTML = ``;
        } else {
            document.getElementById('imprimir-lista-liquidaciones').innerHTML = ``;
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

const llenarTablaContenidoLiquidaciones = async () => {
    showSpinner();
    try {
        const formData = new FormData();
        formData.append("Liquidacion", liquidaciones.value);
        const options = {
            method: 'POST',
            headers: {
            },
            body: formData
        };

        const response = await fetch("listar-centro-cantidad-importe/", options);
        const data = await response.json();
        if (data.Message == "Success") {
            let dato = ``;
            data.Datos.forEach((datos) => {
                dato += `
                <tr>
                    <th><input class="input-checkbox checkbox" type="checkbox" id="idCheck" name="idCheck"
                            value="${datos.Abrev}"></th>
                    <td>${datos.Centro}</td>
                    <td class="fila-cantidad">${datos.Cantidad}</td>
                    <td>${datos.Importe}</td>
                </tr>
                `
            });
            document.getElementById('imprimir-lista-liquidaciones').innerHTML = dato;
            const checkboxes = document.querySelectorAll(".input-checkbox");
            checkboxes.forEach(checkbox => {
                checkbox.addEventListener("change", function () {
                    updateButtonState()
                });
            });
            const individualCheckboxes = document.querySelectorAll(".input-checkbox");
            individualCheckboxes.forEach(checkbox => {
                checkbox.addEventListener("change", function () {
                    if (!checkbox.checked) {
                        selectAllCheckbox.checked = false;
                    } else {
                        const allChecked = Array.from(individualCheckboxes).every(checkbox => checkbox.checked);
                        selectAllCheckbox.checked = allChecked;
                    }
                });
            });
            hideSpinner();
        } else {
            document.getElementById('imprimir-lista-liquidaciones').innerHTML = ``;
            hideSpinner();
            var nota = data.Nota
            var color = "red";
            mostrarInfo(nota, color);
        }
    } catch (error) {
        hideSpinner();
        var nota = "Se produjo un error al procesar la solicitud. " + error;
        var color = "red";
        mostrarInfo(nota, color);
    }
};


const llenarItemsTablaContenido = async () => {
    showSpinner();
    try {
        const formData = new FormData();
        formData.append('Liquidacion', liquidaciones.value);
        const checkboxes = document.querySelectorAll('.input-checkbox:not(#selectAll):checked');
        checkboxes.forEach(checkbox => {
            if (checkbox.checked) {
                formData.append('Centros', checkbox.value);
            }
        });
        const options = {
            method: 'POST',
            headers: {
            },
            body: formData
        };

        const response = await fetch("listar-items-cantidad-importe/", options);
        const data = await response.json();
        if (data.Message == "Success") {
            let dato = ``;
            data.Datos.forEach((datos) => {
                dato += `
                <tr>
                    <td>${datos.Legajo}</td>
                    <td>${datos.Nombre}</td>
                    <td>${datos.Centro}</td>
                    <td class="fila-cantidad">${datos.Cantidad}</td>
                    <td>${datos.Importe}</td>
                    <td class="fila-opciones">
                        <button class="btn-icon details-btn" style="cursor: not-allowed;">
                            <i class="fas fa-info-circle" style="color: grey;" disabled></i>
                        </button>
                        <button class="btn-icon print-btn" onclick="legajo('${datos.Legajo}','${datos.Abrev}');">
                            <i class="fas fa-print"></i>
                        </button>
                    </td>
                </tr>
                `
            });
            document.getElementById('detalles_contenido_liquidaciones').innerHTML = dato;

            cantidadTotal.textContent = 'CANTIDAD DE CONCEPTOS: ' + data.CantTotal;
            cantidadTotal.setAttribute('data-value', data.CantTotal);
            importeTotal.textContent = 'IMPORTE TOTAL: ' + data.ImporTotal;
            importeTotal.setAttribute('data-value', data.ImporTotal);
            hideSpinner();
        } else {
            document.getElementById('detalles_contenido_liquidaciones').innerHTML = ``;
            hideSpinner();
            var nota = data.Nota
            var color = "red";
            mostrarInfo(nota, color);
        }
    } catch (error) {
        hideSpinner();
        var nota = "Se produjo un error al procesar la solicitud. " + error;
        var color = "red";
        mostrarInfo(nota, color);
    }
};

const retornaMemo = async (codigo) => {
    showSpinner();
    try {
        const formData = new FormData();
        formData.append("Liquidacion", liquidaciones.value);
        formData.append("Codigo", codigo);
        formData.append("Legajo", '');
        const checkboxes = document.querySelectorAll('.input-checkbox:not(#selectAll):checked');
        checkboxes.forEach(checkbox => {
            if (checkbox.checked) {
                formData.append('Centros', checkbox.value);
            }
        });
        const options = {
            method: 'POST',
            headers: {
            },
            body: formData
        };

        const response = await fetch("imprimir-recibo-planilla-memo/", options);
        const contentType = response.headers.get('content-type');
        hideSpinner();
        if (contentType && contentType.includes('application/pdf')) {
            const blob = await response.blob();
            const pdfURL = URL.createObjectURL(blob);
            window.open(pdfURL);
        } else {
            const data = await response.json();
            var nota = data.Nota;
            var color = "red";
            mostrarInfo(nota, color);
        }
    } catch (error) {
        hideSpinner();
        var nota = "Se produjo un error al procesar la solicitud. " + error;
        var color = "red";
        mostrarInfo(nota, color);
    }
};


const retornaPlanillas = async (codigo) => {
    showSpinner();
    try {
        const formData = new FormData();
        formData.append("Liquidacion", liquidaciones.value);
        formData.append("Codigo", codigo);
        formData.append("Legajo", '');
        const checkboxes = document.querySelectorAll('.input-checkbox:not(#selectAll):checked');
        checkboxes.forEach(checkbox => {
            if (checkbox.checked) {
                formData.append('Centros', checkbox.value);
            }
        });
        const options = {
            method: 'POST',
            headers: {
            },
            body: formData
        };
        const response = await fetch("imprimir-recibo-planilla-memo/", options);
        const contentType = response.headers.get('content-type');
        hideSpinner();
        if (contentType && contentType.includes('application/pdf')) {
            const blob = await response.blob();
            const pdfURL = URL.createObjectURL(blob);
            window.open(pdfURL);
        } else {
            const data = await response.json();
            var nota = data.Nota;
            var color = "red";
            mostrarInfo(nota, color);
        }
    } catch (error) {
        hideSpinner();
        var nota = "Se produjo un error al procesar la solicitud. " + error;
        var color = "red";
        mostrarInfo(nota, color);
    }
};



const retornaRecibos = async (codigo) => {
    showSpinner();
    try {
        const formData = new FormData();
        formData.append("Liquidacion", liquidaciones.value);
        formData.append("Codigo", codigo);
        formData.append("Legajo", '');
        const checkboxes = document.querySelectorAll('.input-checkbox:not(#selectAll):checked');
        checkboxes.forEach(checkbox => {
            if (checkbox.checked) {
                formData.append('Centros', checkbox.value);
            }
        });
        const options = {
            method: 'POST',
            headers: {
            },
            body: formData
        };
        const response = await fetch("imprimir-recibo-planilla-memo/", options);
        const contentType = response.headers.get('content-type');
        hideSpinner();
        if (contentType && contentType.includes('application/pdf')) {
            const blob = await response.blob();
            const pdfURL = URL.createObjectURL(blob);
            window.open(pdfURL);
        } else {
            const data = await response.json();
            var nota = data.Nota;
            var color = "red";
            mostrarInfo(nota, color);
        }
    } catch (error) {
        hideSpinner();
        var nota = "Se produjo un error al procesar la solicitud. " + error;
        var color = "red";
        mostrarInfo(nota, color);
    }
};


function legajo(legajo,abrev){
    const codigo = 'R';
    recibo(codigo,legajo,abrev);
}

const recibo = async (codigo,legajo,abrev) => {
    showSpinner();
    try {
        const formData = new FormData();
        formData.append("Liquidacion", liquidaciones.value);
        formData.append("Codigo", codigo);
        formData.append("Legajo", legajo);
        formData.append("Centro", abrev);
        // const checkboxes = document.querySelectorAll('.input-checkbox:not(#selectAll):checked');
        // checkboxes.forEach(checkbox => {
        //     if (checkbox.checked) {
        //         formData.append('Centros', checkbox.value);
        //     }
        // });
        const options = {
            method: 'POST',
            headers: {
            },
            body: formData
        };
        const response = await fetch("imprimir-recibo-planilla-memo/", options);
        const contentType = response.headers.get('content-type');
        hideSpinner();
        if (contentType && contentType.includes('application/pdf')) {
            const blob = await response.blob();
            const pdfURL = URL.createObjectURL(blob);
            window.open(pdfURL);
        } else {
            const data = await response.json();
            var nota = data.Nota;
            var color = "red";
            mostrarInfo(nota, color);
        }
    } catch (error) {
        hideSpinner();
        var nota = "Se produjo un error al procesar la solicitud. " + error;
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
