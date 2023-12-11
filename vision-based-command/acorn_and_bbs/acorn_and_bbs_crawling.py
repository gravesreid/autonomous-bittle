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
host_ip = '192.168.1.155'  # IP Address
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

panning = False # initialize panning to false
current_command = "" # initialize empty string for current command being executed
search_time = 1 # initialize time to search when no objects detected
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
            xywhn_list = (results[0].boxes.xywhn).cpu().tolist() # make a list of position and box sizes
            x_list = []
            y_list = []
            w_list = []
            h_list = []
            for i in range(len(xywhn_list)): # loop through list of object detections
                for j, dim in enumerate(xywhn_list[i]): # loop through each detection and get the x,y,w,h values
                    if j==0: # x position value
                        x_list.append(dim)
                    if j==1: # y position value
                        y_list.append(dim)
                    if j==2: # w value
                        w_list.append(dim)
                    if j==3: # h value
                        h_list.append(dim)
            y_min = 1000.0
            min_index = 0
            for i, value in enumerate(y_list): # loop y values to find the minimum 
                if y_min > value: # change y_min to new minimum
                    y_min = value
                    min_index = i
            if result_list: # if result list isn't empty, there is at least one detection
                search_time = 1 # identified an object, so reset search time to 1 second
                if result_list[0] == 0.0: # 0.0 is an acorn detection
                    # determine if green block is to left or right side of frame
                    if x_list[min_index] < 0.25 and current_command != "kcrL": # block is to the left
                        print("sending crawl left command")
                        current_command = "kcrL"
                        commander.send_command('\nkcrL')
                    elif x_list[min_index] > 0.75 and current_command != "kcrR": # block is to the right 
                        print("sending crawl right command")
                        current_command = "kcrR"
                        commander.send_command('\nkcrR')
                    elif current_command != "kcrF": # Block is in center 
                        print("sending crawl forward command")
                        current_command = "kcrF"
                        commander.send_command('\nkcrF')
                elif result_list[0] == 1.0: # 1.0 is a pheromone detection
                    # determine if pheromone is to left or right side of frame
                    if x_list[min_index] < 0.25 and current_command != "kcrL": # pheromone is to the left
                        print("sending crawl left command")
                        current_command = "kcrL"
                        commander.send_command('\nkcrL')
                    elif x_list[min_index] > 0.75 and current_command != "kcrR": # pheromone is to the right 
                        print("sending crawl right command")
                        current_command = "kcrR"
                        commander.send_command('\nkcrR')
                    elif current_command != "kcrF": # pheromone is in center 
                        print("sending crawl forward command")
                        current_command = "kcrF"
                        commander.send_command('\nkcrF')
            else:
                if panning==False:
                    panning = True
                    start_time = time.time()
                pan_time = time.time() - start_time
                print("No object detected Crawling right")
                if pan_time<search_time and current_command != "kcrR":
                    current_command = "kcrR"
                    commander.send_command('\nkcrR')
                    print("pan time: ", pan_time)
                if pan_time>search_time and pan_time<(3*search_time) and current_command != "kcrL":
                    print("didn't find anything to the right. Crawling left")
                    current_command = "kcrL"
                    commander.send_command('\nkcrL')
                    print("pan time: ", pan_time)
                if pan_time>(3*search_time):
                    print("didn't find anything to the left. Increasing search radius")
                    search_time += 2
                    panning = False
        else:
            print("No detections")  

        annotated_frame = results[0].plot()

        cv2.imshow("YOLOv8 Inference", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
commander.close()
client_socket.close()
cv2.destroyAllWindows()

