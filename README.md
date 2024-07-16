# Flask Application Setup

Este proyecto es una aplicación Flask con una base de datos SQLite y autenticación básica.

## Requisitos

- Python 3.6+
- pip (instalador de paquetes de Python)

## 1 Configuración del Entorno

Sigue estos pasos para configurar y ejecutar la aplicación:

### 1.1 Crear el Entorno Virtual

Ejecuta el script `start.bat` para crear un entorno virtual y activar el entorno:

```bash
start.bat
```
## 2 Activar el Entorno Virtual

En la ventana de comandos, activa el entorno virtual (si no se ha activado automáticamente):
```bash
venv\Scripts\activate
```

## 3 Establecer la Variable de Entorno 

Establece la variable de entorno FLASK_APP:

```bash
set FLASK_APP=run.py
```

## 4 Inicializar la Base de Datos

Inicializa la base de datos usando Flask-Migrate:

```bash
flask db init
flask db migrate -m "Initial migration."
flask db upgrade
```

## 5 Ejecutar la Aplicación

Finalmente, ejecuta la aplicación:

```bash
python run.py
```



