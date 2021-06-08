
import four_DOF_simulator 
import GUI
import threading
import numpy as np
from time import time,sleep
import math
from sailboat_v3 import sailboat
import four_DOF_simulator_v2

class simulator:
    def __init__(self,controller=sailboat(),init_pose=np.array([0,0,0,0]),init_v=[0,0,0,0],GUI_EN=False,total_step=1000,
            true_wind=[1.5,-math.pi/2],command_cycle=0.1,simulation_cycle=0.001,GUI_cycle=0.02,sail_command=0,true_sail=0,
            rudder_command=0):
        self.controller=sailboat(position=init_pose,true_wind=true_wind)
        self.dynamic_model=four_DOF_simulator.single_sailboat_4DOF_simulator(location_and_orientation=init_pose,sample_time=simulation_cycle)
        self.GUI=GUI.scene_displayer(pos_and_orientation=init_pose,cycle=GUI_cycle)
        
        self.counter=0
        self.location_and_orientation=np.array(init_pose)
        self.velocity_and_angular_v=np.array(init_v)
        self.true_sail=true_sail
        self.sail_command=sail_command
        self.rudder_command=rudder_command
        self.GUI_EN=GUI_EN
        self.stop_signal=False
        self.total_step=total_step
        self.command_cycle=command_cycle
        self.simulation_cycle=simulation_cycle
        self.GUI_cycle=GUI_cycle
        self.true_wind=true_wind

    def update_info_with_GUI(self):
        while (not self.stop_signal):
            self.GUI.update_pose(self.location_and_orientation,self.rudder_command,self.true_sail,self.stop_signal)
            # print(self.rudder_command,self.true_sail)
            sleep(self.GUI_cycle)


    def compute_dynamic(self):
        while (not self.stop_signal):
            start_time=time()
            self.velocity_and_angular_v,self.location_and_orientation,self.true_sail=\
                self.dynamic_model.step(self.location_and_orientation,self.velocity_and_angular_v,self.sail_command,\
                    self.rudder_command, self.true_wind)

            
            sleep_time=self.simulation_cycle-(time()-start_time)

            if sleep_time>0:
                sleep(sleep_time)
        
    def compute_command(self):
        while (not self.stop_signal):
            self.counter+=1
            start_time=time()
            self.rudder_command,self.sail_command,a,b=self.controller.update_state(self.true_wind,self.location_and_orientation)
            sleep_time=self.command_cycle-(time()-start_time)
            if sleep_time>0:
                sleep(sleep_time)
            if self.counter>self.total_step:
                self.stop_signal=True


    def run(self):
        t1 = threading.Thread(target= self.GUI.main) 
        t2 = threading.Thread(target= self.update_info_with_GUI)
        t3 = threading.Thread(target= self.compute_dynamic)
        t4 = threading.Thread(target= self.compute_command)

        t1.start() # start thread 1
        print("t1_start")
        t2.start()
        print("t2_start")
        t3.start()
        print("t3_start")
        t4.start()
        print("t4_start")
        t1.join() # wait for the t1 thread to complete
        t2.join()
        t3.join()
        t4.join()
        
a=simulator(total_step=1000,simulation_cycle=0.01)
a.run()
