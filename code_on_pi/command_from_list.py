import time
import socket
import sys
import pickle
sys.path.append("..")
from ardSerial import *


model = 'Bittle'
postureTable = postureDict[model]


if __name__ == '__main__':
    try:
        goodPorts = {}
        connectPort(goodPorts)
        t=threading.Thread(target = keepCheckingPort, args = (goodPorts,))
        t.start()
        parallel = False
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('192.168.1.2', 12346)) #raspberry pi IP address
        server_socket.listen()

        print("Waiting for a connection...")
        connection, client_address = server_socket.accept()
        print(f"Connection from {client_address}")
        

        while True and len(goodPorts):
            data = b""
            payload_size = struct.calcsize(">L")
            time.sleep(0.001)
            while len(data) < payload_size:
                data += connection.recv(1028)
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack(">L", packed_msg_size)[0]
            
            while len(data) < msg_size:
                data += connection.recv(1028)
            data = data[msg_size:]
                
            print("Received data size: ", len(data), "Expected size: ", msg_size)
            
            if len(data) == msg_size:
                try:
                    command_dict = pickle.loads(data)
                    command_list = command_dict["command list"]
                    print("Command dictionary: ", command_dict)
                    for command in command_list:
                        send(goodPorts, command)
                except pickle.UnpicklingError as e:
                    print("Unpickling Error:", e)
            else:
                print("Incomplete data received")
                
    except Exception as e:
        print(f"Error receiving data: {e}")  
        logger.info("Exception")
        raise e
    finally:
        if connection:
            print("Closing connection")
            connection.close()
        if server_socket:
            print("Closing socket")
            server_socket.close()
        closeAllSerial(goodPorts)
        logger.info("finish!")
        os._exit(0)