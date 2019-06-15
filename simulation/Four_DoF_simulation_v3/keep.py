
dely=
delx=
if dely>-0.3: #在上半部分
    if abs(delx)<0.6: #在中间
        ref_point=
    else: 
        ref_point=
        ref_angle=
        if sign(ref_angle)!=sign(heading) and cos(heading-wind_angle)<cos(ref_angle-wind_angle):
            tack_or_turn()
        else:
            line_follow



else:#在下半部分
