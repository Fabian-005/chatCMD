# Chat con Comandos de Archivos
***	
## Requisitos
- Python
***	
## Estructura del proyecto

- **server-socket.py:** Codigo del servidor
- **cliente-socket.py:** Codigo del cliente
- **Files/:** Carpeta donde se almacenan los archivos disponibles para descargar.
- **downloard/:** Carpeta creada automaticamente para almacenar los archivos descargados 
***	
## Instalacion
1. Clona el repositorio
2. Dentro del directorio, en la carpeta "Files" coloca los archivos disponibles para que los clientes lo descarguen.
***
# Uso #
### Inicia el servidor ###
Ejecuta el comando para iniciar el servidor.
    python3 server-socket.py
***	
### Inicia el cliente ###
Ejecuta el comando para ejecutar el cliente.
    python3 cliente-socket.py
***	
### Comunicacion ###
**Chat:** Los clientes pueden enviar mensajes de texto a todos los demas clientes conectados.
**Comando /lsFiles:**  Lista los archivos disponibles en el servidor que se encuentran en la carpeta Files/.
**Comando /get <nombre del archivo>  :** Descargara el archivo seleccionado y sera guardado dentro de la carpeta download/ si el archivo existe, de lo contrario se enviara un mensaje de error.
***	
### Salir ###
Para finalizar el cliente y servidor simplemente escribe la palabra **Salir**.