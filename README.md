# Análisis de sentimiento con NAO y SaBert
### Práctica calificada 3
- André Dario Pilco Chiuyare - U202110764
- Iam Anthony Marcelo Alvarez Orellana - U202118258
- Marco Antonio Fuentes Rivera Onofre - U20211b693
- Renato Alberto Alcalde Gonzalez - U20191e742

## Diagrama de arquitectura de componentes
El diagrama representa la arquitectura de componentes diseñada para integrar un modelo de inteligencia artificial en el Robot NAO, permitiéndole realizar acciones específicas basadas en los resultados del modelo. La interacción comienza cuando el usuario selecciona, a través de un menú de opciones, el proceso de análisis de sentimiento proporcionado por `nao_control.py`. Para esto, el robot NAO indica que el usuario puede comenzar a hablar y procesa dicha entrada de voz en el módulo de procesamiento de lenguaje natural, el cual está administrado por el componente `ml_service.py`.

En primer lugar, el módulo `voice_recognition.py` convierte la voz en texto utilizando el servicio Azure Speech to Text y realiza ajustes para garantizar la precisión del texto transcrito. Luego, el texto es enviado a `ml_service.py`, el cual ejecuta el modelo SaBERT (modelo preentrenado basado en BERT y afinado para el análisis de sentimiento en español) para analizar el texto, clasificar el sentimiento como positivo o negativo.

En función de la clasificación, el módulo `nao_control.py` coordina la ejecución de la acción a través de la infraestructura local, enviando la orden al Robot NAO para que realice la acción correspondiente. De esta forma, el robot actúa como un agente inteligente capaz de responder de manera interactiva a las solicitudes del usuario. El objetivo de este sistema es demostrar la capacidad del Robot NAO para ejecutar acciones basadas en un modelo de IA, integrando tecnologías de reconocimiento de voz y aprendizaje automático en un entorno de interacción directa con el usuario.

## Instrucciones de instalación del modelo de IA en el robot NAO
Para el uso del sistema de análisis de sentimiento integrado con NAO v6, es necesario tener instalado el gestor de paquetes y administrador de entornos [Miniconda](https://docs.anaconda.com/miniconda/). Una vez que este requisito sea cumplido, se deben seguir los pasos:


1. En el terminal, crear los entornos correspondientes al controlador de NAO (nao-env) y al servicio del sistema (nao-ml-env) a través de la ejecución de los comandos:

        conda create -n nao-env python=2.7
        conda create -n nao-ml-env python=3.10

2. Descargar el [SDK de Nao v6](https://www.aldebaran.com/en/support/nao-6/downloads-softwares) de la página oficial de Aldebaran. Específicamente el `SDKs 2.8.6 - Python 2.7 SDK` en el caso de Windows. De preferencia, guardar el archivo comprimido en la carpeta `Documentos` para evitar problemas de permisos limitados.
<div align="center">
    <img src="./readme-assets/sdk.png" alt="Descarga de SDKs">
</div>
<br>

3. Modificar el nombre del archivo comprimido a `pynaoqi`, así se evitan inconvenientes por la larga longitud del nombre, la cual puede generar la corrupción de los archivos.

4. Descomprimir el archivo.

5. Una vez descomprimido, ingrese a la carpeta `pynaoqi`, en esta se encontrará con otra que tiene el nombre extenso original, la cual también debe ser renombrada a `pynaoqi`.

6. Copiar dicha carpeta interna que ahora es `pynaoqi`.

7. Pegar la carpeta dentro de la ruta `Disco local (C:) > Usuarios > [tu nombre de usuario] > miniconda3 > envs > nao-env > Lib > site-packages`. La ruta será similar a `C:\Users\andre\miniconda3\envs\nao-env\Lib\site-packages`.

8. Una vez que `pynaoqi` se encuentra dentro de la carpeta `site-packages`, es necesario copiar la ruta de la carpeta `lib` dentro de `pynaoqi`. La ruta será similar a `C:\Users\andre\miniconda3\envs\nao-env\Lib\site-packages\pynaoqi\lib`.

9. Ingresar a `Editar variables de entorno` a través del explorador de Windows.
<div align="center">
    <img src="./readme-assets/variables.png" alt="Variables de entorno">
</div>
<br>

10. Presionar `Variables de Entorno...`.
<div align="center">
    <img src="./readme-assets/entorno.png" alt="Variables de entorno">
</div>
<br>

11. Crear nueva variable para su usuario con el nombre PYTHONPATH y cuyo valor sea la ruta previamente copiada.
<div align="center">
    <img src="./readme-assets/crear-var.png" alt="Crear variable">
</div>
<br>

12. Verificar que se realizó la instalación correctamente a través del `símbolo del sistema (CMD)`. En este, ingresa el comando `conda activate nao-env`, para luego ejecutar `python`, lo que permitirá correr código de dicho lenguaje en la consola. Una de las bibliotecas por defecto es `numpy`, por lo se debe ingresar `import numpy` y presionar `enter` para verificar que no aparece ningún error. Luego de esto, ingresar `import naoqi` y presionar `enter`. Si después de esto no aparece ningún tipo de mensaje de error, se realizó la configuración correcta.
<div align="center">
    <img src="./readme-assets/consola.png" alt="Símbolo del sistema">
</div>

13. Por último, instalar las librerías necesarias para cada entorno a través de los comandos:

        conda activate nao-env
        pip install requests

        conda activate nao-ml-env
        pip install transformers flask torch

## Ejecución del modelo de IA en el robot NAO
Antes de ejecutar el sistema, es necesario descargar el software [Choregraphe](https://drive.google.com/file/d/1fJHgV-SHTfVJ_lM82l8ei6bFOo7mlqRH/view?usp=drive_link) y descomprimir el archivo.

1. Dentro de la carpeta descomprimida, ejecutar `naoqi-bin.exe` dentro de la carpeta `bin`, el cual es el emulador de NAO.
<div align="center">
    <img src="./readme-assets/consola.png" alt="Emulador de NAO">
</div>

2. Dentro de la carpeta descomprimida ejecutar `choregraphe.bat`. Una vez dentro, se debe ingresar a `Editar > Preferencias` y seleccionar el model de robot `NAO H25 (V6)`. De preferencia, cerrar y volver a abrir `Choregraphe` para que los cambios se realicen correctamente.
<div align="center">
    <img src="./readme-assets/preferencias.png" alt="Emulador de NAO">
</div>

3. Luego, realizar una nueva conexión a la dirección `127.0.0.1` en el puerto `9559` (verificar en el inicio de la consola de `naoqi-bin.exe` que la dirección es la misma). Si en la sección derecha aparece un robot virtual, todos los pasos realizados fueron correctos.
<div align="center">
    <img src="./readme-assets/conexion.png" alt="Conexion al emulador">
</div>

4. Ahora, es necesario abrir la carpeta `nao-project` en Visual Studio Code, en donde se deben abrir dos terminales PowerShell.
<div align="center">
    <img src="./readme-assets/terminal.png" alt="Terminales">
</div>

5. Ejecutar el servidor local en la primera terminal a través de los comandos:

        conda activate nao-ml-env
        python .\service\ml_service.py

6. Ejecutar el sistema en la segunda terminal a través de los comandos:

        conda activate nao-env
        python .\controller\nao_control.py

7. Por último, seleccionar una opción, hablar y visualizar los movimientos del robot a través de `Choregraphe`.

<div align="center">
    <img src="./readme-assets/emulador.png" alt="Ejecución del emulador">
</div>