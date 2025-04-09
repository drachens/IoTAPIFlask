# Sistema de Gestión de Datos para Sensores IoT

Este proyecto implementa una API RESTful con Flask para la gestión de datos de sensores IoT, permitiendo registrar compañías, ubicaciones, sensores y datos recolectados. Se utiliza autenticación básica para controlar el acceso a los endpoints.

## Tabla de Contenidos

- [Instalación](#instalación)
- [Configuración](#configuración)
- [Uso](#uso)
  - [Autenticación](#autenticación)
  - [Compañías](#compañías)
  - [Ubicaciones](#ubicaciones)
  - [Sensores](#sensores)
  - [Datos de sensores](#datos-de-sensores)
- [Tecnologías Utilizadas](#tecnologías-utilizadas)
- [Contacto](#contacto)

## Instalación

```bash
git clone https://github.com/tuusuario/tu-repo.git
cd tu-repo
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Configuración

1. Verifica el archivo `config.py` para la URI de la base de datos.
2. Ejecuta la migración inicial:

```bash
flask db init
flask db migrate -m "Migration init"
flask db upgrade
```

3. Ejecuta la aplicación:

```bash
python run.py
```

## Uso

### Autenticación

El sistema utiliza autenticación HTTP Basic para proteger los endpoints. Para usar Postman:

- Ir a la pestaña "Authorization".
- Tipo: `Basic Auth`
- Usuario: (admin creado previamente)
- Contraseña: (la contraseña que asignaste)

### Compañías

#### Crear una compañía

```http
POST /companies
Content-Type: application/json
Authorization: Basic ...

{
  "company_name": "Mi Empresa"
}
```

#### Obtener lista de compañías

```http
GET /companies
Authorization: Basic ...
```

### Ubicaciones

#### Crear una ubicación
```http
POST /locations
Authorization: Basic ...

{
  "company_api_key": "clave-api-compania",
  "location_name": "Sucursal A",
  "location_country": "Chile",
  "location_city": "Santiago",
  "location_meta": "Segundo piso"
}
```

#### Obtener ubicaciones de una compañía
```http
GET /locations?company_api_key=clave-api-compania
Authorization: Basic ...
```

### Sensores

#### Crear un sensor
```http
POST /sensors
Authorization: Basic ...

{
  "company_api_key": "clave-api-compania",
  "sensor_name": "Sensor Temperatura",
  "sensor_category": "Clima",
  "sensor_meta": "Interior"
}
```

#### Obtener sensores
```http
GET /sensors?company_api_key=clave-api-compania
Authorization: Basic ...
```

### Datos de sensores

#### Insertar datos desde sensor
```http
POST /api/v1/sensor_data
Authorization: Basic ...

{
  "api_key": "clave-api-sensor",
  "json_data": [
    {"key1": 22},
    {"key2": 45}
  ]
}
```

#### Obtener datos de sensores
```http
GET /api/v1/sensor_data?company_api_key=clave-api-compania&from=timestamp_inicio&to=timestamp_fin&sensor_id=1&sensor_id=2
Authorization: Basic ...
```

## Tecnologías Utilizadas

- Python 3.x
- Flask
- SQLAlchemy
- Flask-Migrate
- SQLite (por defecto)
- Postman (para pruebas de API)


## Contacto

Desarrollado por Italo Piermartiri. Para consultas o colaboraciones, puedes escribirme a: [italo.piermartiri@mail.udp.cl]
