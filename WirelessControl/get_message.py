import serial
import time
import globalvar as gl
import math
import re
# print('!!!!!!!!!')
def run(ser):
    # print('!!!')
    b=0
    heading_angle=gl.get_value('heading_angle')
    while True:
        if gl.get_value('flag'):
                    
            break


        mess=0
        mess=ser.readline()
        mess=bytes.decode(mess)
        mess=str(mess)
        
        if mess!=0:
            
            mess=mess.split(',')
            # print(mess)
            if len(mess)==3:
                a=mess[0]
                a=re.sub('\D','',a)
                voltage=mess[1]
                current=mess[2]
                current=re.sub('\D','',current)
                current=float(current)/100
                voltage=float(voltage)
                

                
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
        time.sleep(1/frequency)