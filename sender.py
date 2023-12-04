import cv2
import socket
import struct
import time

cap = cv2.VideoCapture(0)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_ip = '192.168.1.11'
port = 12345

client_socket.connect((host_ip,port))

n = 10
frame_count = 0
while cap.isOpened():
    ret, frame = cap.read()
    frame = cv2.resize(frame, (640,480))
    frame_count += 1
    if not ret or frame_count % n != 0:
        continue
    currentTime = time.time()
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 80]
    _, buffer = cv2.imencode('.jpg', frame, encode_param)
    print("Time taken: ",time.time() - currentTime)

    data = buffer.tobytes()
    size = len(data)
    print("Size: ", size)

    client_socket.sendall(struct.pack(">L", size) + data)

cap.release()
client_socket.close()
