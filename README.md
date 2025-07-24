# 🗺️ Map My World - Geolocalización con FastAPI y Docker

Este proyecto es una Rest API desarrollada con **FastAPI**, que permite administrar ubicaciones geográficas 
categorizadas y obtener recomendaciones sobre las mismas según el criterio del administrador. 

El proyecto está dockerizado para facilitar el despliegue y el desarrollo.

## Puedes encontrar el proyecto ya desplegado en AWS Cloud
El mismo fue desplegado para comodidad
de la corrección del proyecto, se encuentra con un EC2 linux al cual se le desplegaron los contenedores
de Docker y se editaron las reglas de los securities groups para que cualquiera pueda acceder a él.
Puedes acceder a la API en el siguiente enlace:


## Si se desea realizar la instalación en local, puede seguir con las siguientes indicaciones abajo descritas

Para evitar conflictos de dependencias y versiones se recomienda no utilizar una versión anterior
de Python a la 3.10, ya que el proyecto utiliza algunas características de Python 3.10 y 3.11
asimismo las relaciones de shema y modelo se encuentran definidas con SQLAlchemy y Pydantic.
Bajo la estructura de un proyecto FastAPI adaptada a python 3.10 o superior.

Por estos motivos se recomienda probar la API en docker, ya que el mismo contiene 
una imagen ligera de Python 3.11 y todas las dependencias necesarias para correr la aplicación.

## 🚀 Características principales

- Crear ubicaciones con coordenadas, nombre, descripción y categorías asociadas.
- Crear y listar categorías.
- Asociar ubicaciones con categorías.
- Marcar combinaciones de ubicación y categoría como "revisadas".
- Obtener recomendaciones frescas: hasta 10 combinaciones ubicación-categoría que no han sido revisadas en los últimos 30 días.
- Interfaz básica (Sandbox) con mapa utilizando HTML y Jinja2.
- Base de datos SQLite.
- Contenedor Docker preconfigurado con Docker Compose.
- Script generador de locaciones y categorias de pruebas automatico

---

# MÉTODOS PARA LA INSTALACIÓN
## Para la instalación y utilización de la API, puedes elegir entre dos opciones: con Docker o sin Docker.
```debes utilizar solo una de las dos opciones, no es necesario utilizar ambas.```


## 🐳 1) Con Docker & Docker Compose

### 📄 `Dockerfile`


Si ya tienes instalado docker, para correr la rest api, solo necesitas hacer lo siguiente:

#### Navega a tu carpeta del proyecto asegurandote que estas a nivel de la ubicacion del 
docker-compose.yml y el Dockerfile:

```bash
cd /ruta/a/map_my_world
```

#### Puedes asegurarte listando los archivos en la carpeta:
```bash
ls -la
```
Esto te mostrará las carpetas y archivos en tu ubicación
algo parecido a esto:

```bash
db                  Dockerfile  main.py  map_my_world.egg-info  __pycache__     README.md         routes   templates
docker-compose.yml  LICENSE     map.db   models                 pyproject.toml  requirements.txt  schemas  utils
```
#### Seguidamente ejecuta el siguiente comando para levantar la aplicación en un contenedor Docker:


El orquestador de contenedores `docker-compose` se encargará de crear y levantar el contenedor con la aplicación FastAPI
y todas las dependencias necesarias.


```bash
sudo docker compose up
```
Eso hara lo siguiente por ti:

1- Creará una imagen ligera con la versión de python adecuada

2- Instalará las dependencias del proyecto.

3- Ejecutara un script con una semilla de datos iniciales.

4- Levantará un contenedor con la aplicación FastAPI.

5- Expondrá el puerto 8000 para acceder a la aplicación.

6- y podrás acceder a sandbox en `http://localhost:8000`.

**Podras acceder a la documentación interactiva en:** `http://localhost:8000/docs`


Si aún no lo tienes instalado y deseas correr la api en Docker, puedes seguir las siguentes instrucciones para instalar Docker en tu ordenador:

### Instrucciones para instalar Docker
https://www.hostinger.com/co/tutoriales/como-instalar-y-usar-docker-en-ubuntu

### Aclaración si te encuentras en un s.o. windows es necesario que instales docker desktop

Puedes hacerlo siguiendo la documentacion oficial en el siguiente enlace:
https://docs.docker.com/desktop/setup/install/windows-install/

---

## 📝 2) Requisitos (si corres sin Docker)
Si decides correr sin Docker:

Este Projecto cuenta con un sistema de gestión de dependencias moderno que suplanta el conocido requirements.txt, lo puedes conseguir en la raiz del proyecto con el nombre de : pyproject.toml

Para poder utilizarlo es recomendable que utilices un gestor de entornos virtuales como `venv` o `virtualenv` 
para evitar conflictos con otras aplicaciones de Python.

## Instrucciones:


#### 1- Navega a tu carpeta del proyecto

```bash
cd /ruta/a/map_my_world
```

#### 2- Crea el entorno virtual**
```bash~ 
python3 -m venv venv
```

#### 3- Actíva el entorno virtual
```bash~ 
source venv/bin/activate
```


Esto deberia funcionar en la mayoria de los 
casos pero ten en cuenta que podrias necesitar ajustarlo a las necesidades, 
según la condición de tu entorno de desarrollo

#### 4- Instala las dependencias:

Ya con él entrono virtual activado debes instalar las dependencias del proyecto:

```bash~ 
pip install -e .
```

#### Opcional para entornos de desarrollo puedes instalar las dependencias de desarrollo con:

```bash~ 
pip install -e .[dev]
```

### 5- Ahora puedes correr la aplicación con el siguiente comando:

```bash~ 
uvicorn main:app --reload
```

#### Eso levantará el servidor y podras acceder a la aplicación en `http://localhost:8000`   

#### Accederas a la documentación de la API en: `http://localhost:8000/docs`

#### 6- Ejecuta la semilla de datos (Opcional)

Una vez que la aplicación esté corriendo, puedes poblar la base de datos con datos de 
ejemplo de esta manera:

Abre una nueva terminal, ubicate en la carpeta del proyecto en donde se encuentra seed_data.sh
y ejecuta el siguiente comando: 

```bash
sh seed_data.sh
``` 

Esto creará:

10 categorías (Restaurante, Parque, Museo, Hospital, etc.)
10 ubicaciones de ejemplo en Medellín
Las relaciones entre ubicaciones y categorías


#### 7- Deten el servidor de uvicorn y reinícialo con los siguientes comandos:

```bash
# Detener el servidor
CTRL + C

# Inicializar el servidor
uvicorn main:app --reload
```


---


### 📜 Rutas del API

| Método | Ruta                    | Descripción                                     |
| ------ |-------------------------|-------------------------------------------------|
| GET    | `/`                     | Página principal con el mapa (sandbox)          |
| GET    | `/docs`                 | Documentacion interactiva Swager                |
| POST   | `/locations/`           | Crear una nueva ubicación                       |
| GET    | `/list/locations`       | Listar todas las ubicaciones                    |
| POST   | `/categories/`          | Crear una nueva categoría                       |
| GET    | `/list/categories/`     | Listar todas las categorías                     |
| POST   | `/location-categories/` | Asociar una ubicación con una categoría         |
| POST   | `/reviews/`             | Marcar una ubicación-categoría como revisada    |
| GET    | `/recommendations/`     | Obtener 10 combinaciones que necesitan revisión |
```



## 🧱 Estructura del proyecto

```map_my_world/
├── db/ # Configuración y conexión de base de datos
│ └── database.py
├── models/ # Modelos ORM SQLAlchemy
│ └── models.py
├── routes/ # Rutas principales del API
│ └── crud_routes.py
├── schemas/ # Esquemas de entrada/salida con Pydantic
│ └── schemas.py
├── templates/ # Plantillas HTML (Jinja2)
│ └── map.html
├── utils/ # Lógica auxiliar, categorías por defecto, recomendaciones
│ └── default_categories.py
│ └── fresh_recommendations.py
├── main.py # Punto de entrada principal de la app
├── Dockerfile # Imagen personalizada de la app
├── docker-compose.yml # Orquestación de servicios
├── pyproject.toml # Dependencias Python
└── README.md # Este archivo```