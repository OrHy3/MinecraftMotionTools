# This code computes the acceleration needed for a Wind charge

import minecraft_motion_tools as mmt

p = float(input('Insert position: '))
t = float(input('Insert time (when to reach position) in seconds: ')) * 20
h = float(input('Insert max height: '))

if h <= 0:
    print('Maximum height must be greater than 0!')
    exit()

a = mmt.a_from_p_t_v_p((p, t), (0, h), d=0)

if a is None:
    print('No solution found')
else:
    v0 = mmt.v0_from_p_t(p, t, a=a[0], d=0)
    print(f'The acceleration needed is {a[0]} and the initial velocity is {v0}')