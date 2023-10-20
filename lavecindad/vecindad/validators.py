from django.core.exceptions import ValidationError

def validate_rut(value):
    """
    Valida el RUT chileno en diferentes formatos: con o sin puntos y con o sin guión.
    """
    # Eliminar puntos y guiones del RUT y convertirlo a mayúsculas
    value = value.replace(".", "").replace("-", "").upper()

    # Validar que el RUT tenga el formato correcto (8 o 9 dígitos seguidos del dígito verificador)
    if not value.isdigit() or not (8 <= len(value) <= 9):
        raise ValidationError("El RUT debe contener 8 o 9 dígitos seguidos del dígito verificador.")
