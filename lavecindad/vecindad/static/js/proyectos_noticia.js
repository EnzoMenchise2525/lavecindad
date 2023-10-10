function crearNoticia() {
    // Obtener los valores de los campos del formulario
    var titulo = document.getElementById("titulo_noticia").value;
    var texto = document.getElementById("texto_noticia").value;
    var imagen = document.getElementById("imagen_noticia").files[0];
    var servicio = document.getElementById("Servicio").value;
    var ciudad = document.getElementById("texto_ciudad").value;
    var tipoServicio = document.getElementById("texto_tipo_servicio").value;

    // Verificar si se ha seleccionado una imagen
    if (!imagen) {
        alert("Por favor, seleccione una imagen antes de crear la noticia.");
        return; // Detener la función si no hay imagen
    }

    // Crear un elemento de noticia
    var noticia = document.createElement("div");
    noticia.className = "noticia";

    // Agregar la imagen si se proporciona
    if (imagen) {
        var img = document.createElement("img");
        img.src = URL.createObjectURL(imagen);
        img.style.maxWidth = "100%";
        noticia.appendChild(img);
    }

    // Agregar contenido a la noticia en el orden deseado
    noticia.innerHTML += `
        <h2>${titulo}</h2>
        <p> ${servicio}</p>
        <p>${ciudad}</p>
        <p>${tipoServicio}</p>
        <p>${texto}</p>
    `;

    // Reemplazar la noticia anterior con la nueva
    var contenedorNoticia = document.getElementById("contenedor-de-noticia");
    contenedorNoticia.innerHTML = ''; // Limpiar el contenedor anterior
    contenedorNoticia.appendChild(noticia);
}