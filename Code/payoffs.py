import scipy.stats as si
import numpy as np


def eur_opt_MC(paths, K, DF, phi = 1):
    
    #Value of  European option
     
    #paths size should be (num_paths)
    #K: strike price
    #phi: 1 is call, -1 is put
    #DF: discount factor, required to calculate PV. The deterministic DF shnould equal to np.exp(-rate*expiry)
    if phi == 1:
        opt_PV = np.mean(np.maximum(phi * (paths - K), 0)) * DF
        st_err_PV = np.std(np.maximum(phi * (paths - K), 0)) / np.sqrt(len(paths))
    elif phi == -1:
        opt_PV = np.mean(np.maximum(phi * (K - paths), 0)) * DF
        st_err_PV = np.std(np.maximum(phi * (K - paths), 0)) / np.sqrt(len(paths))
    
    return [opt_PV, st_err_PV]



def eur_opt_BS(S, K, T, r, sigma, phi = 1):
    
    #Value of  European option
    
    #S: spot price
    #K: strike price
    #T: time to maturity
    #r: interest rate
    #sigma: volatility of underlying asset
    #phi: 1 is call, -1 is put
    
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    if phi == 1:
        eur_opt = S * si.norm.cdf(d1, 0.0, 1.0) - K * np.exp(-r * T) * si.norm.cdf(d2, 0.0, 1.0)
    elif phi == -1:
        eur_opt = K * np.exp(-r * T) * si.norm.cdf(-d2, 0.0, 1.0) - S * si.norm.cdf(-d1, 0.0, 1.0)
    
    
    return eur_opt


