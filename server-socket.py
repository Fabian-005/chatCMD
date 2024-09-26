import socket 
import threading
import sys
import os

class Servidor():
    def __init__(self, host="localhost", port=7000):
        # Lista para guardar los clientes conectados
        self.clientes = []
        
        # Crear el socket y configurarlo
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((str(host), int(port)))
        self.sock.listen(10)  # Escuchar hasta 10 conexiones simultáneas
        self.sock.setblocking(False)  # No bloquear el programa esperando conexiones

        # Directorio donde se guardan los archivos
        self.files_dir = "./Files"

        # Crear y ejecutar los hilos para aceptar y procesar las conexiones
        aceptar = threading.Thread(target=self.aceptarCon)
        procesar = threading.Thread(target=self.procesarCon)
        aceptar.daemon = True  
        aceptar.start()
        procesar.daemon = True 
        procesar.start()

        # Bucle para manejar el servidor en la terminal
        try:
            while True:
                msg = input('-> ')
                if msg == 'salir':  # Si el admin escribe 'salir', el servidor se cierra
                    break
                self.sock.close()
                sys.exit()
        except:
            self.sock.close()
            sys.exit()

    # Acepta nuevas conexiones de clientes
    def aceptarCon(self):
        print("aceptarCon iniciado")
        while True:
            try:
                conn, addr = self.sock.accept()  # Aceptar la conexión
                conn.setblocking(False)  # No bloquear al recibir datos
                self.clientes.append(conn)  # Añadir el cliente a la lista
            except:
                pass

    # Procesa los mensajes de los clientes
    def procesarCon(self):
        print("ProcesarCon iniciado")
        while True:
            if len(self.clientes) > 0:  
                for c in self.clientes:
                    try:
                        data = c.recv(1024).decode('utf-8')  
                        if data:
                            if data.startswith('/'):
                                # Si el mensaje comienza con '/', es un comando
                                self.handle_command(data, c)
                            else:
                                # Cualquier otro mensaje se trata como mensaje de chat
                                self.msg_to_all(f"Cliente: {data}", c)
                    except:
                        pass

    # Maneja los comandos que empiezan con '/'
    def handle_command(self, command, cliente):
        if command == '/lsFiles':
            self.list_files(cliente)  # Listar archivos en el servidor
        elif command.startswith('/get '):
            filename = command.split(' ')[1]  
            self.send_file(cliente, filename)  

    # Enviar la lista de archivos al cliente
    def list_files(self, cliente):
        try:
            files = os.listdir(self.files_dir)  # Listar archivos en el directorio
            file_list = "\n".join(files)  # Convertir la lista en una cadena de texto
            cliente.send(file_list.encode('utf-8'))  # Enviar la lista al cliente
        except Exception as e:
            cliente.send(f"Error: {str(e)}".encode('utf-8'))  # Enviar error si falla

    # Enviar un archivo al cliente
    def send_file(self, cliente, filename):
        filepath = os.path.join(self.files_dir, filename)  # Ruta completa del archivo
        if os.path.exists(filepath):  # Verificar si el archivo existe
            with open(filepath, 'rb') as f:
                cliente.send(f"START {filename}".encode('utf-8'))  # Indicador de inicio de archivo
                while True:
                    data = f.read(1024)  # Leer el archivo en trozos de 1024 bytes
                    if not data:
                        break
                    cliente.send(data)  
                cliente.send(b"END")  
        else:
            cliente.send(f"Error: El archivo {filename} no existe.".encode('utf-8'))

    # Enviar mensajes a todos los clientes excepto al que lo envió
    def msg_to_all(self, msg, cliente):
        for c in self.clientes:
            if c != cliente:  
                try:
                    c.send(msg.encode('utf-8'))  
                except:
                    self.clientes.remove(c) 

server = Servidor()
server()
