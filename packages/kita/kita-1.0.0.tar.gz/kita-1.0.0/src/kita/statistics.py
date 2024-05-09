from .basic import *

def binomial_distribution(n:int,p:float,k:int,condition="="):
    if condition == "=":
        return nCk(n,k)*p**(k) * (1-p)**(n-k)
    elif condition == "<=":
        probability = 0
        for i in range(0, k+1):
            probability += nCk(n,i)*p**(i) * (1-p)**(n-i)
        return probability
    elif condition == "<":
        probability = 0
        for i in range(0, k):
            probability += nCk(n,i)*p**(i) * (1-p)**(n-i)
        return probability
    elif condition == ">":
        probability = 0
        for i in range(0, k+1):
            probability += nCk(n,i)*p**(i) * (1-p)**(n-i)
        return 1-probability
    elif condition == ">=":
        probability = 0
        for i in range(0, k):
            probability += nCk(n,i)*p**(i) * (1-p)**(n-i)
        return 1-probability
    
    
    