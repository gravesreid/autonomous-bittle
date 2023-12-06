import cv2
import socket
import struct
import numpy as np
from ultralytics import YOLO

# Load YOLO
model = YOLO('best.pt')
model.conf = 0.5

#get output from YOLO V8
def detect_objects(frame):
    results = model([frame], stream=True)
    return results

# Create a socket for receiving data
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_ip = '192.168.1.11'  # IP Address
port = 12345  # Must be the same as in the sender

socket_address = (host_ip, port)

# Bind to the address and listen
server_socket.bind(socket_address)
server_socket.listen(5)
print("Listening at:", socket_address)

# Accept a connection
client_socket, addr = server_socket.accept()
print('Connection from:', addr)

data = b""
payload_size = struct.calcsize(">L")

# Create socket for sending commands

class Commander: 
    def __init__(self):
        self.command_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        pi_ip = '192.168.1.2' # raspberry pi ip address
        pi_port = 12346 # must match port in ardSocket.py on pi
        self.command_socket.connect((pi_ip, pi_port))
        
    def send_command(self, command):
        try:
            self.command_socket.sendall(command.encode())
        except:
            print("Error sending command")
    def close(self):
        self.command_socket.close()
commander = Commander()

while True:
    # Retrieve message size
    while len(data) < payload_size:
        data += client_socket.recv(4096)

    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack(">L", packed_msg_size)[0]

    # Retrieve all data based on message size
    while len(data) < msg_size:
        data += client_socket.recv(4096)

    frame_data = data[:msg_size]
    data = data[msg_size:]

    # Decompress frame
    frame = cv2.imdecode(np.frombuffer(frame_data, dtype=np.uint8), cv2.IMREAD_COLOR)

    if frame is not None:
        results = model(frame)
        if len(results) > 0: 
            result_list = (results[0].boxes.cls).cpu().tolist()
            names = (results[0].names)
            xyxy = (results[0].boxes.xyxy).cpu()
            xywh = (results[0].boxes.xywh).cpu().tolist()
            xyxyn = (results[0].boxes.xyxyn).cpu().tolist()
            print("First detection:", result_list)
            print("names", names)
            if result_list:
                print("sending walk command")
                print("xyxy", xyxy)
                print("xywh", xywh)
                print("xyxyn", xyxyn)
                commander.send_command('\nkwkF')
            else:
                print("sending rest command")
                commander.send_command('\nkrest')
        else:
            print("No detections")  

        annotated_frame = results[0].plot()

        cv2.imshow("YOLOv8 Inference", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
commander.close()
client_socket.close()
cv2.destroyAllWindows()

