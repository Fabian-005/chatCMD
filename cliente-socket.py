import socket
import threading
import sys
import os

class Cliente():
    def __init__(self, host="localhost", port=7000):
        try:
            # Crear el socket y conectarlo al servidor
            self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.sock.connect((str(host), int(port)))

            # Directorio donde se descargan los archivos
            self.download_dir = "./download"
            if not os.path.exists(self.download_dir):
                os.makedirs(self.download_dir)  # Crear el directorio si no existe

            # Hilo para recibir mensajes del servidor
            msg_recv = threading.Thread(target=self.msg_recv)
            msg_recv.daemon = True  
            msg_recv.start()

            # Bucle para enviar mensajes al servidor
            while True:
                msg = input('-> ')  # Pedir input al usuario
                if msg != 'salir':  # Si no es salir, enviar el mensaje
                    if msg.startswith('/'):
                        # Si el mensaje comienza con '/', es un comando
                        self.send_msg(msg)
                    else:
                        # Mensaje de chat
                        self.send_msg(msg)
                else:
                    # Cerrar el socket si el usuario escribe 'salir'
                    self.sock.close()
                    sys.exit()
        except Exception as e:
            print(f"Error al conectar el socket: {str(e)}")

    # Función para recibir mensajes del servidor
    def msg_recv(self):
        buffer = b'' 
        receiving_file = False
        filename = None

        while True:
            try:
                data = self.sock.recv(1024)  

                if data:
                    if data.startswith(b"START"):
                        # Si el mensaje empieza con "START", indica que empieza un archivo
                        receiving_file = True
                        filename = data.decode('utf-8').split(' ')[1]
                        print(f"Recibiendo archivo: {filename}")
                        buffer = b''  # Limpiar buffer para el nuevo archivo
                    elif data.endswith(b"END"):
                        # Si el mensaje acaba con "END", el archivo ha terminado
                        receiving_file = False
                        filepath = os.path.join(self.download_dir, filename)
                        with open(filepath, 'wb') as f:
                            f.write(buffer)  # Guardar el archivo en el directorio
                        print(f"Archivo guardado en {filepath}")
                    else:
                        if receiving_file:
                            buffer += data  
                        else:
                            print(data.decode('utf-8'))  # Mostrar mensaje de texto
            except:
                pass

    # Función para enviar mensajes al servidor
    def send_msg(self, msg):
        try:
            self.sock.send(msg.encode('utf-8'))  # Enviar mensaje al servidor
        except Exception as e:
            print(f"Error al enviar mensaje: {str(e)}")

cliente = Cliente()
cliente()
