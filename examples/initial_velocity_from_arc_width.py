# This code computes initial velocity for a primed TNT

import minecraft_motion_tools as mmt

width = float(input('Insert arc\'s width: '))
t = float(input('Time taken in seconds: ')) * 20

if t == 0:
    print('Time cannot be 0!')
    exit()

motion_x = mmt.v0_from_p_t(width, t, a=0)
motion_y = mmt.v0_from_p_t(0, t)

print('Horizontal velocity:', motion_x)
print('Vertical velocity:', motion_y)