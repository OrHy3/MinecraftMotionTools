from scipy.special import lambertw
import math

def check_values(a, d):
    '''
    Checks wheter acceleration and drag parameters are in the permitted ranges (a >= 0, 0 <= d < 1).

    a: gravity acceleration
    d: drag force
    '''
    return d >= 0 and d < 1 and a >= 0

def v_from_t(v0: float, t: float, a=0.04, d=0.02, after=True):
    '''
    Retrieves velocity from an initial velocity and the time that has passed, in ticks.

    Default parameters refer to Falling Blocks.

    v0: initial velocity
    t: ticks passed
    a: gravity acceleration
    d: drag force
    after: whether drag is applied after or before gravity acceleration
    '''
    if not check_values(a, d):
        raise ValueError('Inappropriate parameters (look help(check_values))')
    if d == 0:
        return v0 - a * t
    if after:
        a *= 1 - d
    return ((v0 * d + a) * (1 - d) ** t - a) / d

def p_from_t(v0: float, t: float, a=0.04, d=0.02, after=True, slowed_pos=True):
    '''
    Retrieves relative position from an initial velocity and the time that has passed, in ticks.

    Default parameters refer to Falling Blocks.

    v0: initial velocity
    t: ticks passed
    a: gravity acceleration
    d: drag force
    after: whether drag is applied after or before gravity acceleration
    slowed_pos: whether gravity acceleration is subtracted after applying velocity
    '''
    if not check_values(a, d):
        raise ValueError('Inappropriate parameters (look help(check_values))')
    if d == 0:
        return (v0 - a * (t + (1 if slowed_pos else -1)) / 2) * t
    if slowed_pos:
        if after:
            return (((v0 * d + a * (1 - d))) * (1 - (1 - d) ** t) / d - a * t) / d
        else:
            return ((v0 * d + a) * (1 - (1 - d) ** t) / d - a * (1 + d) * t) / d
    else:
        if after:
            a *= 1 - d
        return ((v0 * d + a) * (1 - (1 - d) ** t) / d - a * t) / d

def max_height_tick_from_v0(v0: float, a=0.04, d=0.02, after=True, slowed_pos=True):
    '''
    Retrieves the time in ticks the maximux relative height is reached.
    Can be negative.

    Returns None if no solution can be found.

    Default parameters refer to Falling Blocks.

    v0: initial velocity
    a: gravity acceleration
    d: drag force
    after: whether drag is applied after or before gravity acceleration
    slowed_pos: whether gravity acceleration is subtracted after applying velocity
    '''
    if d == 0:
        if a == 0:
            return None
        return v0 / a + (-1 if slowed_pos else 0)
    if not check_values(a, d):
        raise ValueError('Inappropriate parameters (look help(check_values))')
    if slowed_pos:
        if after:
            arg = v0 * d + a * (1 - d)
            if arg == 0:
                return None
            arg = a / arg
        else:
            arg = v0 * d + a
            if arg == 0:
                return None
            arg = a * (1 + d) / arg
    else:
        if after:
            a *= 1 - d
        arg = v0 * d + a
        if arg == 0:
            return None
        arg = a / arg
    if arg <= 0:
        return None
    return math.log(arg, 1 - d)

def max_height_from_v0(v0: float, a=0.04, d=0.02, after=True, slowed_pos=True):
    '''
    Retrieves the maximux relative height reached (using integer approximation of the tick).
    Can be an height reached in a previous tick.

    If acceleration is 0 returns the approximate ending position.
    Returns None if there is no ending position.

    Returns None if no solution can be found.

    Default parameters refer to Falling Blocks.

    v0: initial velocity
    a: gravity acceleration
    d: drag force
    after: whether drag is applied after or before gravity acceleration
    slowed_pos: whether gravity acceleration is subtracted after applying velocity
    '''
    if not check_values(a, d):
        raise ValueError('Inappropriate parameters (look help(check_values))')
    if a == 0:
        if d == 0:
            return None
        return v0 / d
    t = max_height_tick_from_v0(v0, a, d, after, slowed_pos)
    if t is None:
        return None
    return p_from_t(v0, math.ceil(t), a, d, after, slowed_pos)

def v0_from_max_height(h: float, a=0.04, d=0.02, after=True, slowed_pos=True):
    '''
    Retrieves 2 tuples, each representing a closed interval with lower and upper bounds.

    The first tuple gives the approximate velocity after the maximum relative height specified has been reached, following the fall to position 0,
    the second tuple gives the approximate velocity to reach the maximum relative height specified, yet to reach.

    If the acceleration is 0 returns a single value,
    None if drag is 0 as well.

    Default parameters refer to Falling Blocks.

    h: maximum height required, positive
    a: gravity acceleration
    d: drag force
    after: whether drag is applied after or before gravity acceleration
    slowed_pos: whether gravity acceleration is subtracted after applying velocity
    '''
    if not check_values(a, d) or h <= 0:
        raise ValueError('Inappropriate parameters (look help(check_values))')
    if a == 0:
        if d == 0:
            return None
        return h * d
    if d == 0:
        return (
            (((1 if slowed_pos else -1) - (h * 8 / a + 1) ** 0.5) * a / 2, ((1 if slowed_pos else -1) - (h * 8 / a) ** 0.5) * a / 2),
            (((1 if slowed_pos else -1) + (h * 8 / a) ** 0.5) * a / 2, ((1 if slowed_pos else -1) + (h * 8 / a + 1) ** 0.5) * a / 2)
        )
    if slowed_pos:
        if after:
            return (
                (
                    a * (lambertw(-(1 - d) ** (h * d / a - 1 / math.log(1 - d))).real / math.log(1 - d) + 1 - 1 / d),
                    a * (lambertw(math.log(1 - d) * (1 - d) ** (h * d / a + 1 / d) / d).real / math.log(1 - d) + 1 - 1 / d)
                ),
                (
                    a * (lambertw(-(1 - d) ** (h * d / a - 1 / math.log(1 - d)), -1).real / math.log(1 - d) + 1 - 1 / d),
                    a * (lambertw(math.log(1 - d) * (1 - d) ** (h * d / a + 1 / d) / d, -1).real / math.log(1 - d) + 1 - 1 / d)
                )
            )
        else:
            return (
                (
                    a * ((1 + d) * lambertw(-(1 - d) ** (h * d / a / (1 + d) - 1 / math.log(1 - d))).real / math.log(1 - d) - 1 / d),
                    a * ((1 + d) * lambertw(math.log(1 - d) * (1 - d) ** (h * d / a / (1 + d) + 1 / d) / d).real / math.log(1 - d) - 1 / d)
                ),
                (
                    a * ((1 + d) * lambertw(-(1 - d) ** (h * d / a / (1 + d) - 1 / math.log(1 - d)), -1).real / math.log(1 - d) - 1 / d),
                    a * ((1 + d) * lambertw(math.log(1 - d) * (1 - d) ** (h * d / a / (1 + d) + 1 / d) / d, -1).real / math.log(1 - d) - 1 / d)
                )
            )
    else:
        if after:
            a *= 1 - d
        return (
            (
                a * (lambertw(-(1 - d) ** (h * d / a - 1 / math.log(1 - d))).real / math.log(1 - d) - 1 / d),
                a * (lambertw(math.log(1 - d) * (1 - d) ** (h * d / a + 1 / d) / d).real / math.log(1 - d) - 1 / d)
            ),
            (
                a * (lambertw(-(1 - d) ** (h * d / a - 1 / math.log(1 - d)), -1).real / math.log(1 - d) - 1 / d),
                a * (lambertw(math.log(1 - d) * (1 - d) ** (h * d / a + 1 / d) / d, -1).real / math.log(1 - d) - 1 / d)
            )
        )

def v0_from_v_t(v: float, t: float, a=0.04, d=0.02, after=True):
    '''
    Retrieves initial velocity from a pair of current velocity and time passed, in ticks.

    Default parameters refer to Falling Blocks.

    v: current velocity
    t: ticks passed
    a: gravity acceleration
    d: drag force
    after: whether drag is applied after or before gravity acceleration
    '''
    if not check_values(a, d):
        raise ValueError('Inappropriate parameters (look help(check_values))')
    if d == 0:
        return v + t * a
    if after:
        return (v + a * (1 - d) / d) * (1 - d) ** -t + a - a / d
    else:
        return (v + a / d) * (1 - d) ** -t - a / d

def v0_from_p_t(p: float, t: float, a=0.04, d=0.02, after=True, slowed_pos=True):
    '''
    Retrieves initial velocity from a pair of current relative position and time passed, in ticks.

    Returns None if no solution can be found, or there are infinite solutions.

    Default parameters refer to Falling Blocks.

    p: current relative position
    t: ticks passed
    a: gravity acceleration
    d: drag force
    after: whether drag is applied after or before gravity acceleration
    slowed_pos: whether gravity acceleration is subtracted after applying velocity
    '''
    if not check_values(a, d):
        raise ValueError('Inappropriate parameters (look help(check_values))')
    if t == 0:
        return None
    if d == 0:
        return p / t + (t + (1 if slowed_pos else -1)) * a / 2
    if slowed_pos:
        if after:
            return (p * d + a * t) / (1 - (1 - d) ** t) + a - a / d
        else:
            return (p * d + a * t * (1 + d)) / (1 - (1 - d) ** t) - a / d
    else:
        if after:
            a *= 1 - d
        return (p * d + a * t) / (1 - (1 - d) ** t) - a / d

def t_from_v0_v(v0: float, v: float, a=0.04, d=0.02, after=True):
    '''
    Retrieves the time passed (in ticks) since velocity was v0 to become v.

    Returns None if no solution can be found.

    Default parameters refer to Falling Blocks.

    v0: initial velocity
    v: current velocity
    a: gravity acceleration
    d: drag force
    after: whether drag is applied after or before gravity acceleration
    '''
    if not check_values(a, d):
        raise ValueError('Inappropriate parameters (look help(check_values))')
    if d == 0:
        if a == 0:
            return None
        return (v0 - v) / a
    if after:
        arg = v0 * d + a - a * d
        if arg == 0:
            return None
        arg = (v * d + a - a * d) / arg
        if arg <= 0:
            return None
        return math.log(arg, 1 - d)
    else:
        arg = v0 * d + a
        if arg == 0:
            return None
        arg = (v * d + a) / arg
        if arg <= 0:
            return None
        return math.log(arg, 1 - d)

def t_from_v0_p(v0: float, p: float, a=0.04, d=0.02, after=True, slowed_pos=True):
    '''
    Retrieves the time passed (in ticks) to reach the relative position specified.

    Returns a tuple of up to 2 solutions, None if no solution can be found.

    Default parameters refer to Falling Blocks.

    v0: initial velocity
    p: current position
    a: gravity acceleration
    d: drag force
    after: whether drag is applied after or before gravity acceleration
    slowed_pos: whether gravity acceleration is subtracted after applying velocity
    '''
    if not check_values(a, d):
        raise ValueError('Inappropriate parameters (look help(check_values))')
    if (a == 0 and v0 == 0) or p > max_height_from_v0(v0, a, d, after):
        return None
    if d == 0:
        if a == 0:
            return None
        arg = (v0 + (-a if slowed_pos else a) / 2) ** 2 - p * a * 2
        if arg < 0:
            return None
        if arg == 0:
            return (((v0 + (-a if slowed_pos else a) / 2) / a))
        return (
            (v0 + (-a if slowed_pos else a) / 2 - arg ** 0.5) / a,
            (v0 + (-a if slowed_pos else a) / 2 + arg ** 0.5) / a
        )
    if a == 0:
        arg = 1 - p * d / v0
        if arg <= 0:
            return None
        return math.log(arg, 1 - d)
    if slowed_pos:
        if after:
            return (
                v0 / a + 1 / d - 1 - p * d / a - lambertw(math.log(1 - d) * (v0 / a + 1 / d - 1) * (1 - d) ** (v0 / a + 1 / d - 1 - p * d / a), -1).real / math.log(1 - d),
                v0 / a + 1 / d - 1 - p * d / a - lambertw(math.log(1 - d) * (v0 / a + 1 / d - 1) * (1 - d) ** (v0 / a + 1 / d - 1 - p * d / a)).real / math.log(1 - d)
            )
        else:
            return (
                (v0 / a + 1 / d - p * d / a) / (1 + d) - lambertw(math.log(1 - d) * (v0 / a + 1 / d) / (1 + d) * (1 - d) ** ((v0 / a + 1 / d - p * d / a) / (1 + d)), -1).real / math.log(1 - d),
                (v0 / a + 1 / d - p * d / a) / (1 + d) - lambertw(math.log(1 - d) * (v0 / a + 1 / d) / (1 + d) * (1 - d) ** ((v0 / a + 1 / d - p * d / a) / (1 + d))).real / math.log(1 - d)
            )
    else:
        if after:
            a *= 1 - d
        return (
            (v0 - p * d) / a + 1 / d - lambertw(math.log(1 - d) * (v0 / a + 1 / d) * (1 - d) ** ((v0 - p * d) / a + 1 / d), -1).real / math.log(1 - d),
            (v0 - p * d) / a + 1 / d - lambertw(math.log(1 - d) * (v0 / a + 1 / d) * (1 - d) ** ((v0 - p * d) / a + 1 / d)).real / math.log(1 - d)
        )

def v0_t_from_v_p(v: float, p: float, a=0.04, d=0.02, after=True, slowed_pos=True):
    '''
    Retrieves a pair of initial velocity and time passed (in ticks) to reach the state of current velocity/position specified.

    Returns up to 2 solutions, None if no solution can be found.

    Default parameters refer to Falling Blocks.

    v: current velocity
    p: current relative position
    a: gravity acceleration
    d: drag force
    after: whether drag is applied after or before gravity acceleration
    slowed_pos: whether gravity acceleration is subtracted after applying velocity
    '''
    if not check_values(a, d):
        raise ValueError('Inappropriate parameters (look help(check_values))')
    if d == 0:
        if a == 0:
            return None
        arg = (a / 2 + (-v if slowed_pos else v)) ** 2 + p * a * 2
        if arg < 0:
            return None
        if arg == 0:
            t = -v / a + (0.5 if slowed_pos else -0.5)
            return ((v + t * a, t))
        t = (
            (-v - arg ** 0.5) / a + (0.5 if slowed_pos else -0.5),
            (-v + arg ** 0.5) / a + (0.5 if slowed_pos else -0.5)
        )
        return (
            (v + t[0] * a, t[0]),
            (v + t[1] * a, t[1])
        )
    if a == 0:
        if v == 0 or 1 + p * d / v <= 0:
            return None
        v0 = v + p * d
        return ((v0, math.log(v / v0, 1 - d)))
    if slowed_pos:
        if after:
            arg = math.log(1 - d) * (v / a - 1 + 1 / d) * (1 - d) ** ((v + p * d) / a - 1 + 1 / d)
            if arg >= 0:
                v0 = a * (lambertw(arg).real / math.log(1 - d) + 1 - 1 / d)
                return ((v0, (v0 - v - p * d) / a))
            else:
                v0 = (
                    a * (lambertw(arg).real / math.log(1 - d) + 1 - 1 / d),
                    a * (lambertw(arg, -1).real / math.log(1 - d) + 1 - 1 / d)
                )
                return (
                    (v0[0], (v0[0] - v - p * d) / a),
                    (v0[1], (v0[1] - v - p * d) / a)
                )
        else:
            arg = math.log(1 - d) * (v / a + 1 / d) / (1 + d) * (1 - d) ** ((v + p * d) / a / (1 + d) + 1 / d / (1 + d))
            if arg >= 0:
                v0 = a * (lambertw(arg).real * (1 + d) / math.log(1 - d) - 1 / d)
                return ((v0, (v0 - v - p * d) / a / (1 + d)))
            else:
                v0 = (
                    a * (lambertw(arg).real * (1 + d) / math.log(1 - d) - 1 / d),
                    a * (lambertw(arg, -1).real * (1 + d) / math.log(1 - d) - 1 / d)
                )
                return (
                    (v0[0], (v0[0] - v - p * d) / a / (1 + d)),
                    (v0[1], (v0[1] - v - p * d) / a / (1 + d))
                )
    else:
        if after:
            a *= 1 - d
        arg = math.log(1 - d) * (v / a + 1 / d) * (1 - d) ** ((v + p * d) / a + 1 / d)
        if arg >= 0:
            v0 = a * (lambertw(arg).real / math.log(1 - d) - 1 / d)
            return ((v0, (v0 - v - p * d) / a))
        else:
            v0 = (
                a * (lambertw(arg).real / math.log(1 - d) - 1 / d),
                a * (lambertw(arg, -1).real / math.log(1 - d) - 1 / d)
            )
            return (
                (v0[0], (v0[0] - v - p * d) / a),
                (v0[1], (v0[1] - v - p * d) / a)
            )