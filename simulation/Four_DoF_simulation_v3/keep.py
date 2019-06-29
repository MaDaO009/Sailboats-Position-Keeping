import math
import copy

def sign(p):  
    if p>0:
        return 1
    elif p==0:
        return 0
    else:
        return -1

class reference_point():
    def __init__(self,accelerating_x_distance=1.1,wearing_y_distance=1.2):
        self.point1=[0,0]  #upper_left_point
        self.point2=[0,0]  #upper_right_point
        self.point3=[0,0]  #lower_left_point
        self.point4=[0,0]  #lower_right_point
        self.ref_point=None
        self.number_of_points=0
        self.accelerating_x_distance=accelerating_x_distance
        self.wearing_y_distance=wearing_y_distance

    def get_ref_point(self,target,true_wind):
        self.point1[0]=target[0]-self.accelerating_x_distance/1.8*math.cos(true_wind[1]+math.pi/2)-self.wearing_y_distance/1.8*math.cos(true_wind[1])
        self.point1[1]=target[1]-self.accelerating_x_distance/1.8*math.sin(true_wind[1]+math.pi/2)-self.wearing_y_distance/1.8*math.sin(true_wind[1])
        ##-    +   
        ##+    +

        self.point2[0]=target[0]+self.accelerating_x_distance/1.8*math.cos(true_wind[1]+math.pi/2)-self.wearing_y_distance/1.8*math.cos(true_wind[1])
        self.point2[1]=target[1]+self.accelerating_x_distance/1.8*math.sin(true_wind[1]+math.pi/2)-self.wearing_y_distance/1.8*math.sin(true_wind[1])
        ##+    +  
        ##-    -
        self.point3[0]=target[0]-self.accelerating_x_distance/1.8*math.cos(true_wind[1]+math.pi/2)+self.wearing_y_distance/3.5*math.cos(true_wind[1])
        self.point3[1]=target[1]-self.accelerating_x_distance/1.8*math.sin(true_wind[1]+math.pi/2)+self.wearing_y_distance/3.5*math.sin(true_wind[1])
        ##-    -  
        ##+    -
        self.point4[0]=target[0]+self.accelerating_x_distance/1.8*math.cos(true_wind[1]+math.pi/2)+self.wearing_y_distance/3.5*math.cos(true_wind[1])
        self.point4[1]=target[1]+self.accelerating_x_distance/1.8*math.sin(true_wind[1]+math.pi/2)+self.wearing_y_distance/3.5*math.sin(true_wind[1])
        ##+    - 
        ##-    -
        for i in range(1,5):
            exec ("print(self.point%s)"%i)

    def if_there_exist_points_according_to_heading_angle(self,true_wind,sailboat_x,sailboat_y,heading_angle):
        
        for i in range(1,5):
            exec('boat_to_point_angle%s=math.atan2(self.point%s[1]-sailboat_y,self.point%s[0]-sailboat_x)'%(i,i,i))
            exec('if math.sin(boat_to_point_angle%s-true_wind[1])*math.sin(heading_angle-true_wind[1])>=0:\n\tself.number_of_points+=1'%i)
            exec('print(boat_to_point_angle%s)'%i)
        number=self.number_of_points
        print(self.number_of_points)
        self.number_of_points=0
        if number==0:
            self.ref_point=None
        return number
    
    def select_farther_upper_point(self,sailboat_x,sailboat_y):
        
        distance1=math.sqrt((self.point1[0]-sailboat_x)**2+(self.point1[1]-sailboat_y)**2)
        distance2=math.sqrt((self.point2[0]-sailboat_x)**2+(self.point2[1]-sailboat_y)**2)
        if distance1>distance2:
            self.ref_point=self.point1
        else:
            self.ref_point=self.point2
        return self.ref_point
    
    def select_farther_lower_point(self,sailboat_x,sailboat_y):
        distance3=math.sqrt((self.point3[0]-sailboat_x)**2+(self.point3[1]-sailboat_y)**2)
        distance4=math.sqrt((self.point4[0]-sailboat_x)**2+(self.point4[1]-sailboat_y)**2)
        if distance3>distance4:
            self.ref_point=self.point3
        else:
            self.ref_point=self.point4
        print(reference_point)
        return self.ref_point



reference_point=reference_point()
reference_point.get_ref_point([3,5],[1,-math.pi/2])
reference_point.if_there_exist_points_according_to_heading_angle([1,-math.pi/2],4,5,0.5)


def keep_in_target_area():

    if there_exists_points_according_to_heading_angle():
        if in_up_wind_area(heading_angle,true_wind,position):
            reference_point=select_farther_upper_point()
        else:
            reference_point=select_farther_lower_point()
    
    else:
        if in_up_wind_area(heading_angle,true_wind,position):
            wear(initial_angle)
        else:
            if velocity[0]<0.35:
                wear(initial_angle)
            else:
                tack_if_is_able_to(initial_angle)


