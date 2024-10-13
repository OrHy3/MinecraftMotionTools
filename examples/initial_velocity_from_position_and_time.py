# This code computes initial velocity for a Mob

import minecraft_motion_tools as mmt

x = float(input('X offset: '))
y = float(input('Y offset: '))
z = float(input('Z offset: '))
t = float(input('Time in seconds: ')) * 20

if t == 0:
    print('Time cannot be 0!')
    exit()

motion = [
    mmt.v0_from_p_t(x, t, a=0, d=0.09, k=0),
    mmt.v0_from_p_t(y, t, a=0.08, d=0.02, k=0),
    mmt.v0_from_p_t(z, t, a=0, d=0.09, k=0)
]

print(f'Motion tag: [{motion[0]}d, {motion[1]}d, {motion[2]}d]')