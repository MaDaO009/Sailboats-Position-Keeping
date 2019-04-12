import math


def run(velocity,position,target,true_wind,dT,dM,last_desired_angle,tacking_angle,tacking_sign,
start_tacking_time,counter,keeping_state):
    
    boat_to_target_angle=math.atan2(target[1]-position[1],target[0]-position[0])
    distance_st=math.sqrt(pow(target[1]-position[1],2)+pow(target[0]-position[0],2))
    
    force_turning_angle=boundary_detector(position,tacking_angle)
    
    

    if distance_st>dT:
        keeping_state=0
        desired_angle=go_to_target_area(boat_to_target_angle,distance_st,dM,dT,true_wind)
    else:
        desired_angle,keeping_state=keeping_in_target_area(position,distance_st,target,keeping_state,
        true_wind,boat_to_target_angle)
    # print('last1',last_desired_angle,desired_angle)
    tacking_angle,tacking_sign,start_tacking_time,desired_angle=tacking_detector(velocity[0],position[3],desired_angle,
    last_desired_angle,tacking_angle,tacking_sign,true_wind,start_tacking_time,counter)
    # print('last3',last_desired_angle,desired_angle)

    if force_turning_angle!=None:
        tacking_angle=None
        

    elif tacking_angle!=None:
        
        force_turning_angle=None
    
    return [desired_angle,keeping_state,force_turning_angle,tacking_angle,tacking_sign,start_tacking_time]


def boundary_detector(position,tacking_angle):
    if tacking_angle== None:
        x=position[0]+math.cos(position[3]*1.3)
        y=position[1]+math.sin(position[3]*1.3)
        if x>0 and x<6 and y>1 and y<7.5:
            force_turning_angle=None
        else:
            if x<0:
                if y<7:
                    force_turning_angle=0.6
                else:
                    force_turning_angle=-0.6
            elif x>6:
                if y<7:
                    force_turning_angle=2.5
                else:
                    force_turning_angle=-2.5
            else: 
                force_turning_angle=None
        return force_turning_angle
    else:
        return None

def tacking_detector(v,heading_angle,desired_angle,last_desired_angle,tacking_angle,tacking_sign,true_wind,
start_tacking_time,counter):
    if tacking_angle ==None:
        if math.cos(heading_angle-true_wind[1])+math.cos(desired_angle-true_wind[1])<0:
            # print(next_desired_angle,heading_angle)
            # print(' tacking!')
            if sign(math.sin(desired_angle-true_wind[1])) != sign(math.sin(heading_angle-true_wind[1])):
                ###Yes, it's a tacking!
                print('Yes, it is a tacking!')
                if v>0.9:
                    start_tacking_time=counter
                    tacking_sign=sign(math.sin(heading_angle-true_wind[1]))
                    tacking_angle=desired_angle
                else:
                    # print('last2',last_desired_angle,desired_angle)
                    desired_angle=last_desired_angle
                    # print('last4',last_desired_angle,desired_angle)

    else:
    ### is tacking
        is_success=(tacking_sign !=sign(math.sin(heading_angle-true_wind[1])))
        if is_success or counter-start_tacking_time>35 or v<0:
            start_tacking_time=None
            tacking_sign=None
            tacking_angle=None
    return tacking_angle,tacking_sign,start_tacking_time,desired_angle

def go_to_target_area(boat_to_target_angle,distance_st,dM,dT,true_wind):
    next_desired_angle=boat_to_target_angle
        
    if distance_st<dM and distance_st>dT:
        if math.cos(boat_to_target_angle-true_wind[1])>0.4: ##not able to slow down
            
            if math.cos(boat_to_target_angle-(true_wind[1]+math.pi/2))>math.cos(boat_to_target_angle-(true_wind[1]-math.pi/2)):
                next_desired_angle=-math.pi/2+boat_to_target_angle
            else:
                next_desired_angle=math.pi/2+boat_to_target_angle

    if math.cos(true_wind[1]-next_desired_angle)<-0.71: ##exceed dead angle
        next_desired_angle=sign(math.sin(true_wind[1]-next_desired_angle))*0.98+true_wind[1]+math.pi
    next_desired_angle=regular_angle(next_desired_angle)
    return next_desired_angle

def keeping_in_target_area(position,distance_st,target,keeping_state,true_wind,boat_to_target_angle):
    del_x=distance_st*math.sin(true_wind[1]-boat_to_target_angle)
    del_y=distance_st*math.cos(true_wind[1]-boat_to_target_angle)
    if (del_x**2/3.24+del_y**2<1 and keeping_state!=2) or keeping_state==0:
        keeping_state=1
        desired_angle=true_wind[1]+math.pi+sign(math.sin(true_wind[1]-position[3]))*0.9
        desired_angle=regular_angle(desired_angle)
    elif del_x**2/3.24+del_y**2>1 :
        if  keeping_state==1:
            keeping_state=2
       
    if keeping_state==2:
        if sign(math.sin(position[3]-true_wind[1])) != sign(math.sin(boat_to_target_angle-true_wind[1])):
            if abs(math.sin(position[3]-true_wind[1]))>0.8:
                keeping_state=3
    if keeping_state==3:
        desired_angle=sign(math.sin(true_wind[1]-position[3]))*0.95+true_wind[1]+math.pi
    
    desired_angle=regular_angle(desired_angle)
    return desired_angle,keeping_state
        

    
    



def sign(p):
        
    if p>0:
        return 1
    elif p==0:
        return 0
    else:
        return -1

def regular_angle(angle):
        
    while angle>math.pi:
        angle-=math.pi*2
    while angle<-math.pi:
        angle+=math.pi*2
    return angle


# run([0,0,0,0],[1,1,0,0],[1,1.5],[1,1.5],1,2,False,None)