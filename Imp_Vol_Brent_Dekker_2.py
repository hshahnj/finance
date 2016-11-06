import numpy as np
import scipy
from scipy import integrate
from numpy import inf

#T = Maturity Date
#t = time in years
ref = 'C'
rate = 0.25
rate /= 100
strikePrice = 107
spotPrice = 108.84
x1 = -50
x2 = 50
eps = 1e-8
deltaTime = 0.079 #in years

bsmcounts = 0

call_price = 4.10
put_price = 0.00

print('inputs used are Call/Put is ',ref, 'rate is ', rate, '% strike Px is ', strikePrice, ' spotPx is ', spotPrice, ' time is ', deltaTime, ' call Px is ', call_price)

MAX_COUNT=100

def NormDist(value):
    int_Val = integrate.quad(lambda z: np.exp((-1*(z**2))/2), -inf, value)
    final = int_Val[0]
    return 1/np.sqrt(2*np.pi) * final

def bsm_call(vol):
    global bsmcounts 
    time_sqrt = np.sqrt(deltaTime)
    d1 = (1/(vol*time_sqrt)) * (np.log(spotPrice/strikePrice) + (rate + (vol**2)/2)*(deltaTime))
    d2 = d1 - (vol*time_sqrt)
    
    bsmcounts = bsmcounts + 1
    
    return NormDist(d1)*spotPrice - NormDist(d2)*strikePrice*np.exp(-1*rate*deltaTime)
    
    

def bsm_put(vol):
    #use put-call parity
    call_p = bsm_call(vol)
    return strikePrice*np.exp(-1*rate*deltaTime) - spotPrice + call_p

def test_func(x):
    y = ((x - 2) ** 3) - 1
    return y

def diff(x, ref):
    if (ref == 'C'):
        return bsm_call(x) - call_price
    elif (ref == 'P'):
        return bsm_put(x) - put_price

def func(x, ref):
    return diff(x, ref)

def ImpVol_BD(x1, x2, tol, ref):

    e = float(0); d = float(0)
    min1 = float(0); min2 = float(0)
    f_c = float(0)
    p = float(0); q = float(0); r = float(0); s = float(0)
    tol1 = float(0); xm = float(0)
    
    a = x1
    b = x2

    f_a = func(a, ref)
    f_b = func(b, ref)
    
    if f_a*f_b >= 0:
        print('Root not in the interval')
        return -400.0

    f_c = f_b

    iter = 1    
    while (iter < MAX_COUNT):
        if (f_b > 0 and f_c > 0) or (f_b < 0 and f_c < 0):
            c = a
            f_c = f_a
            e = b-a
            d = e
        
        if abs(f_c) < abs(f_b):
            a=b
            b=c
            c=a
            f_a=f_b
            f_b=f_c
            f_c=f_a
        #check convergence here    
        tol1=2.0*eps*abs(b)+0.5*tol
        xm=0.5*(c-b)
        if abs(xm) <= tol1 or f_b == 0.0:
            print ("iterations ", iter, "bsm calls ", bsmcounts)
            return b
        
        if abs(e) > tol1 and abs(f_a) > abs(f_b):
            s=f_b/f_a #do inv quadratic interpolation
            if a == c:
                p=2.0*xm*s
                q=1.0-s
            else:
                q=f_a/f_c
                r=f_b/f_c
                p=s*(2.0*xm*q*(q-r)-(b-a)*(r-1.0))
                q=(q-1.0)*(r-1.0)*(s-1.0)
            
            if p > 0.0: #check bounds
                q=-q
            
            p=abs(p)
            min1=3.0*xm*q-abs(tol1*q)
            min2=abs(e*q)
            if 2.0*p < np.minimum(min1,min2):
                e=d #interpolation OK
                d=p/q
            else:
                d=xm #interpolation won't work
                e=d
            
        else:
            d=xm #use bisection
            e=d
        
        a=b
        f_a=f_b
        if abs(d) > tol1:
            b += d
        else:
            b += abs(tol1) if xm > 0.0 else -abs(tol1)
        
        f_b = func(b, ref)
             
        iter+=1    
        
    print("max iteration count reached")
    return 0.0 #don't arrive here at all
bsmcounts=0
solution = ImpVol_BD(x1, x2, eps, ref)

#Convert to Percentage
solution *= 100
#pct_soln = "%.2f" % solution

print('Implied volatility % ',solution,'%')




