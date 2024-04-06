# This code computes the acceleration needed for a Fireball

import minecraft_motion_tools as mmt

v0 = float(input('Insert initial velocity: '))
t = float(input('Insert stop time in seconds: ')) * 20

a = mmt.a_from_double_v_t((v0, 0), (0, t))

if a is None:
    print('No solution found')
else:
    print(f'The acceleration needed is {a}')