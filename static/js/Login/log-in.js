

const loginButton = document.getElementById("login-button");
const usernameInput = document.getElementById("username");
const passwordInput = document.getElementById("password");




document.getElementById('login-button').addEventListener('click', function() {
    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;
    fetch('salary/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-Requested-With': 'XMLHttpRequest'
        },
        body: 'username=' + encodeURIComponent(username) + '&password=' + encodeURIComponent(password)
    })
    .then(response => response.json())
    .then(data => {
        if (data.Message == 'success') {
            window.location.href = '/';
        } else if (data.Message == 'Change') {
            popup.style.display = "flex";
        } else {
            var Message = data.data;
            var Color = 'Red';
            mostrarInfo(Message,Color)
        }
    })
    .catch(error => {
        var nota = "Se produjo un error al procesar la solicitud. "  + error;
        var color = "red";
        mostrarInfo(nota, color);
    });
});


passwordInput.addEventListener("keyup", function(event) {
    if (event.key === "Enter") {
      loginButton.click();
    }
});

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