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
        annotated_frame = results[0].plot()

        cv2.imshow("YOLOv8 Inference", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

client_socket.close()
cv2.destroyAllWindows()

