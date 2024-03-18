import numpy as np

def paths(spot, vol, rate, expiry, num_paths, seed = 1):
    '''This function simulates 'num_paths' paths of lognormal 
    distributed random stock variable'''
            
    np.random.seed(seed)# added to unit test mc paths and mc payoffs
    S = np.zeros(num_paths)
    z = np.random.standard_normal(num_paths)  # generate standard normal random number
    S = spot * np.exp((rate - 0.5 * vol ** 2) * expiry + vol * np.sqrt(expiry) * z)

    return S