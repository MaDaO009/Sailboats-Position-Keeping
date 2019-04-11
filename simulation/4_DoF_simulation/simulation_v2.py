import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.gridspec as gridspec
import time
import math
import threading
from sailboat_4_DOF_v2 import sailboat
import random
import four_DOF_simulator
import boat_profile


class visualazation():
    def __init__(self):
        self.initialize_parameters()
        self.create_window()
        self.init_subwindows_data()
        self.init_boat_data()
        self.init_window_data()
        
    def initialize_parameters(self):
        self.start_time=time.time()
        self.my_boat=sailboat(position=[2,3,0,0])
        self.boat_generator=boat_profile.boat_profile(boat_size=0.15)
        
        self.all_line=[]
        self.heading_angle=0
        self.desired_angle=0
        self.rudder=0
        self.sail=0
        self.x=2
        self.y=3
        self.v=0
        self.u=0
        self.w=0
        self.target=self.my_boat.target
        self.boat_size=0.15
        self.sample_time=0.01
        self.velocity=[0,0]
        self.app_wind=[0,0]
        self.angular_velocity,self.roll_angular_velocity=0,0
        self.last_sail=0
        self.roll=0
        # self.true_wind=[self.my_boat.true_wind[0],math.pi/2-self.my_boat.true_wind[1]]
        self.true_wind=self.my_boat.true_wind
        # print('bbbbb',self.my_boat.true_wind[1])
        self.true_wind[1]=math.pi/2-self.true_wind[1]
        print('aaaaaa',self.my_boat.true_wind[1])
    
    def create_window(self):
        self.figure = plt.figure()
        self.gs1 = gridspec.GridSpec(1, 1)
        self.gs2 = gridspec.GridSpec(3, 1)

        self.main_window=self.figure.add_subplot(self.gs1[0])
        ##this part is for target area and pre-arrive area.
        theta = np.linspace(0, 2*np.pi,60)
        x_t,y_t = np.cos(theta)*self.my_boat.dT+np.linspace(self.my_boat.target[0],self.my_boat.target[0],60), np.sin(theta)*self.my_boat.dT+np.linspace(self.my_boat.target[1],self.my_boat.target[1],60)
        self.main_window.plot(x_t, y_t, color='red', linewidth=1.0)
        
        x_p,y_p = np.cos(theta)*self.my_boat.dM+np.linspace(self.my_boat.target[0],self.my_boat.target[0],60), np.sin(theta)*self.my_boat.dM+np.linspace(self.my_boat.target[1],self.my_boat.target[1],60)
        self.main_window.plot(x_p, y_p, color='orange', linewidth=1.0)


        self.main_window.axis('equal')

        plt.xlim(0,8)
        plt.ylim(-2,10)
        self.gs1.tight_layout(self.figure, rect=[0, 0, 0.7, 1])

        self.forward_velocity_window = self.figure.add_subplot(self.gs2[0])
        plt.xlabel('forward velocity')
        plt.ylim(-0.2,1)
        self.side_velocity_window = self.figure.add_subplot(self.gs2[1])
        plt.xlabel('side velocity')
        plt.ylim(-0.2,0.2)
        self.angular_velocity_window = self.figure.add_subplot(self.gs2[2])
        plt.xlabel('angular velocity')
        plt.ylim(-1,1)
        self.gs2.tight_layout(self.figure, rect=[0.7, 0, 1, 1], h_pad=0.5)



        top = min(self.gs1.top, self.gs2.top)
        bottom = max(self.gs1.bottom, self.gs2.bottom)

        self.gs1.update(top=top, bottom=bottom)
        self.gs2.update(top=top, bottom=bottom)

    def init_subwindows_data(self):
        self.location_x_data = np.linspace(self.my_boat.position[0],self.my_boat.position[0],300)
        self.location_y_data=np.linspace(self.my_boat.position[1],self.my_boat.position[1],300)
        self.trajectory_line, = self.main_window.plot(self.location_x_data,self.location_y_data)
        self.v_x_data = np.linspace(0, 5, 60)
        self.v_data=np.linspace(self.v,self.v,60)
        self.line_forward_velocity, = self.forward_velocity_window.plot(self.v_x_data, self.v_data)
        # x2_data = np.linspace(0, 5, 60)
        self.u_data=np.linspace(self.u,self.u,60)
        self.line_side_velocity, = self.side_velocity_window.plot(self.v_x_data, self.u_data)
        # x3_data = np.linspace(0, 5, 60)
        self.heading_data=np.linspace(self.heading_angle,self.heading_angle,60)
        self.line_heading, = self.angular_velocity_window.plot(self.v_x_data, self.heading_data)
        self.desired_angle_data=np.linspace(self.desired_angle,self.desired_angle,60)
        self.line_desired_angle, = self.angular_velocity_window.plot(self.v_x_data, self.desired_angle_data,color='gray')
        self.all_line.append(self.trajectory_line)
        self.all_line.append(self.line_forward_velocity)
        self.all_line.append(self.line_side_velocity)
        self.all_line.append(self.line_heading)
        
        
        
    def init_boat_data(self):
        # global current_x_data, current_y_data, current_rudder_x_data, current_rudder_y_data, current_sail_x_data,current_sail_y_data
        
        # current_x_data,current_y_data,current_rudder_x_data,current_rudder_y_data,current_sail_x_data,current_sail_y_data=self.boat_generator.get_lines(0,0,0,0,0,0)
        data=self.boat_generator.get_lines(0,0,0,0,0,0)
        
        for i in range(3):
            exec ("self.line%s,=self.main_window.plot(data[%d][0],data[%d][0],color='b')"%(i+1,i,i))
            exec ("self.all_line.append(self.line%s)"%(i+1))
        
        
        self.line_disired_angle,=self.main_window.plot([1.5*math.cos(self.heading_angle)*self.boat_size,1.5*math.cos(self.heading_angle)+math.cos(self.desired_angle)*self.boat_size],
                                    [1.5*math.sin(self.heading_angle)*self.boat_size,1.5*math.sin(self.heading_angle)+math.sin(self.desired_angle)*self.boat_size],color='gray')
        self.all_line.append(self.line_disired_angle)

    def init_window_data(self):
        self.window_y_data=np.array([0,2.5,2.5,2.5,5,5])
        self.window_x_data=np.array([5.5,5.5,8,5.5,5.5,8])
        self.line_window,=self.main_window.plot(self.window_x_data,self.window_y_data,color='b')

        self.boundary_y_data=np.array([2,2,8,8,2])
        self.boundary_x_data=np.array([0.8,5.5,5.5,0.8,0.8])
        
        self.line_boundary,=self.main_window.plot(self.boundary_x_data,self.boundary_y_data,color='gray',linestyle='--')
        
        self.boat_generator.set_boat_size(0.75)
        data=self.boat_generator.get_lines(0,0,6.75,1.25,0,0)
        self.boat_generator.set_boat_size(0.15)
        for i in range(3):
            exec ("self.window_line%s,=self.main_window.plot(data[%d][0],data[%d][1],color='b')"%(i+1,i,i))
            exec ("self.all_line.append(self.window_line%s)"%(i+1))
        
        self.wind_y_data=np.array([3.75,5])
        self.wind_x_data=np.array([6.75,6.75])
        self.line_wind,=self.main_window.plot(self.wind_x_data,self.wind_y_data,color='b')
        
        self.all_line.append(self.line_window)
        self.all_line.append(self.line_boundary)
        self.all_line.append(self.line_wind)
        
    def init1(self):  # only required for blitting to give a clean slate.
        # print(self.all_line)
        return self.all_line

    def to_next_moment(self):
        # self.rudder,self.target_sail=self.my_boat.rudder+0,self.my_boat.sail+0
        # print('aaaaaaaaaaaaaaaaasail',self.sail)
        
        
        for i in range(0,10):
            self.moving_sail()
    
            self.true_sail=self.get_true_sail()
            a,b,self.app_wind=four_DOF_simulator.to_next_moment(0.01,self.velocity[0],-self.velocity[1],-self.roll_angular_velocity,-self.angular_velocity,self.y,self.x,-self.roll,math.pi/2-self.heading_angle,self.true_sail,self.rudder,self.true_wind)
            [self.velocity[0],self.velocity[1],self.roll_angular_velocity,self.angular_velocity]=-a
            self.app_wind[1]=-self.app_wind[1]
            self.velocity[0]*=-1
            # print(self.velocity,'v')

            
            [self.y,self.x,self.roll,self.heading_angle]=b
            self.roll=-self.roll
            self.heading_angle=math.pi/2-self.heading_angle
            
            # print(self.roll)
        # print("aaaaaa")
        # print(wind_effect_on_v,g_s*math.sin(self.sail))
        self.rudder,self.target_sail,self.desired_angle=self.my_boat.update_state(self.true_wind,[self.x,self.y,self.roll,self.heading_angle])
        #+random.gauss(0,0.01)
        print(self.target_sail,self.sail,self.true_sail,self.app_wind)
        
    def moving_sail(self):
        
        try:
            if abs(self.target_sail-self.last_sail)>0.01:
                self.sail+=self.sign(self.target_sail-self.last_sail)*0.01
                # print('moving sail')
        except:
            print('an exception occurred when moving sail')
        self.last_sail=self.sail
   
    def get_true_sail(self):
        sail=self.sail
        
        if math.sin(self.app_wind[1])<0:
            sail=-sail
            # print('!!!!',self.sail,self.my_boat.if_force_turning)
            
        if math.cos(self.app_wind[1])>math.cos(sail) or abs(self.app_wind[1]-sail)<0.1:
            sail=self.app_wind[1]
            # print('!!!\n!!!!!!',self.sail,self.my_boat.if_force_turning)
        # print(self.app_wind[1],sail)
        
        
        return sail

    def animate1(self,i):
        # self.to_next_moment()
        # self.to_next_moment()
        # self.to_next_moment()
        # self.to_next_moment()
        self.to_next_moment()
        # print(self.my_boat.true_wind)
        self.update_data()
        
        self.update_line_boat()
        
        self.update_window_boat()
        
        self.update_wind()
        
        return self.all_line
        # return self.trajectory_line,self.line_forward_velocity,self.line_side_velocity,self.line_heading,self.line1,self.line2,self.line3,self.window_line1,self.window_line2,self.window_line3,self.line_wind,self.line_disired_angle,self.line_boundary,self.line_desired_angle

    def update_data(self):
        self.desired_angle=self.my_boat.desired_angle
        
        [self.v,self.u,self.p,self.w]=self.my_boat.velocity
        
        # print(self.v,u)
        self.location_x_data=np.delete(self.location_x_data,0,0)
        self.location_x_data=np.append(self.location_x_data,[self.x],0)
        self.location_y_data=np.delete(self.location_y_data,0,0)
        self.location_y_data=np.append(self.location_y_data,[self.y],0)
        self.trajectory_line.set_data(self.location_x_data,self.location_y_data)

        self.v_data=np.delete(self.v_data,0,0)
        self.v_data=np.append(self.v_data,[self.v],0)
        self.line_forward_velocity.set_ydata(self.v_data)  # update the data.

        
        self.u_data=np.delete(self.u_data,0,0)
        self.u_data=np.append(self.u_data,[self.u],0)
        self.line_side_velocity.set_ydata(self.u_data)  # update the data.
        self.heading_data=np.delete(self.heading_data,0,0)
        self.heading_data=np.append(self.heading_data,[self.w],0)
        self.line_heading.set_ydata(self.heading_data)
        self.desired_angle_data=np.delete(self.desired_angle_data,0,0)
        self.desired_angle_data=np.append(self.desired_angle_data,[self.desired_angle],0)
        self.line_desired_angle.set_ydata(self.desired_angle_data)

    def update_line_boat(self): 
        data=self.boat_generator.get_lines(self.heading_angle,self.roll,self.x,self.y,self.rudder,self.true_sail)
        
        for i in range(3):
            # exec ("self.line%s,=self.main_window.plot(data[%d][0],data[%d][1],color='b')"%(i+1,i,i))
            exec ("self.all_line[%d].set_data([data[%d][0],data[%d][1]])"%(i+4,i,i))
        
        self.all_line[7].set_data([1.5*math.cos(self.heading_angle)*self.boat_size+self.x,1.5*math.cos(self.heading_angle)*self.boat_size+math.cos(self.desired_angle)*self.boat_size+self.x],
                                    [1.5*math.sin(self.heading_angle)*self.boat_size+self.y,1.5*math.sin(self.heading_angle)*self.boat_size+math.sin(self.desired_angle)*self.boat_size+self.y])

    def update_window_boat(self):
        self.boat_generator.set_boat_size(0.75)
        data=self.boat_generator.get_lines(self.heading_angle,self.roll,6.75,1.25,self.rudder,self.true_sail)
        self.boat_generator.set_boat_size(0.15)
        for i in range(3):
            # exec ("self.window_line%s,=self.main_window.plot(data[%d][0],data[%d][1],color='b')"%(i+1,i,i))
            exec ("self.all_line[%d].set_data([data[%d][0],data[%d][1]])"%(i+8,i,i))
            
    def update_wind(self):
        coo_wind=[0,-2]
        # del_x=coo_wind[0]*2*self.boat_size
        # del_y=coo_wind[1]*2*self.boat_size
        del_x=-math.sin(self.roll)
        del_y=math.cos(self.roll)
        self.wind_y_data=np.array([3.75,del_y+3.75])
        self.wind_x_data=np.array([6.75,del_x+6.75])
        self.line_wind,=self.main_window.plot(self.wind_x_data,self.wind_y_data,color='black')

    def sign(self,p):
        if p>0:
            return 1
        elif p<0:
            return -1
        else :
            return 0
        
    def plot(self):
        ani = animation.FuncAnimation(
            self.figure, self.animate1, init_func=self.init1, interval=60, blit=True, save_count=50)
    
        plt.show()
        plt.close()
    
my_plot=visualazation()
my_plot.plot()
