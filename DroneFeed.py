import socket
import cv2
import sys
import zlib
import numpy as np
import struct
import time
import math
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
            self.conn.send(struct.pack("B",1)+str("FeedBack Connected").encode()) # Send a message to the drone
            break
        return self.conn, self.address 

    def Video(self):
       try:
            seg = b''
            seg = self.conn.recv(self.Header)
            


            if struct.unpack("B", seg[0:1])[0] == 0:
                #print("\n======================================\n")
                #print("\nGettiing image information")
                #print(seg)
                self.data = struct.unpack("2B3I", seg[:16])
                #print("[INFO] 1.Actual Chunk Size: ",self.data[3])
                #print("[INFO] 2.Current Chunk Number: ",self.data[1])
                #print("[INFO] 3.Total Number of Chunks: ", self.data[2])
                #print("[INFO] 4.Total Image Length: ", self.data[4])
                self.Header = self.data[3] #+ 1
  

            if struct.unpack("B", seg[0:1])[0] == 1:
                timer = time.perf_counter()
                imageData = seg[1:]
                self.frameBuffer.extend(imageData)
                while len(self.frameBuffer) < self.data[3]:
                    packet = self.conn.recv(self.data[3]-len(self.frameBuffer))
                    if not packet:
                        return None
                    self.frameBuffer.extend(packet)
                    if len(self.frameBuffer) > self.data[3]:
                        self.frameBuffer = bytearray()
                        self.frames.clear()
                self.frames.append(self.frameBuffer)
                if len(self.frameBuffer) == self.data[3]:
                    img = zlib.decompress(self.frames[0])
                    self.img = cv2.imdecode(np.frombuffer(img, dtype=np.uint8), 1)
                    self.frameBuffer = bytearray()
                    self.frames.clear()
                    #print("Processing Time: " + str((time.perf_counter() - timer)*1000) + " MS")
                    return self.img
                    
                if len(self.frameBuffer) > self.data[3]:
                    self.frameBuffer = bytearray()
                    self.frames.clear()


            #if struct.unpack("B", seg[0:1])[0] == 2:
                #imageData = seg[1:]
       except:
            e = sys.exc_info()[0]
            print("[ERROR SUB-THREAD]: ",e)









            #if struct.unpack("B", seg[0:1])[0] == 1:
            #    pass
            #    #print("OP 1")
            #    #struct.calc
            #    #self.imageSize = struct.unpack("2B3H", seg[:8])
            #    #Header = self.imageSize[1]
            #    #print(self.imageSize)
            #    #print("\n======================================\n")
            #    #print("[INFO] 1.Actual Chunk Size: ",self.imageSize[2])
            #    #print("[INFO] 2.Current Chunk Number: ",self.imageSize[1])
            #    #print("[INFO] 2.Total Number of Chunks: ", self.imageSize[3])
            #    #print("[INFO] 3.Total Image Length: ", self.imageSize[4])
            #    #time.sleep(2)
            ##segament = list(bytes(seg))
            ##print(seg[0:1])
            ##i = 0 
            #if struct.unpack("B", seg[0:1])[0] == 0:
            #    data = struct.unpack("2B3H",seg[:8])
            #    print("\n======================================\n")
            #    print("[INFO] 1.Actual Chunk Size: ",data[3])
            #    print("[INFO] 2.Current Chunk Number: ",data[1])
            #    print("[INFO] 2.Total Number of Chunks: ", data[2])
            #    print("[INFO] 3.Total Image Length: ", data[4])
            #    if len(self.chunkInfo) == 0:

            #        self.chunkInfo.append(data[4])
            #        self.framebuffer.append(seg[8:])
            #        numChunks = math.ceil(data[4]/(2**13-1024))
            #        print("Calculated Number of chunks: ",numChunks)
            #        print("Revc ChunkSize: ", len(seg[8:]))
            #    elif self.chunkInfo[0] == data[4]:
            #        self.framebuffer.append(seg[8:])

            #    else:
            #        self.chunkInfo.clear()
            #        self.framebuffer.clear()
                    

            #    if data[1] == data[2]:
            #        img = b''
            #        self.chunkInfo.clear()
            #        #data = zlib.decompress(seg[1:])
            #        for x in range(len(self.framebuffer)):
            #            img += self.framebuffer[x]#zlib.decompress(self.framebuffer[x])
            #        if len(img) == data[4]:
            #            img_decomp = zlib.decompress(img)
            #            self.img = cv2.imdecode(np.frombuffer(img_decomp, dtype=np.uint8), 1)
                    
            #            self.framebuffer.clear()
            #            return(self.img)
            #        else:
            #            self.framebuffer.clear()
            #            img = b''

            #        #self.i = 1
            #        #self.chunkInfo.clear()
            #        #return(self.img)
            #    if len(self.framebuffer) > data[2]:
            #        self.framebuffer.clear()
           
            

            #if struct.unpack("B", seg[0:1])[0] == 2:
                
            #    imgInfo = struct.unpack("2BH", seg[:4])
            #    print("\n[INFO] 4.Processing: " + str(imgInfo[1]) + "/" + str(self.imageSize[1]))
            #    print("[INFO] 5.Current Chunk Processing: ", imgInfo[1])
            #    print("[INFO] 6.Current Chunk Size: ", imgInfo[2])
            #    if imgInfo[2] == len(seg[4:]):
            #        print("[INFO] 7.Data Integrity 100%")
            #        print("\nGetting Chunk Information")
            #        print("\n[INFO] 8.Current Chunk Processing: ", imgInfo[1])
            #        print("[INFO] 9.Current Chunk Size: ", imgInfo[2])
                   
            #        self.chunkInfo.append(imgInfo[2])
            #        self.framebuffer.append(seg[4:])
            #        #print("FrameBuffer: ", len(self.framebuffer))
            #        #if len(self.framebuffer) > imgInfo[1]+1:
            #        #        print("\n[ERROR 1] DATA OUT OF SYNC\n")
            #        #        #print("[INFO] CLEARING BUFFER")
                         
            #        #        self.framebuffer.clear()
            #        #        self.chunkInfo.clear()
                   
            #        if len(self.framebuffer) == self.imageSize[1]:
            #            ##last chunk
            #            print("\n[INFO] 10.Processing Last Chunk")

            #            #print("CI:", len(self.chunkInfo))
            #            #print("FB: ", len(self.framebuffer))
            #            if len(self.framebuffer) == len(self.chunkInfo):
            #                for x in range(len(self.framebuffer)):
            #                    #if self.chunkInfo[x] == len(self.framebuffer[x]):
            #                        #print("[INFO] 11.Chunks Confirmed")
            #                    img = b''
            #                    img += zlib.decompress(i)
            #                    self.img = cv2.imdecode(np.frombuffer(img, dtype=np.uint8), 1)
            #                    #print("[INFO] 12. IMAGE RECONSTRUCTED")
            #                    self.framebuffer.clear()
            #                    self.chunkInfo.clear()
            #                    return(self.img)
            #            else:
            #                print("\n[ERROR 2] FAILED TO CONFIRM CHUNKS\n")
            #                self.framebuffer.clear()
            #                self.chunkInfo.clear()
            #    else:
            #        print("[ERROR 3]: Chunk mismatch")
            #        self.framebuffer.clear()
            #        self.chunkInfo.clear()
        #except:
         #   e = sys.exc_info()[0]
           # print("[ERROR SUB-THREAD]: ",e)





                        #self.chunkInfo.clear()
                        ##print(len(self.framebuffer[0]))
                        #if len(self.framebuffer[0]) != self.imageSize[1]:
                        #    print("Corrupted Data")
                        #    print("Frame: ", len(self.framebuffer[0]))
                        #    print("SI: ", self.imageSize[1])
                        #    self.framebuffer.clear()
                        #else:
                        #    

                        #    self.framebuffer.clear()
                    #else:
                    #    print("Error in confirming number of Chunks")
                    #    for i in self.framebuffer:
                    #        img += zlib.decompress(i)
                    #        self.img = cv2.imdecode(np.frombuffer(img, dtype=np.uint8), 1)
                    #        self.framebuffer.clear()
                    #        self.chunkInfo.clear()
                    #        return(self.img)
                #else:
                #    print("Error in confirming Chunk size")
                #    self.framebuffer.clear()
                #    self.chunkInfo.clear()
                        



















                #chunkData = struct.unpack("BBB",seg[0:3])
                #if len(self.framebuffer) != chunkData[2]+1:
                #        c = seg[1]
                #        if len(self.framebuffer) == c:
                #            self.framebuffer.append(seg[3:])
                #        else:
                #            self.framebuffer.clear()

                #if len(self.framebuffer) == chunkData[2]+1:
                #    for x in range(len(self.framebuffer)):
                #      #  print("For loops")
                #        print("Chunk size: ",len(self.framebuffer[x]))
                #    #print("Chunk length: ", len(self.framebuffer))
                #    #print(chunkData[2])
                #    print("Number of Chunks: ", len(self.framebuffer)) 
                #    print("Total Chunks to process: ", chunkData[2])
                #    #last chunk
                #    img = b''
                #    for x in self.framebuffer:
                #        img += zlib.decompress(x)
                #    if len(img) > self.imageSize[1]:
                #        print("\nERROR: Image mis-match")
                #        print("Gernerated Image Size: ", len(img))
                #        print("Actual Image Size: ",self.imageSize[1])
                #        self.framebuffer.clear()

                #        self.img = cv2.imdecode(np.frombuffer(img, dtype=np.uint8), 1)
                #        self.framebuffer.clear()
                #        #time.sleep(0.8)
                #        return(self.img)
                #    if len(img) == self.imageSize[1]:
                #        print("Image MATCH")
                #        self.img = cv2.imdecode(np.frombuffer(img, dtype=np.uint8), 1)
                #        self.framebuffer.clear()
                #        return(self.img)

                     
                    #else:
                        ##self.img = cv2.imdecode(np.frombuffer(img, dtype=np.uint8), 1)
                     #   self.framebuffer.clear()
                        #time.sleep(0.8)
                        #return(self.img)


       # except:
        #    e = sys.exc_info()[0]
            #print(e)
            #print("Corrupted Image")

# NOTE ADD Frame buffer to reduce the la


              
                #print(len(self.framebuffer))
                
                #data += struct.unpack("B", seg)
                #print(len(data))
                #print("The data Segament: ", len(data))
                #print("A")
            #if struct.unpack("B", seg[0:1])[0] == 2:
            #    print("Entered 2")
            #    #print("B")
            #    img = b''
            #    self.framebuffer.append(seg[1:])
            #    for x in self.framebuffer:
            #        img += x
            #    print(len(img))
            #    #img = zlib.decompress(data)
            #    self.img = cv2.imdecode(np.frombuffer(img, dtype=np.uint8), 1)
                
            #    self.framebuffer.clear()
            #    return(self.img)

        #except:
            
            #print(e)


        ##if len(seg) == Header:
        # #   self.framebuffer.clear()
        #  #  self.framebuffer.append(seg)
        #   # #print("Segament: ",len(self.framebuffer))
        ##else:
        #    #print("Seg: ",len(seg))
        #    #data = zlib.decompress(seg)
        #    #seg, addr = self.feed.recvfrom(Header)
        # #   self.framebuffer.append(seg)
        #    print("Segaments: ",len(self.framebuffer))
        #    #data = zlib.decompress(chunk2)
        #if len(self.framebuffer) >= 2:
        #    for i in range(len(self.framebuffer)):
        #        data = data + zlib.decompress(self.framebuffer[i])
        #        #data = zlib.decompress(self.framebuffer[0])+zlib.decompress(self.framebuffer[1])
        #    self.img = cv2.imdecode(np.frombuffer(data, dtype=np.uint8), 1)
        #    self.framebuffer.clear()
        #    return self.img
        #else:
        #     #print("chunk1 is empty")
        #     data = zlib.decompress(self.framebuffer[0])
        #     self.img = cv2.imdecode(np.frombuffer(data, dtype=np.uint8), 1)
        #     #print("here")
        #     self.framebuffer.clear()
        #     return(self.img)
        ##data = zlib.decompress(chunk1)+zlib.decompress(chunk2)