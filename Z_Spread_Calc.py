import numpy as np
import time

start_time = time.time()
debug = False
par_val = 1000
cr = .12
time_to_maturity = 4
market_price = 975
tolerance = 1e-7

print('Bond params: par:' + str(par_val) + ' coupon:' + str(cr*100) + '% years:' + str(time_to_maturity) + ' mkt_px:' + str(market_price) + ' tolerance:' + str(tolerance))

cf = np.zeros(time_to_maturity)

for i in range(0,time_to_maturity):
    cf[i] = par_val*cr

cf[time_to_maturity-1] += par_val

#TSP Curve

#hardcoded tsp
tsp_curve = np.array([0.05, 0.06, 0.065, 0.07])

print('curve points:' , tsp_curve)

dcf = np.zeros(cf.size)
for i in range(0,time_to_maturity):
    dcf[i] = cf[i]/((1 + tsp_curve[i])**(i+1))

#print('dcf', dcf)

z_guess = 0.04
total_Val = np.sum(dcf)
counter=0

while(1>0):

    value_at_z = 0

    for i in range(0,time_to_maturity):
        value_at_z += cf[i] / ((1 + tsp_curve[i] + z_guess)**(i+1))

    #print('value_at_z', value_at_z)

    derivative = 0
    for j in range(0,time_to_maturity):
        derivative += ((j+1 * cf[j]) / ((1 + tsp_curve[j] + z_guess) ** (j + 2)))
        #print('sum partial', derivative)
        
    #print('derivative', derivative)

    value_at_z = market_price - value_at_z
    #print('after diff value_at_z', value_at_z)

    ratio = value_at_z / derivative
    #print('ratio', ratio)

    next_z = z_guess - ratio/100
    
    if debug:
        print('next Z', next_z)
        print('-'*40)
        
    if abs(next_z - z_guess) < tolerance:
        print('final z-spread:', next_z*100, '%')
        print('iterations:',counter)
        elapsed_time = time.time() - start_time
        print('elapsed time:',elapsed_time,' seconds')
        break
    
    z_guess = next_z
    counter += 1
########   
