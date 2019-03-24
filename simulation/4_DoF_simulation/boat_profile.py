import numpy as np
import math

class boat_profile():
    def __init__(self,yaw=0,roll=0,x=0,y=0,boat_size=1):
        self.yaw  = yaw
        self.roll = roll
        self.x    = x
        self.y    = y
        self.boat_size=boat_size

        self.x_data=np.array([-1.5,  1,   1.5,  1,   -1.5])*self.boat_size
        self.y_data=np.array([-0.5, -0.5, 0,    0.5, 0.5])*self.boat_size

        self.current_x_data=np.array([-1.5,  1,   1.5,  1,   -1.5])*self.boat_size
        self.current_y_data=np.array([-0.5, -0.5, 0,    0.5, 0.5])*self.boat_size


        self.rudder_y_data=np.array([0, 0])*self.boat_size
        self.rudder_x_data=np.array([-1,-2])*self.boat_size


        self.sail_y_data=np.array([0  ,0 ])*self.boat_size
        self.sail_x_data=np.array([0.8,-1])*self.boat_size
        
    def set_boat_size(self,boat_size):
        self.boat_size=boat_size
        self.x_data=np.array([-1.5,  1,   1.5,  1,   -1.5])*self.boat_size
        self.y_data=np.array([-0.5, -0.5, 0,    0.5, 0.5])*self.boat_size

        self.current_x_data=np.array([-1.5,  1,   1.5,  1,   -1.5])*self.boat_size
        self.current_y_data=np.array([-0.5, -0.5, 0,    0.5, 0.5])*self.boat_size


        self.rudder_y_data=np.array([0, 0])*self.boat_size
        self.rudder_x_data=np.array([-1,-2])*self.boat_size


        self.sail_y_data=np.array([0  ,0 ])*self.boat_size
        self.sail_x_data=np.array([0.8,-1])*self.boat_size

    def get_lines(self,yaw,roll,x,y,rudder,sail):
        R=np.array([[math.cos(yaw),-math.sin(yaw)],
                    [math.sin(yaw),math.cos(yaw)]])
        for i in range(5):
            ## get boat line
            old_vector=np.array([ [self.x_data[i]] ,
                                  [self.y_data[i]]    ])
            new_vector=np.dot(R,old_vector)
            self.current_x_data[i]=new_vector[0]+x
            self.current_y_data[i]=new_vector[1]+y
        
        ## get rudder line
        R_rudder=np.array([[math.cos(yaw+rudder),-math.sin(yaw+rudder)],
                    [math.sin(yaw+rudder),math.cos(yaw+rudder)]])
         
        rudder_vector_1=np.array([[self.rudder_x_data[0]],
                                [self.rudder_y_data[0]] ])
        new_r_vector_1=np.dot(R,rudder_vector_1)
        rudder_vector_2=np.array([[-1*self.boat_size],
                                  [0] ])
        new_r_vector_2=np.dot(R_rudder,rudder_vector_2)
        current_rudder_x_data=np.array([new_r_vector_1[0]+x, new_r_vector_2[0]+new_r_vector_1[0]+x])
        current_rudder_y_data=np.array([new_r_vector_1[1]+y, new_r_vector_2[1]+new_r_vector_1[1]+y])

        ### get sail line
        R_sail=np.array([[math.cos(yaw+sail),-math.sin(yaw+sail)],
                    [math.sin(yaw+sail),math.cos(yaw+sail)]])
        
        sail_vector_1=np.array([[self.sail_x_data[0]],
                                [self.sail_y_data[0]] ])
        new_s_vector_1=np.dot(R,sail_vector_1)
        sail_vector_2=np.array([[-1.8*self.boat_size],
                                  [0] ])
        new_s_vector_2=np.dot(R_sail,sail_vector_2)
        current_sail_x_data=np.array([new_s_vector_1[0]+x,  new_s_vector_2[0]+new_s_vector_1[0]+x])
        current_sail_y_data=np.array([new_s_vector_1[1]+y,  new_s_vector_2[1]+new_s_vector_1[1]+y])
        
        

        current_x_data=self.current_x_data.flatten()
        current_y_data=self.current_y_data.flatten()
        current_rudder_x_data=current_rudder_x_data.flatten()
        current_rudder_y_data=current_rudder_y_data.flatten()
        current_sail_x_data=current_sail_x_data.flatten()
        current_sail_y_data=current_sail_y_data.flatten()
        
        return [(current_x_data, current_y_data), (current_rudder_x_data, current_rudder_y_data), (current_sail_x_data,current_sail_y_data)]


# my_boat=boat_profile()
# print(my_boat.get_lines(1,0,1,1,0,0))
# my_boat.set_boat_size(5)
# print(my_boat.get_lines(1,0,1,1,0,0))
# print(my_boat.current_x_data)
# print(my_boat.current_y_data)
