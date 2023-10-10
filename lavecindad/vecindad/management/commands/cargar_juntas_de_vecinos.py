import json
from django.core.management.base import BaseCommand
from vecindad.models import JuntaDeVecinos  # Importa el modelo JuntaDeVecinos

class Command(BaseCommand):
    help = 'Carga datos desde un archivo JSON a la tabla JuntaDeVecinos'

    def handle(self, *args, **kwargs):
        ruta_json = 'C:/Users/javie/Downloads/lavecindad-main/lavecindad/vecindad/static/sedes.json'  # Reemplaza con la ruta correcta al archivo JSON

        with open(ruta_json, 'r', encoding='utf-8') as archivo_json:
            datos_json = json.load(archivo_json)
        
        print(datos_json)


        for elemento in datos_json:
            nuevo_registro = JuntaDeVecinos(
                id_sede=elemento['id-Sede'],
                comuna=elemento['Comuna'],
                sector_cerro=elemento['Sector/Cerro'],
                nombre=elemento['Nombre'],
                direccion=elemento['Dirección'],
                telefono=elemento['Telefono'],
                unidad_vecinal=elemento['Unidad Vecinal']
            )
            nuevo_registro.save()

        self.stdout.write(self.style.SUCCESS('Los datos se han cargado en la tabla JuntaDeVecinos exitosamente.'))
