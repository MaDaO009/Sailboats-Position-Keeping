import test2
import globalvar as gl
import threadind
my_plot=visualazation()
my_plot.plot()

gl.set_value('keeping_state',1)
gl.set_value('tacking_state','not')

# conn = tcpserver.tcpserver()

t1 = threading.Thread(target= controller_4_DoF.run) # Receiving Commands
t2 = threading.Thread(target= IMU.IMU)
t3 = threading.Thread(target= sensor.sensor)
t4 = threading.Thread(target= database.run)


t1.start() # start thread 1
t2.start() # start thread 2
t3.start() # start thread 3
t4.start()

t1.join() # wait for the t1 thread to complete
t2.join() # wait for the t2 thread to complete
t3.join() # wait for the t3 thread to complete
t4.join()

self.p1=0        ##drift coefficient####relative big for the plastic sailboat
        self.p2=4         ##tangential friction
        self.p3=2.5        ##angular friction
        self.p4=1.8         ##sail lift
        self.p5=30        ##rudder lift
        self.p6=0.05         ##distance to sail
        self.p7=0.05         ##distance to mast
        self.p8=0.25           ##distance to rudder
        self.p9=3         ##mass of boat
        self.p10=0.3        ##moment of inertia
        self.p11=0.3  
        self.p12=0.002   #wind effect on w   
        self.p13=0.045 #wind effect on v
        self.time=0