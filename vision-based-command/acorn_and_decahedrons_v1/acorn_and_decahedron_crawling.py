import cv2
import socket
import struct
import numpy as np
import time
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
    def drop_pheromone(self):
        self.command_socket.sendall('\nm3 -2 3 10'.encode())
    def close(self):
        self.command_socket.close()
commander = Commander()

panning = False # initialize panning to false
current_command = "" # initialize empty string for current command being executed
search_time = 1 # initialize time to search when no objects detected

# bools for collection state
acorn_collecting = True
pheromone_collecting = False

# counter for number of commands sent
command_count = 0
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
                # handling detections
        if len(results) > 0:
            result_list = (results[0].boxes.cls).cpu().tolist()
            #print("result list: ", result_list)
            xywhn_list =  (results[0].boxes.xyxyn).cpu().tolist()
            #print("xywhn list: ", xywhn_list)
            # make list for acorn detection locations
            acorn_locations = []
            # make list for pheromone detection locations
            pheromone_locations = []
            for i in range(len(result_list)):
                if int(result_list[i]) == 0:
                    acorn_locations.append(xywhn_list[i])
                    #print("acorn locations: ", acorn_locations, "size: ", len(acorn_locations))
                elif int(result_list[i]) == 1:
                    pheromone_locations.append(xywhn_list[i])
                    #print("pheromone locations: ", pheromone_locations, "size: ", len(pheromone_locations))
            # sort acorn locations by y value
            acorn_locations.sort(key=lambda x: x[1], reverse=True)
            #print("sorted acorn locations: ", acorn_locations, "size: ", len(acorn_locations))
            # sort pheromone locations by y value
            pheromone_locations.sort(key=lambda x: x[1], reverse=True)
            #print("sorted pheromone locations: ", pheromone_locations, "size: ", len(pheromone_locations))
            
            # make list of center points of acorn locations
            acorn_centers = []
            for i in range(len(acorn_locations)):
                acorn_centers.append(((acorn_locations[i][0] + acorn_locations[i][2])/2, (acorn_locations[i][1] + acorn_locations[i][3])/2))
            print("acorn centers: ", acorn_centers, "size: ", len(acorn_centers))
            # make list of center points of pheromone locations
            pheromone_centers = []
            for i in range(len(pheromone_locations)):
                pheromone_centers.append(((pheromone_locations[i][0] + pheromone_locations[i][2])/2, (pheromone_locations[i][1] + pheromone_locations[i][3])/2))
            print("pheromone centers: ", pheromone_centers, "size: ", len(pheromone_centers))
        #end handling detections
        # start sending command section
            if acorn_collecting:
                print("current mode: acorn collecting")
                if len(acorn_centers) > 0 and acorn_centers[0][1] < 0.85:
                    print("entered acorn loop")
                    if acorn_centers[0][0] > 0.75:
                        current_command = "\nkcrR"
                    elif acorn_centers[0][0] < 0.25:
                        current_command = "\nkcrL"
                    else:
                        current_command = "\nkcrF"
                elif len(acorn_centers) > 0 and acorn_centers[0][1] > 0.85:
                    print("collecting acorns")
                    current_command = "\nm4 0 4 120"
                    print("turning around")
                    acorn_collecting = False
                    pheromone_collecting = True
            elif pheromone_collecting:
                print("current mode: pheromone collecting ")
                if len(pheromone_centers) > 0:
                    if pheromone_centers[0][0] > 0.75:
                        current_command = "\nkcrR"
                    elif pheromone_centers[0][0] < 0.25:
                        current_command = "\nkcrL"
                    else:
                        current_command = "\nkcrF"
                else:
                    current_command = "\nkvtR"
            print("current command: ", current_command)
            commander.send_command(current_command) 
            command_count += 1

            
        
        
        # end sending command section
        annotated_frame = results[0].plot()

        cv2.imshow("YOLOv8 Inference", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
commander.close()
client_socket.close()
cv2.destroyAllWindows()

