
import socket
import cv2
import sys
import zlib
import numpy as np
import struct
import time
import math
import threading
import csv

import serverDrone
#from turbojpeg import TurboJPEG, TJPF_GRAY, TJSAMP_GRAY, TJFLAG_PROGRESSIVE
import Controller
Header = 2**14-1024

class VideoFeed(object):
    """ A class to recieve and decompress the video feed"""

    def __init__(self):
        self.feed = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.frameBuffer = bytearray()
            self.frames = []
            self.Header = 16
           ## Setting up UDP to receive video
            self.feed.bind((socket.gethostname(),8090)) # Binding to address 4G PORT 8090
            #self.feed.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # # Reuse this address if there was a problem
            self.feed.listen(1)
        except:
            e = sys.exc_info()[0]
            print(e)
    def acceptConn(self):
        # A function to wait for a client to connect
        print("Waiting for Visual Feed to Connect")
        while True:
            self.conn, self.address = self.feed.accept() # Accept the connection
            print(f"Client {self.address} has Connected")
            #self.conn.send(struct.pack("B",1)+str("FeedBack Connected").encode()) # Send a message to the drone
            break
        return self.conn, self.address 

    def Video(self, Image):
        #with open('test.csv', 'w', newline='') as file:
        #    writer = csv.writer(file)
        #    writer.writerow(["FrameNumber", "size", "processingTime"])
        #    FrameNumber = 0
        #    Revtimer = 0
        #    self.timeRev = 0
            while True:
                try:
                    seg = b''
                    seg = self.conn.recv(self.Header)
                    #print(len(seg))

                    if struct.unpack("B", seg[0:1])[0] == 0:
                        #print("\n======================================\n")
                        #print("\nGettiing image information")
                        #print(seg)
                        self.data = struct.unpack("BI", seg[:8])
                        #print("[INFO] 1.Actual Chunk Size: ",self.data[3])
                        #print("[INFO] 2.Current Chunk Number: ",self.data[1])
                        #print("[INFO] 3.Total Number of Chunks: ", self.data[2])
                        #print("[INFO] 4.Total Image Length: ", self.data[4])
                        self.Header = self.data[1] #+ 1

                    if struct.unpack("B", seg[0:1])[0] == 1:
                        
                        #print("Recv: "+ str(len(imageData))+ "Actual Len: " + str(self.data[3]))
                        if len(seg) == self.data[1]:
                            #print("Decompressing")
                            timer = time.perf_counter()
                            zobj = zlib.decompressobj()
                            img = zobj.decompress(seg[1:])
                           # self.img = self.jpeg(img)
                            self.img = cv2.imdecode(np.frombuffer(img, dtype=np.uint8), 1)
                            #processTime = round((time.perf_counter() - timer)*1000,2)
                            #self.img = cv2.imencode(img)
                            Image.append(self.img)
                            #FrameNumber += 1
                            #print("Processing Time: " + str(processTime) + " MS" + "\nFrame Number: " + str(FrameNumber))
                            #time.sleep(1)
                            #writer.writerow([FrameNumber, len(seg), processTime])
                            

                            #if FrameNumber == 100:
                            #    file.close()
                            #    break

                    #if struct.unpack("B", seg[0:1])[0] == 2:
                        #print("Data sent")
                    #    self.timeRev = time.time()
                    #    tr
                    #    if self.timeRev != 0:
                    #        self.conn.send(struct.pack("B",1))
                    #        delay = time.time() - self.timeRev
                    #        self.timeRev = 0
                    #        print(round(delay*1000,3))


                except:
                    e = sys.exc_info()[0]
                    #print("[ERROR VIDEO-THREAD]: ",e)


class GUI():

    def __init__(self):
        self.font = cv2.FONT_HERSHEY_SIMPLEX
    def Draw(self, Image):
        """ Processing Image and Displaying """
        try:
            self.time = time.strftime("%H:%M:%S", time.localtime())
            self.flipImg = cv2.flip(Image[0], -1)# Original: self.img
            resized_image = cv2.resize(self.flipImg, (1280, 720))
            cv2.putText(resized_image, "RemoteView",(600,30),self.font,0.5, (255,255,255),1)
        
            cv2.putText(resized_image , str(self.time),(30,700),self.font,0.5, (255,255,255),1)


            cv2.imshow('RemoteView', resized_image)#resized_image)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("Client Disconnected")
                cv2.destroyAllWindows()
                return (0)
        except:
            pass
           #print("Video Thread Error - format")
      


if __name__ == "__main__":
    Feed = VideoFeed()
    services = serverDrone.DroneComms()
    services_conn ,addr = services.acceptConn()

    
    Display = GUI()
    conn, addr = Feed.acceptConn()
    Control = Controller.controller(services_conn)

    Image = []
    Video_Thread = threading.Thread(target = Feed.Video, args = (Image,), daemon = True)
    Video_Thread.start()
    
    Controller_Thread = threading.Thread(target = Control.send)
    Controller_Thread.start()
    while True:
        if Image != []:
            show = Display.Draw(Image)
            #print("Images decoded: ",len(Image))
            Image.clear()
            if show == 0:
                break

        if Video_Thread.is_alive() != True:
            print("\nVideo Thread Stopped\n")
            break

print("EXIT")





