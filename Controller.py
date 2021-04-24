#Controller

import pygame
import struct
import time
import sys

class controller(object):
    """ A class for the controller """
    def __init__(self,conn):
        """ Initailising Pygame """
        self.conn = conn
        self.previousControl = []
        pygame.init()
        while True:
            try:
                self.joystick_count = pygame.joystick.get_count()
                if self.joystick_count != 1:
                    print("Please connect a controller")
                    #time.sleep(3)
                    self.reconnect()
                else:
                    for i in range(self.joystick_count):
                        self.joystick = pygame.joystick.Joystick(i)
                        self.joystick.init()
                    self.axes = self.joystick.get_numaxes()
                    #print(self.axes)
                    self.buttons = self.joystick.get_numbuttons()
                    name = self.joystick.get_name()
                    print(name)
                    break
            except:
                e = sys.exc_info()[1]
                time.sleep(3)
                print("An Error Occurred during the Controller setup: ",e)
    
    def reconnect(self):
        print("Number of controllers detected: ", self.joystick_count)
        while True:
            pygame.joystick.quit()
            pygame.joystick.init()
            pygame.init()
            self.joystick_count = pygame.joystick.get_count()
            #print("Number of controllers detected: ", self.joystick_count)
            if self.joystick_count == 1:
                for i in range(self.joystick_count):
                    self.joystick = pygame.joystick.Joystick(i)
                    self.joystick.init()
                self.axes = self.joystick.get_numaxes()
                #print(self.axes)
                #self.buttons = self.joystick.get_numbuttons()
                name = self.joystick.get_name()
                print(name)
                break
                
    #def sender(self, command):

    #    self.previousControl.append(command)
    #    if len(self.previousControl) == []:
    #        self.conn.send(command)
    #    if len(self.previousControl) > 1:
    #        if self.previousControl[0] != self.previousControl[1]:
    #            self.conn.send(command)
    #            self.previousControl.clear()
    #            self.previousControl.append(command)
    #        else:
    #            self.previousControl.pop()
                #print(len(self.previousControl))
    def send(self):
        """ Send Commands to Drone"""
        
        while True:
            self.joystick_count = pygame.joystick.get_count()
            if self.joystick_count != 1:
                    print("Please reconnect the controller")
                    self.reconnect()
                    continue
            else:
                for event in pygame.event.get(): 
                    if event.type == pygame.QUIT:
                        done = True
                    #print("Event: ",event)
                for i in range(self.axes):
                    axis = self.joystick.get_axis(i)
                    time.sleep(0.01)
                    if i == 0:
                        if round(axis) == 0:
                            d = struct.pack("BBf",2,0,round(axis))
                         #   d= struct.pack("BBf",2,i,0)
                            #print("LSCA: ", struct.unpack("BBf",d))
                            #self.sender(d)
                            self.conn.send(d)
                            #continue
                     
                        if round(axis) == 1:
                            d = struct.pack("BBf",2,i,round(axis))
                            print("LSR: ", struct.unpack("BBf",d))
                            #self.sender(d)
                            self.conn.send(d)
                        if round(axis) == -1:
                            d = struct.pack("BBf",2,i,round(axis))
                            print("LSL: ", struct.unpack("BBf",d))
                            #self.sender(d)
                            self.conn.send(d)
                        #else:
                            #d = struct.pack("BBf",2,1,round(axis,3))
                            #self.conn.send(d)
                    if i == 1:
                        #print(round(axis,3))
                        if round(axis) == 0:
                            d = struct.pack("BBf",2,i,round(axis))
                            #print("LSCB: ", struct.unpack("BBf",d))
                            #self.sender(d)
                            self.conn.send(d)
                            #continue
                        if round(axis) == 1:
                            d = struct.pack("BBf",2,i,round(axis))
                            print("LSB: ", struct.unpack("BBf",d))
                            #self.sender(d)
                            self.conn.send(d)

                        if round(axis) == -1:
                            d = struct.pack("BBf",2,i,round(axis))
                            print("LSF: ", struct.unpack("BBf",d))
                            #self.sender(d)
                            self.conn.send(d)
                        #else:
                            #d = struct.pack("BBf",2,1,round(axis,3))
                            #self.conn.send(d)
                        
                    if i == 2:
                        if round(axis) == 0:
                            continue
                        if round(axis) == -1:
                            d = struct.pack("BBf",2,i,round(axis))
                            print("RSL: ", struct.unpack("BBf",d))
                            #self.sender(d)
                            self.conn.send(d)
                        
                        if round(axis) == 1:
                            d = struct.pack("BBf",2,i,round(axis))
                            print("RSR: ", struct.unpack("BBf",d))
                            #self.sender(d)
                            self.conn.send(d)



                    if i == 4:
                        if round(axis) == 0:
                            continue
                        if round(axis) != -1:
                            d = struct.pack("BBf",2,i,round(axis))
                            print("LT: ", struct.unpack("BBf",d))
                            #self.sender(d)
                            self.conn.send(d)
                    if i == 5:
                        if round(axis) == 0:
                            continue
                        if axis != -1:
                            d = struct.pack("BBf",2,i,round(axis))
                            print("RT: ", struct.unpack("BBf",d))
                            #self.sender(d)
                            self.conn.send(d)


                    for i in range(self.buttons):
                        button = self.joystick.get_button(i)
                       
                        if i == 6 and button == 1:
                            print("Calibrating")
                            d = struct.pack("BBf",2,7,1.0)
                            #self.sender(d)
                            self.conn.send(d)
                            time.sleep(1)
                        if i == 7 and button == 1:
                            print("start")
                            d = struct.pack("BBf",2,6,1.0)
                            #self.sender(d)
                            self.conn.send(d)
                            time.sleep(2)


#Control = controller()
#Control.send()
