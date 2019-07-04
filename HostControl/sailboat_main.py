"""
Created on FRI DEC 28 14:29:21 2018

@author: Zeyuan Feng

@contributor: fahah & Lianxin Zhang

Main program for station keeping. 
"""


import math
import threading
import time

# import plot
import serial


import controller_4_DoF
import data_writer
import database
import get_message
import globalvar as gl
import keyboard_control
import visualization
import simulator
# import matplotlib.pyplot as plt


if __name__ == "__main__":
    # ser=serial.Serial('COM3',57600)
    ser='1'
    gl.set_value('flag',False) # Stop sign
     # initial heading angle zero
    gl.set_value('desired_angle',0)
    gl.set_value('sail',0) 
    gl.set_value('rudder',0)
    gl.set_value('frequency',10)
    gl.set_value('true_wind',[1.5,-math.pi/2])
    gl.set_value('target',[0,0]) 
    gl.set_value('x',0)
    gl.set_value('y',0)
    gl.set_value('roll',0)
    gl.set_value('heading_angle',0)
    
    
    gl.set_value('keeping_state',1)
    gl.set_value('tacking_angle',None)
    gl.set_value('current',0)
    gl.set_value('voltage',0)
    gl.set_value('keyboard_flag',False)
    gl.set_value('target_v',0.1)
    gl.set_value('reset',False)
    # gl.set_value('ser',ser)
    # conn = tcpserver.tcpserver()

    
    t1 = threading.Thread(target= controller_4_DoF.run,kwargs={'ser':ser}) # Receiving Commands
    t2 = threading.Thread(target= get_message.run,kwargs={'ser':ser})
    t3 = threading.Thread(target= data_writer.run)
    t4 = threading.Thread(target= simulator.run)
    t5 = threading.Thread(target= keyboard_control.main)
    
    
    t1.start() # start thread 1
    # t2.start() # start thread 2
    t3.start() # start thread 3
    t4.start()
    t5.start()
    my_plot=visualization.visualazation()
    my_plot.plot()

    t1.join() # wait for the t1 thread to complete
    # t2.join() # wait for the t2 thread to complete
    t3.join() # wait for the t3 thread to complete
    t4.join()
    t5.join()
    ser.close()
    # conn.close()
    time.sleep(1)
    print('Connection closed!')
    
    
#-----------------------------------------------------------


# import time
# import threading
# import controller
# import IMU_for_sailboat
# import current_sensor
# import data_writer


# if __name__ == "__main__":
    
#     my_IMU=IMU_for_sailboat.IMU()
#     my_current_sensor=current_sensor.c_sensor()
#     my_controller=
#     my_writer=data_writer.d_writer('test1.xls')
    
#     t1 = threading.Thread(target= my_IMU.run_IMU) # Receiving Commands
#     t2 = threading.Thread(target= my_current_sensor.run)
#     t3 = threading.Thread(target= my_writer.run)
    

#     t1.start() # start thread 1
#     t2.start() # start thread 2
#     t3.start() # start thread 3

    
#     t1.join() # wait for the t1 thread to complete
#     t2.join() # wait for the t2 thread to complete
#     t3.join() # wait for the t3 thread to complete

    
#     time.sleep(1)
#     print('Connection closed!')



#     thread1 :get IMU
#     thread2 :get sensor
#     thread3 :controller
#     thread4 :writer
