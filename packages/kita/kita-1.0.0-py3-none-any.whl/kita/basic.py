pi = 3.141592653589793

def card(E):
    return len(E)

def gcd(a:int,b:int):
    a,b = (a**2)**0.5, (b**2)**0.5
    while b:
        a,b = b, a%b
    return int(a)

def sqrt(x:float):
    return x**(1/2)

def seq_sum(function, from_n:int, to_k:int):
    sequence_sum = 0
    while from_n <= to_k:
        sequence_sum += function(from_n)
        from_n += 1
    return sequence_sum

def seq_mul(function, from_n:int, to_k:int):
    sequence_sum = 1
    while from_n <= to_k:
        sequence_sum *= function(from_n)
        from_n += 1
    return sequence_sum

def factorial(n:int):
    result = 1
    for i in range(1, n+1):
        result *= i
    return result

def deg(x):
    rad = x * pi/180
    return rad

def sin(x:float):  # Taylor Expansion
    k = 0
    sinx = 0
    while x >= pi:
        x -= pi
    if pi > x > pi / 2:
        x = pi - x
    while k < 15:
        sinx += (-1)**k * x**(2*k + 1) / factorial(2*k + 1)
        k += 1
    return sinx

def cos(x:float):
    cosx = sin(pi / 2 - x)
    return cosx

def tan(x:float):
    return sin(x)/cos(x)

def exp(x:float):
    return 2.718281828459045**x

def gamma(x):
    import math
    g = 7
    p = [
        0.99999999999980993,
        676.5203681218851, -1259.1392167224028,
        771.32342877765313, -176.61502916214059,
        12.507343278686905, -0.13857109526572012,
        9.9843695780195716e-6, 1.5056327351493116e-7
    ]
    
    if x < 0.5:
        return pi / (sin(pi * x) * gamma(1 - x))
    else:
        x -= 1
        a = p[0]
        for i in range(1, g + 2):
            a += p[i] / (x + i)
        t = x + g + 0.5
        return sqrt(2 * pi) * t ** (x + 0.5) * exp(-t) * a

def nCk(n:int, k:int):
    if k <= n:
        return factorial(n)/(factorial(k)*factorial(n-k))