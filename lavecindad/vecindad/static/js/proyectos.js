function crearContenedor() {
    // Obtén el valor del campo de entrada de archivo
    var inputImagen = document.getElementById("imagen");
    var imagen = inputImagen.files[0]; // Obtiene el archivo de imagen seleccionado
    var titulo = document.getElementById("titulo_noti").value;
    var texto = document.getElementById("texto_noti").value;

    // Verifica si se proporciona una imagen
    if (imagen) {
        // Crea un nuevo elemento div para el contenido
        var nuevoContenedor = document.createElement("div");
        nuevoContenedor.classList.add("contenedor-individual"); // Aplica la clase CSS

        // Crea un elemento img para mostrar la imagen
        var imagenElement = document.createElement("img");
        imagenElement.src = URL.createObjectURL(imagen); // Establece la URL de la imagen
        imagenElement.alt = "Imagen";
        nuevoContenedor.appendChild(imagenElement); // Agrega la imagen al contenedor

        // Agrega título y texto al nuevo elemento div
        var tituloElement = document.createElement("h2");
        tituloElement.textContent = titulo;
        nuevoContenedor.appendChild(tituloElement);

        var textoElement = document.createElement("p");
        textoElement.textContent = texto;
        nuevoContenedor.appendChild(textoElement);

        // Limpia los campos del formulario
        inputImagen.value = "";
        document.getElementById("titulo_noti").value = "";
        document.getElementById("texto_noti").value = "";

        // Agrega el nuevo contenido al contenedor principal
        var contenedorPrincipal = document.getElementById("contenedor-de-contenido");
        contenedorPrincipal.appendChild(nuevoContenedor);
    } else {
        alert("Debes seleccionar una imagen.");
    }
}