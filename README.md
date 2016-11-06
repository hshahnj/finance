# finance
finding z-spread and implied volatility

Imp_Vol_Brent_Dekker_2.py:

Uses Brent-Dekker root finding method to minimize the difference between the option price derived from Black-Scholes model and the market price in order to find volatility. This is known as implied volatility. 

Z_Spread_Calc.py:

Uses Newton-Raphson's method to find an optimal Z-Spread value at which the bond value equals the market price of the bond. Hard-coded test example in the python file. 

ZSpread.xlsx:

Excel file which displays iterations using Newton-Rhapson's Method to find the optimal Z-Spread value given certain criteria of an example bond. Displays 100 iterations of Newton-Raphson's Method.

ImpVol.xlsx:

Excel file which sets up a scenario to use Goal-Seek in order to find the implied volatility based on the call-price (and other required parameters) of the option. Uses Black-Scholes to calculate option price if volatility (and other required parameters) are provided.
