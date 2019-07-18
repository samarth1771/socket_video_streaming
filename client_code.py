import cv2
import socket
import pickle
import struct

cap = cv2.VideoCapture(0)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

HOST = '192.168.0.139'  # Enter IP add of server here
PORT = 8089

s.connect((HOST, PORT))
data = b''
payload_size = struct.calcsize("L")

# Sending frame data to server and displays the received frame data from server


while True:

    ret, frame = cap.read()
    dat = pickle.dumps(frame)
    s.sendall(struct.pack("L", len(dat)) + dat)

    while len(data) < payload_size:
        data += s.recv(4096)
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("L", packed_msg_size)[0]
    while len(data) < msg_size:
        data += s.recv(4096)
    frame_data = data[:msg_size]
    data = data[msg_size:]
    frame = pickle.loads(frame_data)
    cv2.imshow('Client frame', frame)
    # Breaks loop on 'esc' key
    if cv2.waitKey(30) == 27:
        break


