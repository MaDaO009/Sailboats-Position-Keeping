"""
Updated on FRI DEC 29 13:56:39 2018

@author: Zeyuan Feng

@contributor: fahah & Lianxin Zhang

*Get the command from sailboat object.
*Execute the command
*Update the global values
"""

import time
import globalvar as gl
from sailboat_4_DoF import sailboat
import math
import serial 
import re



def send(ser,rudder,sail,heading_angle):
    rudder_output=90-9*rudder*rudder-50*rudder
    sail_output=20+sail*53
    if math.sin(heading_angle-math.pi/2)>0:
        sail_output=20+(sail_output-20)*9/8
    command=rudder_output//1*100+sail_output
    command=(',,'+str(command)+',').encode(encoding='utf-8')
    ser.write(command)

#-------------Receiving Commands-----------------
def run(ser):
    # print('!')
    #-----------ESC Configuration----------------------
    
    # ser=gl.get_value('ser')
    gl.set_value('x',0)
    gl.set_value('y',0)
    gl.set_value('flag',False)
    rudder=0
    sail=0

    
    
    my_boat=sailboat()
    target=my_boat.target
    gl.set_value('target',target)
    times=0
    last_rudder_value=0
    last_sail_value=0
    while True:
        times=(times+1)%10
        # get_message(ser)
        if my_boat.flag==True:
            gl.set_value('flag',True)
            print('Program stops!',my_boat.d)
            
            break

        ## change the frequency of communication when the sailboat arrives at its target area
        # if my_boat.if_keeping==True:
        #     gl.set_value('frequency',20)
        # else:
        #     gl.set_value('frequency',10)

        frequency=gl.get_value('frequency')
        ##get information of sailboat
        x=gl.get_value('x')
        y=gl.get_value('y')
        heading_angle=gl.get_value('heading_angle')
        my_boat.frequency=frequency
        my_boat.updata_pos(x,y,heading_angle,0)
        v=my_boat.velocity[0]
        u=my_boat.velocity[1]
        w=my_boat.angular_velocity
        # tacking_state=my_boat.tacking_state
        keeping_state=my_boat.keeping_state
        
        ##control the rudder and sail
        rudder,sail,desired_angle=my_boat.update_state()
        rudder= float('{0:.2f}'.format(rudder))
        sail= float('{0:.2f}'.format(sail))
        send(ser,rudder,sail,heading_angle)

        # print(rudder)
        last_rudder_value=rudder
        last_sail_value=sail

        #change the global variables
        gl.set_value('tacking_state',my_boat.tacking_state)
        gl.set_value('v',v)
        gl.set_value('u',u)
        gl.set_value('w',w)
        
        # print(u,v,w)
        # gl.set_value('rudder',rudder) # PWM for Motor1
        # gl.set_value('sail',sail) # PWM for Motor2
        gl.set_value('desired_angle',desired_angle)
        gl.set_value('keeping_state',keeping_state)
        time.sleep(1/frequency)
    
    # End the program        
    
    send(ser,0,0,heading_angle)
    print('Motors Stopped \n')
    time.sleep(0.5)
   
 

def sign(x):
    if x>0:
        return 1
    elif x==0:
        return 0
    else:
        return -1

def get_message(ser):
    mess=0
    mess=ser.readline()
    mess=bytes.decode(mess)
    mess=str(mess)
    print(mess)
    if mess!=0:
        
        mess=mess.split(',')
        # print(mess)
        a=mess[0]
        a=re.sub('\D','',a)
        voltage=mess[1]
        current=mess[2]

        
        try:    
            b=int(a)
        except:
            b=b
    
    heading_angle=b/57.32
    if heading_angle>math.pi:
        heading_angle-=math.pi*2
    
    gl.set_value('heading_angle',heading_angle)
    gl.set_value('current',current)
    gl.set_value('voltage',voltage)

    frequency=gl.get_value('frequency')
    ser.flushInput()
#    conn.close()
#    time.sleep(1)
#    print('Connection closed!')

#------------------------------------------------
