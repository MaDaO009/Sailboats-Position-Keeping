
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
    