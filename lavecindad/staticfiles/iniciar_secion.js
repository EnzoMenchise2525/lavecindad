const btnSignIn = document.getElementById("sign-in"),
      btnSignUp = document.getElementById("sign-up"),
      formRegister = document.querySelector(".register"), 
      formLogin = document.querySelector(".login"); 

btnSignIn.addEventListener("click", e => {
    formRegister.classList.add("hide");
    formLogin.classList.remove("hide")
})

btnSignUp.addEventListener("click", e => {
    formLogin.classList.add("hide");
    formRegister.classList.remove("hide")
})


document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('registro-form');

    form.addEventListener('submit', function (event) {
        // Evitar que el formulario se envíe automáticamente
        event.preventDefault();

        // Realizar tus validaciones personalizadas aquí
            const username = form.querySelector('#id_username').value;
            const password1 = form.querySelector('#id_password1').value;
            const password2 = form.querySelector('#id_password2').value;

            // Ejemplo de validación: asegurarse de que las contraseñas coincidan
            if (password1 !== password2) {
                alert('Las contraseñas no coinciden. Por favor, inténtalo de nuevo.');
                return;
            }

            // Si todas las validaciones son exitosas, puedes enviar el formulario
            form.submit();
        });
    });


$(document).ready(function() {
    $('#select-sexo').select2({
        placeholder: "Sexo",
        minimumResultsForSearch: -1, // Esto oculta la barra de búsqueda
    });
});

