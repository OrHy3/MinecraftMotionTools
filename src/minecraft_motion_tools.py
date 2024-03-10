from scipy.special import lambertw
import math

def check_values(a, d):
    '''
    Checks wheter acceleration and drag parameters are in the permitted ranges (a >= 0, 0 <= d < 1).

    a: acceleration
    d: drag force
    '''
    if d < 0 or d >= 1 or a < 0:
        raise ValueError('Inappropriate parameters (see help(check_values))')

def v_from_t(v0: float, t: float, a=0.04, d=0.02, after=True):
    '''
    Retrieves velocity from an initial velocity and the time that has passed, in ticks.

    Default parameters refer to Falling Blocks.

    v0: initial velocity
    t: ticks passed
    a: acceleration
    d: drag force
    after: whether drag is applied after or before gravity acceleration
    '''
    check_values(a, d)
    if d == 0:
        return v0 - a * t
    if after:
        a *= 1 - d
    return ((v0 * d + a) * (1 - d) ** t - a) / d

def p_from_t(v0: float, t: float, a=0.04, d=0.02, after=True, k=1):
    '''
    Retrieves relative position from an initial velocity and the time that has passed, in ticks.

    Default parameters refer to Falling Blocks.

    v0: initial velocity
    t: ticks passed
    a: acceleration
    d: drag force
    after: whether drag is applied after or before gravity acceleration
    k: acceleration drag coefficient
    '''
    check_values(a, d)
    if d == 0:
        return (v0 + (0.5 - 0.5 * t - k) * a) * t
    if after:
        a *= 1 - d
        k /= 1 - d
    return ((v0 * d + a) * (1 - (1 - d) ** t) / d - a * t) / d - k * a * t

def max_height_tick_from_v0(v0: float, a=0.04, d=0.02, after=True, k=1):
    '''
    Retrieves the time in ticks the maximux relative height is reached.
    Can be negative.

    Returns None if no solution can be found.

    Default parameters refer to Falling Blocks.

    v0: initial velocity
    a: acceleration
    d: drag force
    after: whether drag is applied after or before gravity acceleration
    k: acceleration drag coefficient
    '''
    check_values(a, d)
    if d == 0:
        if a == 0:
            return None
        return v0 / a - k
    if after:
        a *= 1 - d
        k /= 1 - d
    arg = v0 * d + a
    if arg == 0:
        return None
    arg = (1 + k * d) * a / arg
    if arg <= 0:
        return None
    return math.log(arg, 1 - d)

def max_height_from_v0(v0: float, a=0.04, d=0.02, after=True, k=1):
    '''
    Retrieves the maximux relative height reached (using integer approximation of the tick).
    Can be an height reached in a previous tick.

    If acceleration is 0 returns the approximate ending position.
    Returns None if there is no ending position.

    Returns None if no solution can be found.

    Default parameters refer to Falling Blocks.

    v0: initial velocity
    a: acceleration
    d: drag force
    after: whether drag is applied after or before gravity acceleration
    k: acceleration drag coefficient
    '''
    check_values(a, d)
    if a == 0:
        if d == 0:
            return None
        return v0 / d
    t = max_height_tick_from_v0(v0, a, d, after, k)
    if t is None:
        return None
    return p_from_t(v0, math.ceil(t), a, d, after, k)

def v0_from_max_height(h: float, a=0.04, d=0.02, after=True, k=1):
    '''
    Retrieves a tuple of up to 2 solutions, each representing a closed interval with lower and upper bounds.

    The first tuple gives the approximate velocity after the maximum relative height specified has been reached, following the fall to position 0,
    the second tuple gives the approximate velocity to reach the maximum relative height specified, yet to reach.

    If the acceleration is 0 returns a single value.
    Returns None if no solution can be found.

    Default parameters refer to Falling Blocks.

    h: maximum height required, positive
    a: acceleration
    d: drag force
    after: whether drag is applied after or before gravity acceleration
    k: acceleration drag coefficient
    '''
    check_values(a, d)
    if h <= 0:
        raise ValueError('Maximum height must be greater than 0')
    if a == 0:
        if d == 0:
            return None
        return h * d
    if d == 0:
        return (
            ((k * 2 - 1 - (h * 8 / a + 1) ** 0.5) * a / 2, (k * 2 - 1 - (h * 8 / a) ** 0.5) * a / 2),
            ((k * 2 - 1 + (h * 8 / a) ** 0.5) * a / 2, (k * 2 - 1 + (h * 8 / a + 1) ** 0.5) * a / 2)
        )
    if after:
        a *= 1 - d
        k /= 1 - d
    arg = a * (1 + k * d)
    if arg == 0:
        return None
    v0 = [
        (
            a * ((1 + k * d) * lambertw(-(1 - d) ** (h * d / arg - 1 / math.log(1 - d))).real / math.log(1 - d) - 1 / d),
            a * ((1 + k * d) * lambertw(math.log(1 - d) * (1 - d) ** (h * d / arg + 1 / d) / d).real / math.log(1 - d) - 1 / d)
        ),
        (
            a * ((1 + k * d) * lambertw(-(1 - d) ** (h * d / arg - 1 / math.log(1 - d)), -1).real / math.log(1 - d) - 1 / d),
            a * ((1 + k * d) * lambertw(math.log(1 - d) * (1 - d) ** (h * d / arg + 1 / d) / d, -1).real / math.log(1 - d) - 1 / d)
        )
    ]
    if max_height_tick_from_v0(v0[1][0], a, d, False, k) is None or max_height_tick_from_v0(v0[1][1], a, d, False, k) is None:
        v0.pop(1)
    if max_height_tick_from_v0(v0[0][0], a, d, False, k) is None or max_height_tick_from_v0(v0[0][1], a, d, False, k) is None:
        v0.pop(0)
    if len(v0) > 0:
        return tuple(v0)
    return None

def v0_from_v_t(v: float, t: float, a=0.04, d=0.02, after=True):
    '''
    Retrieves initial velocity from a pair of current velocity and time passed, in ticks.

    Default parameters refer to Falling Blocks.

    v: current velocity
    t: ticks passed
    a: acceleration
    d: drag force
    after: whether drag is applied after or before gravity acceleration
    '''
    check_values(a, d)
    if d == 0:
        return v + t * a
    if after:
        a *= 1 - d
    return (v + a / d) * (1 - d) ** -t - a / d

def v0_from_p_t(p: float, t: float, a=0.04, d=0.02, after=True, k=1):
    '''
    Retrieves initial velocity from a pair of current relative position and time passed, in ticks.

    Returns None if no solution can be found, or there are infinite solutions.

    Default parameters refer to Falling Blocks.

    p: current relative position
    t: ticks passed
    a: acceleration
    d: drag force
    after: whether drag is applied after or before gravity acceleration
    k: acceleration drag coefficient
    '''
    check_values(a, d)
    if t == 0:
        return None
    if d == 0:
        return p / t + (t - 1 + k * 2) * a / 2
    if after:
        a *= 1 - d
        k /= 1 - d
    return (p * d + a * t * (1 + k * d)) / (1 - (1 - d) ** t) - a / d

def t_from_v0_v(v0: float, v: float, a=0.04, d=0.02, after=True):
    '''
    Retrieves the time passed (in ticks) since velocity was v0 to become v.

    Returns None if no solution can be found.

    Default parameters refer to Falling Blocks.

    v0: initial velocity
    v: current velocity
    a: acceleration
    d: drag force
    after: whether drag is applied after or before gravity acceleration
    '''
    check_values(a, d)
    if d == 0:
        if a == 0:
            return None
        return (v0 - v) / a
    if after:
        a *= 1 - d
    arg = v0 * d + a
    if arg == 0:
        return None
    arg = (v * d + a) / arg
    if arg <= 0:
        return None
    return math.log(arg, 1 - d)

def t_from_v0_p(v0: float, p: float, a=0.04, d=0.02, after=True, k=1):
    '''
    Retrieves the time passed (in ticks) to reach the relative position specified.

    Returns a tuple of up to 2 solutions, None if no solution can be found.

    Default parameters refer to Falling Blocks.

    v0: initial velocity
    p: current position
    a: acceleration
    d: drag force
    after: whether drag is applied after or before gravity acceleration
    k: acceleration drag coefficient
    '''
    check_values(a, d)
    if d == 0:
        if a == 0:
            return None
        arg = (v0 + a * (0.5 - k)) ** 2 - p * a * 2
        if arg < 0:
            return None
        if arg == 0:
            return (v0 / a + 0.5 - k,)
        return (
            (v0 - arg ** 0.5) / a + 0.5 - k,
            (v0 + arg ** 0.5) / a + 0.5 - k
        )
    if a == 0:
        if v0 == 0:
            return None
        arg = 1 - p * d / v0
        if arg <= 0:
            return None
        return math.log(arg, 1 - d)
    if after:
        a *= 1 - d
        k /= 1 - d
    if 1 + k * d == 0:
        return None
    arg = math.log(1 - d) * (v0 / a + 1 / d) / (1 + k * d) * (1 - d) ** ((v0 / a + 1 / d - p * d / a) / (1 + k * d))
    if arg * math.e < -1:
        return None
    if arg * math.e == -1 or arg >= 0:
        return ((v0 / a + 1 / d - p * d / a) / (1 + k * d) - lambertw(arg).real / math.log(1 - d),)
    return (
        (v0 / a + 1 / d - p * d / a) / (1 + k * d) - lambertw(arg, -1).real / math.log(1 - d),
        (v0 / a + 1 / d - p * d / a) / (1 + k * d) - lambertw(arg).real / math.log(1 - d)
    )

def v0_t_from_v_p(v: float, p: float, a=0.04, d=0.02, after=True, k=1):
    '''
    Retrieves a pair of initial velocity and time passed (in ticks) to reach the state of current velocity/position specified.

    Returns up to 2 solutions, None if no solution can be found.

    Default parameters refer to Falling Blocks.

    v: current velocity
    p: current relative position
    a: acceleration
    d: drag force
    after: whether drag is applied after or before gravity acceleration
    k: acceleration drag coefficient
    '''
    check_values(a, d)
    if d == 0:
        if a == 0:
            if v == 0:
                return None
            return ((v, p / v),)
        arg = ((k - 0.5) * a - v) ** 2 + p * a * 2
        if arg < 0:
            return None
        if arg == 0:
            t = k - 0.5 - v / a
            return ((v + t * a, t),)
        t = (
            k - 0.5 - (v + arg ** 0.5) / a,
            k - 0.5 - (v - arg ** 0.5) / a
        )
        return (
            (v + t[0] * a, t[0]),
            (v + t[1] * a, t[1])
        )
    if a == 0:
        if v == 0:
            return None
        v0 = v + p * d
        if v0 == 0:
            return None
        arg = v / v0
        if arg <= 0:
            return None
        return ((v0, math.log(arg, 1 - d)))
    if after:
        a *= 1 - d
        k /= 1 - d
    if 1 + k * d == 0:
        return None
    arg = math.log(1 - d) * (v / a + 1 / d) / (1 + k * d) * (1 - d) ** (((v + p * d) / a + 1 / d) / (1 + k * d))
    if arg >= 0:
        v0 = a * (lambertw(arg).real * (1 + d) / math.log(1 - d) - 1 / d)
        return ((v0, (v0 - v - p * d) / a / (1 + k * d)),)
    else:
        v0 = (
            a * (lambertw(arg).real * (1 + k * d) / math.log(1 - d) - 1 / d),
            a * (lambertw(arg, -1).real * (1 + k * d) / math.log(1 - d) - 1 / d)
        )
        return (
            (v0[0], (v0[0] - v - p * d) / a / (1 + k * d)),
            (v0[1], (v0[1] - v - p * d) / a / (1 + k * d))
        )