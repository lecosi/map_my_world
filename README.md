# Proyecto  map_my_world


## Objectivo
Se crea un sistema de almacenamiento de localizaciones de lugares
o sitios de importancia categorizados deqcuerdo a su tipo de interes, 
con el proposito de identificarlos y exponerlos al publico, no obstante, 
dicha funcionalidad deberia contar con herramientas de control para verificar 
que dichos lugares correspondan a su ubicacion y a la categoria en la que 
fueron asignados.

## Implementacion

- Se crea el servicio `/category` para registrar las categorias segun corresponda
- Se crea el servicio `/location` para registrar las ubicaciones de los lugares a almacenar
- Se crea el servicio `/exploration-recommender` para mostrar referencia sobre los lugares que aun no han sido explorados o verificados por el sistema

## Documentacion

1. Para conocer los API's deben ingresar a `/docs` en su servidor local.
2. Adjunto al proyecto hay una carpeta con un archivo en `postman` como ejemplo de los datos que se deben asignar en los servicios expuestos.

## pasos para correr el proyecto en local

1. Crear un entorno virtual `python3 -m venv nombre-de-ambiente`
2. Instalar dependencias `pip3 install -r requirements.txt`
3. Crear la base de datos y configurar su `.envrc` y `alembic.ini`
4. Aplicar las migraciones con alembic `alembic upgrade head`
5. Levantar el servidor `uvicorn main:app` o `uvicorn main:app --reload` en el caso de que necesiten autorecarga del servidor.