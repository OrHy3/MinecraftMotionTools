import math
from scipy.special import lambertw
from scipy.optimize import brentq
from .velocity import check_values

def phi(x, a, b, c):
    '''
    This function is used to find the zeros in delta's derivative
    '''
    if x == 0:
        return -a * b
    return (a * c - b) * x * math.log(x) - (c * x - b) * (x - a)

def delta(x, a, b, c, k, right=True):
    '''
    Delta is the exponential function passed to Brent's algorithm.
    "right" parameter is used to determine the asymptotic value at a.
    '''
    if x == a:
        if x == 1:
            return 1 - k
        elif x > 1:
            if (right and b - a * c > 0) or (not right and b - a * c < 0):
                return math.inf
            else:
                return -k
        else:
            if (right and b - a * c > 0) or (not right and b - a * c < 0):
                return -k
            else:
                return math.inf
    if x == 0:
        temp = -a / b
        if temp == 0:
            return 1 - k
        elif temp > 0:
            return -k
        else:
            return math.inf
    if x == math.inf:
        if -c == 0:
            return 1 - k
        elif -c > 0:
            return math.inf
        else:
            return -k
    return x ** ((b - c * x) / (x - a)) - k

def phi1z(a, b, c):
    if b - a * c == 0:
        return []
    arg = math.exp(2 * a * c / (b - a * c)) * 2 * c / (b - a * c)
    if arg * math.e < -1:
        return []
    if arg * math.e == -1 or arg >= 0:
        return [lambertw(arg).real * (b - a * c) / c / 2]
    return [
        lambertw(arg).real * (b - a * c) / c / 2,
        lambertw(arg, -1).real * (b - a * c) / c / 2
    ]

def solve_equation(a, b, c, k=1):
    '''
    Function to solve the exponential equation.
    This is needed due to the fact that there isn't a way to use Lambert's W function on this kind of equation.
    '''

    itol = 1e-8

    if k <= 0:
        return []
    if b - a * c == 0:
        if a <= 0 or a == 1:
            return []
        x = math.log(k, a)
        if x == -c:
            return []
        return x
    
    phi1_zeros = phi1z(a, b, c)
    delta1_zeros = set()

    if phi1_zeros == []:
        if -a * b * (c if c else b) > 0:
            temp = 1
            while -a * b * phi(temp, a, b, c) > 0:
                temp *= 2
            delta1_zeros.append(brentq(phi, 0, temp, args=(a, b, c)))

    else:
        phi1_zeros.insert(0, 0)

        if phi(phi1_zeros[-1], a, b, c) * (c if c else b) > 0:
            phi1_zeros.append(phi1_zeros[-1] * 2)
            while phi(phi1_zeros[-1], a, b, c) * phi(phi1_zeros[-2], a, b, c) > 0:
                phi1_zeros[-1] *= 2

        for i in range(len(phi1_zeros) - 1):
            if phi(phi1_zeros[i], a, b, c) * phi(phi1_zeros[i + 1], a, b, c) < 0:
                delta1_zeros.add(brentq(phi, phi1_zeros[i], phi1_zeros[i + 1], args=(a, b, c)))

    delta1_zeros -= {0, a}
    delta1_zeros = list(delta1_zeros)
    delta1_zeros.sort()

    if a == 1:
        check_map = {math.fabs(delta1_zeros[i] - 1): i for i in range(len(delta1_zeros))}
        if check_map != {} and min(check_map) < itol:
            delta1_zeros.pop(check_map[min(check_map)])

    solutions = set()

    if delta1_zeros == []:
        if delta(0, a, b, c, k) * delta(math.inf, a, b, c, k) < 0:
            temp = 1
            while delta(0, a, b, c, k) * delta(temp, a, b, c, k) > 0:
                temp *= 2
            solutions.add(brentq(delta, 0, temp, args=(a, b, c, k)))

    else:
        delta1_zeros.insert(0, 0)

        if a > 0:
            for i in range(len(delta1_zeros) - 1):
                if a > delta1_zeros[i] and a < delta1_zeros[i + 1]:
                    delta1_zeros.insert(i + 1, a)
                    break
            else:
                delta1_zeros.append(a)

        if delta(delta1_zeros[-1], a, b, c, k) * delta(math.inf, a, b, c, k) < 0:
            delta1_zeros.append(delta1_zeros[-1] * 2)
            while delta(delta1_zeros[-1], a, b, c, k) * delta(delta1_zeros[-2], a, b, c, k) > 0:
                delta1_zeros[-1] *= 2

        for i in range(len(delta1_zeros) - 1):
            if delta(delta1_zeros[i], a, b, c, k) * delta(delta1_zeros[i + 1], a, b, c, k, delta1_zeros[i + 1] != a) < 0:
                solutions.add(brentq(delta, delta1_zeros[i], delta1_zeros[i + 1], args=(a, b, c, k, delta1_zeros[i + 1] != a)))

    solutions -= {0, a}
    solutions = list(solutions)
    solutions.sort()
    
    return [(b - c * sol) / (sol - a) for sol in solutions]

def solve_quadratic(a, b, c):
    '''
    This is a simple function to solve 2nd grade polynomials.
    '''
    if a == 0:
        return [-c / b]
    arg = b ** 2 - 4 * a * c
    solutions = []
    if arg == 0:
        solutions.append(-b / a / 2)
    elif arg > 0:
        solutions.append((-b - arg ** 0.5) / a / 2)
        solutions.append((-b + arg ** 0.5) / a / 2)
        solutions.sort()
    return solutions

def a_from_double_v_t(first: tuple, second: tuple, d=0.05, after=True):
    '''
    Retrieves acceleration from 2 states of velocity/time.

    Returns a single value solution.
    Returns None if no solution can be found.

    Default parameters refer to Fireballs.

    first: first state pair
    second: second state pair
    d: drag force
    after: whether drag is applied after or before gravity acceleration
    '''
    check_values(d)
    v1, t1 = first
    v2, t2 = second
    if d == 0:
        if t2 - t1 == 0:
            return None
        return (v1 - v2) / (t2 - t1)
    arg = (1 - d) ** t2 - (1 - d) ** t1
    if arg == 0:
        return None
    a = (v2 * (1 - d) ** t1 - v1 * (1 - d) ** t2) * d / arg
    if after:
        a /= 1 - d
    return a

def a_from_double_p_t(first: tuple, second: tuple, d=0.05, after=True, k=0):
    '''
    Retrieves acceleration from 2 states of position/time.

    Returns a single value solution.
    Returns None if no solution can be found.

    Default parameters refer to Fireballs.

    first: first state pair
    second: second state pair
    d: drag force
    after: whether drag is applied after or before gravity acceleration
    k: acceleration drag coefficient
    '''
    check_values(d)
    p1, t1 = first
    p2, t2 = second
    if d == 0:
        if t1 == 0 or t2 == 0 or t2 - t1 == 0:
            return None
        return (p1 / t1 - p2 / t2) * 2 / (t2 - t1)
    if after:
        k /= 1 - d
    if 1 + k * d == 0:
        return None
    arg = t2 * (1 - (1 - d) ** t1) - t1 * (1 - (1 - d) ** t2)
    if arg == 0:
        return None
    a = (p1 * (1 - (1 - d) ** t2) - p2 * (1 - (1 - d) ** t1)) * d / (1 + k * d) / arg
    if after:
        a /= 1 - d
    return a

def a_from_double_v_p(first: tuple, second: tuple, d=0.05, after=True, k=0):
    '''
    Attempts to retrieve the acceleration from 2 states of velocity/position.
    If drag is set to 0, a safe algorithm will be used.

    Returns a tuple of the possible solutions.
    Returns None if no solution can be found.

    Default parameters refer to Fireballs.

    first: first state pair
    second: second state pair
    d: drag force
    after: whether drag is applied after or before gravity acceleration
    k: acceleration drag coefficient
    '''
    check_values(d)
    v1, p1 = first
    v2, p2 = second
    if d == 0:
        arg = 2 * (p2 - p1) + (1 - 2 * k) * (v2 - v1)
        if arg == 0:
            return None
        a = (v1 ** 2 - v2 ** 2) / arg
        if ((k - 0.5) * a - v1) ** 2 + 2 * a * p1 < 0 or ((k - 0.5) * a - v2) ** 2 + 2 * a * p2 < 0:
            return None
        return (a,)
    if after:
        k /= 1 - d
    if 1 + k * d == 0:
        return None
    a = solve_equation(1, v1 * d, v2 * d, (1 - d) ** ((v2 - v1 + (p2 - p1) * d) / (1 + k * d)))
    for i in range(len(a) - 1, -1, -1):
        if math.log(1 - d) * (v1 / a[i] + 1 / d) / (1 + k * d) * (1 - d) ** (((v1 + p1 * d) / a[i] + 1 / d) / (1 + k * d)) * math.e < -1 or math.log(1 - d) * (v2 / a[i] + 1 / d) / (1 + k * d) * (1 - d) ** (((v2 + p2 * d) / a[i] + 1 / d) / (1 + k * d)) * math.e < -1:
            a.pop(i)
    if a == []:
        return None
    if after:
        a = [sol / (1 - d) for sol in a]
    return tuple(a)

def a_from_v_t_p_t(first: tuple, second: tuple, d=0.05, after=True, k=0):
    '''
    Retrieves acceleration from 2 states of velocity/time and position/time.

    Returns a single value solution.
    Returns None if no solution can be found.

    Default parameters refer to Fireballs.

    first: first state pair
    second: second state pair
    d: drag force
    after: whether drag is applied after or before gravity acceleration
    k: acceleration drag coefficient
    '''
    check_values(d)
    v1, t1 = first
    p2, t2 = second
    if d == 0:
        arg = t2 * (t2 - 2 * t1 - 1 + 2 * k)
        if arg == 0:
            return None
        return 2 * (v1 * t2 - p2) / arg
    if after:
        k /= 1 - d
    arg = (1 - (1 - d) ** t2) / d - t2 * (1 + k * d) * (1 - d) ** t1
    if arg == 0:
        return None
    a = (p2 * d * (1 - d) ** t1 - v1 * (1 - (1 - d) ** t2)) / arg
    if after:
        a /= 1 - d
    return a

def a_from_v_t_v_p(first: tuple, second: tuple, d=0.05, after=True, k=0):
    '''
    Attempts to retrieve the acceleration from 2 states of velocity/time and velocity/position.
    If drag is set to 0, a safe algorithm will be used.

    Returns a tuple of the possible solutions.
    Returns None if no solution can be found.

    Default parameters refer to Fireballs.

    first: first state pair
    second: second state pair
    d: drag force
    after: whether drag is applied after or before gravity acceleration
    k: acceleration drag coefficient
    '''
    check_values(d)
    v1, t1 = first
    v2, p2 = second
    if d == 0:
        a = solve_quadratic(t1 * (2 * k - 1 - t1), (v2 - v1) * (1 - 2 * k) + 2 * (p2 - v1 * t1), v2 ** 2 - v1 ** 2)
        for i in range(len(a)):
            if ((k - 0.5) * a[i] - v2) ** 2 + 2 * a[i] * p2 < 0:
                a.pop(i)
        if a == []:
            return None
        return tuple(a)
    if after:
        k /= 1 - d
    if 1 + k * d == 0:
        return None
    gamma = (1 - d) ** (((1 - d) ** -t1 - 1) / d / (1 + k * d) - t1)
    a = solve_equation(gamma, gamma * v1 * d, v2 * d, (1 - d) ** ((v2 - v1 * (1 - d) ** -t1 + p2 * d) / (1 + k * d)))
    for i in range(len(a) - 1, -1, -1):
        if math.log(1 - d) * (v2 / a[i] + 1 / d) / (1 + k * d) * (1 - d) ** (((v2 + p2 * d) / a[i] + 1 / d) / (1 + k * d)) * math.e < -1:
            a.pop(i)
    if a == []:
        return None
    if after:
        a = [sol / (1 - d) for sol in a]
    return tuple(a)

def a_from_p_t_v_p(first: tuple, second: tuple, d=0.05, after=True, k=0):
    '''
    Attempts to retrieve the acceleration from 2 states of position/time and velocity/position.
    If drag is set to 0, a safe algorithm will be used.

    Returns a tuple of the possible solutions.
    Returns None if no solution can be found.

    Default parameters refer to Fireballs.

    first: first state pair
    second: second state pair
    d: drag force
    after: whether drag is applied after or before gravity acceleration
    k: acceleration drag coefficient
    '''
    check_values(d)
    p1, t1 = first
    v2, p2 = second
    if d == 0:
        if t1 == 0:
            return None
        a = solve_quadratic(k * (k - 1) + (1 - t1 ** 2) / 4, v2 * (1 - 2 * k) + 2 * p2 - p1, v2 ** 2 - p1 ** 2 / t1 ** 2)
        for i in range(len(a)):
            if ((k - 0.5) * a[i] - v2) ** 2 + 2 * a[i] * p2 < 0:
                a.pop(i)
        if a == []:
            return None
        return tuple(a)
    if after:
        k /= 1 - d
    if 1 + k * d == 0:
        return None
    arg = 1 - (1 - d) ** t1
    if arg == 0:
        return None
    gamma = (1 - d) ** (t1 / arg - 1 / d / (1 + k * d)) * d / arg
    a = solve_equation(gamma * (1 + k * d) * t1, gamma * p1 * d, v2 * d, (1 - d) ** ((v2 + (p2 - p1 / arg) * d) / (1 + k * d)))
    for i in range(len(a) - 1, -1, -1):
        if math.log(1 - d) * (v2 / a[i] + 1 / d) / (1 + k * d) * (1 - d) ** (((v2 + p2 * d) / a[i] + 1 / d) / (1 + k * d)) * math.e < -1:
            a.pop(i)
    if a == []:
        return None
    if after:
        a = [sol / (1 - d) for sol in a]
    return tuple(a)