# This code computes current distance for a Fireball after being hit

import minecraft_motion_tools as mmt

t = float(input('Time in seconds: ')) * 20

if t < 0:
    print('Time cannot be lower than 0!')
    exit()

print(f'Current fireball\'s distance: {mmt.p_from_t(1, t, a=-0.1, d=0.05, k=0)}')