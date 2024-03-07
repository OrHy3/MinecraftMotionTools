# This code computes initial velocity for a Thrown potion

import minecraft_motion_tools as mmt

h = float(input('Insert maximum height: '))

if h <= 0:
    print('Maximum height must be greater than 0!')
    exit()

solutions = mmt.v0_from_max_height(h, a=0.05, d=0.01, after=False)
print(f'Y axis\' velocity is between {solutions[1][0]} and {solutions[1][1]}')