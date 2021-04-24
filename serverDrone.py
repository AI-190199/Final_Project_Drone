""" Server Communication """

import socket
import struct
import sys
import time

class DroneComms(object):
    # Class to setup connection
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Connection 
        try:
            self.server.bind((socket.gethostname(),1902)) # Attempt to bind this application to the ip and port 4G Port 1902  
            self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Reuse this address if there was a problem
            self.server.listen(1) # Wait for connection
            self.orientation = [] # initial Variables
        except: # Catching Errors
            e = sys.exc_info()[0]
            print(e) # Print the Error

    def acceptConn(self):
        # A function to wait for a client to connect
        print("Waiting for Drone to Connect")
        while True:
            self.conn, self.address = self.server.accept() # Accept the connection
            print(f"Client {self.address} has Connected")
            self.conn.send(struct.pack("B",1)+str("Connected to server").encode()) # Send a message to the drone
            break
        return self.conn, self.address 
    
    def Received(self):
        try:
            data = b''
            #print("Waiting for Data")
            data += self.conn.recv(16)
            #print("Data Received")
            if struct.unpack("B", data[0:1])[0] == 1:
                print("Message Recieved: ", data[1:].decode())
                data = b''
                
            if struct.unpack("B", data[0:1])[0] == 2:
                if len(data) == 16:
                    self.orientation = struct.unpack("Bfff",data)
                    return (self.orientation)
                data = b''
                
            if struct.unpack("B ", data[0:1])[0] == 3:
                if len(data) == 10:
                    self.speed = struct.unpack("B4H",data)
                    return(self.speed)
                data = b''
            if struct.unpack("B ", data[0:1])[0] == 4:
                self.position = struct.unpack("Bdd",data)
                print(self.position)
                data = b''
            if struct.unpack("B ", data[0:1])[0] == 5:
                self.startTime = struct.unpack("Bd",data)
                print(self.startTime[1])
                ping =  time.time() - self.startTime[1]
                print(ping)
                data = b''
        except struct.error as e:
            pass