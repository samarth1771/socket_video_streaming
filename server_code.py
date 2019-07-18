import socket
import cv2
import pickle
import struct

PORT = 8089

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')
s.bind(('', PORT))
print('Socket bind complete')
s.listen(10)
print('Socket now listening')

conn, addr = s.accept()
data = b''  # Initializing empty binary object
payload_size = struct.calcsize("L")
cap = cv2.VideoCapture(0)

# Sending frame data to client and Listens to client

while True:

    # Sending frames to client

    ret, frame = cap.read()  # Starting video capture
    dat = pickle.dumps(frame)   # Creating pickle of frame data
    conn.sendall(struct.pack("L", len(dat)) + dat)

    # Receiving data from client

    while len(data) < payload_size:
        data += conn.recv(4096)
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("L", packed_msg_size)[0]
    while len(data) < msg_size:
        data += conn.recv(4096)
    frame_data = data[:msg_size]
    data = data[msg_size:]
    frame = pickle.loads(frame_data)
    cv2.imshow('Server Frame', frame)
    # Breaks loop on 'esc' key
    if cv2.waitKey(30) == 27:
        break
