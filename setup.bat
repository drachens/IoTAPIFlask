@echo off

:: Crear entorno virtual
python -m venv venv

:: Activar entorno virtual
call venv\Scripts\activate

:: Instalar dependencias
pip install -r requirements.txt

:: Mensaje de éxito
echo Entorno virtual creado y dependencias instaladas.
echo Para activar el entorno, usa "venv\Scripts\activate".
pause