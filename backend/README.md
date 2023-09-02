uvicorn main:app --reload
http://localhost:5001




Crear un cliente (POST):
Payload para crear un nuevo cliente:

{
  "first_name": "María",
  "last_name": "Gómez",
  "date_of_birth": "1990-05-15",
  "gender": "Femenino",
  "address": "123 Calle Principal",
  "phone": "555-123-4567",
  "email": "maria@example.com"
}


Actualizar un cliente (PUT):
{
  "first_name": "Juan",
  "last_name": "Gómez",
  "date_of_birth": "1988-12-03"
}


Consultar detalles de un cliente (GET):
/patient_details/1


Eliminar un cliente (DELETE, GET):
/patients/1



ejecucion local


tener docker-compose instalado


una vez ejecutando comandos de docker-compose ejecutar en la raiz de este proyecto el comando

docker-compose up


esto expondra la APP al puerto 5001

http://localhost:5001/
donde podra visualizar el crud


o si no se tiene docker instalado , navegar hasta la carpeta backend, y crear un entorno virtual en ella

python3 -m venv venv


activar el entorno

source venv/bin/activate

luego instalar las dependencias

pip install -r requirements.txt

luego de esto ejecutar el scrip api-service.py

e ir la ruta http://localhost:5001/

:)
