import numpy as np
import scipy.stats as si

from payoffs import eur_opt_BS

def eur_opt_BS_vega(S, K, T, r, sigma, phi = 1):
    
    #Vega of European option
    
    #S: spot price
    #K: strike price
    #T: time to maturity
    #r: interest rate
    #sigma: volatility of underlying asset
    #phi: 1 is call, -1 is put
    
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    vega = S * np.sqrt(T) * si.norm.pdf(d1, 0.0, 1.0)
    
    return vega


def iv_eur_opt_BS1(P, S, K, T, r, phi = 1, threshold = 0.0001):
    
    #Given the price of an European Option this function 
    # calculates the corresponding volatility using bisection
    
    #P: spot price
    #S: spot price
    #K: strike price
    #T: time to maturity
    #r: interest rate
    #threshold: denotes when to stop the searching algorithm
    #phi: 1 is call, -1 is put
    
    
    vol_low = 0.0001
    vol_high = 1
    vol_m = (vol_low + vol_high) / 2
    price_diff = eur_opt_BS(S, K, T, r, sigma = vol_m, phi = phi) - P
    iterations = 0
    
    if np.sign(eur_opt_BS(S, K, T, r, sigma = vol_low, phi = phi) - P) == np.sign(eur_opt_BS(S, K, T, r, sigma = vol_high, phi = phi) - P):
        print("No zero point")
        return [vol_m, iterations]

    while np.abs(price_diff) > threshold:
        if iterations > 100:
            print("Iterations reached maximum limit")
            break
        if np.sign(price_diff) == np.sign(eur_opt_BS(S, K, T, r, sigma = vol_low, phi = phi) - P):
            vol_low = vol_m
        else:
            vol_high = vol_m
        
        vol_m = (vol_low + vol_high) / 2
        price_diff = eur_opt_BS(S, K, T, r, sigma = vol_m, phi = phi) - P
        iterations += 1
    
    return [vol_m, iterations]



def iv_eur_opt_BS2(P, S, K, T, r, phi = 1, threshold = 0.0001):
    
    #Given the price of an European Option this function 
    # calculates the corresponding volatility using Newton-Rhapson
    
    #P: market price of option
    #S: spot price
    #K: strike price
    #T: time to maturity
    #r: interest rate
    #threshold: denotes when to stop the searching algorithm
    #phi: 1 is call, -1 is put
    
    vol_new = 0.2
    iterations = 0

    while True:
        if iterations > 100:
            print("Iterations reached maximum limit")
            break
        price = eur_opt_BS(S, K, T, r, vol_new, phi)
        vega = eur_opt_BS_vega(S, K, T, r, vol_new, phi)
        vol_new -= (price - P) / vega
        iterations += 1
        if abs(price - P) < threshold:
            break
    
    return [vol_new, iterations]