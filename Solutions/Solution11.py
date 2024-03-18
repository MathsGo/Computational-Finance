#standard python packages
import numpy as np
import matplotlib.pyplot as plt
import os
import sys
import time

# import own functions
# Spyder and VSCode not always consistent for os.getcwd(), so set cwd explicity

os.chdir(os.path.dirname(__file__)) 
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..','Code' )))

from paths import paths
from distribution import lognorm_pdf

spot, vol, rate, expiry = 443, 0.20, 0.06, 2


fwd = spot * np.exp(rate * expiry)
mu = np.log(fwd) - 1/2 * vol**2

#analytical lognormal PDF
x = np.linspace(0.00001, round(5* fwd), round(5* fwd))
pdf  = lognorm_pdf(x, mu, vol * np.sqrt(expiry))


num_paths_arr = [2000, 20000]
fig, ax  = plt.subplots(len(num_paths_arr),1)

ax[0].set_title('Lognormal Distribution')

for i, num_paths in enumerate(num_paths_arr):
    # Generate Monte Carlo paths
    underlying_values = paths(spot, vol, rate, expiry, num_paths)
    
    # Plot empirical distribution
    ax[i].hist(underlying_values, bins=50, density=True, alpha=0.5, label=f'{num_paths} paths')
    ax[i].plot(x, pdf, color='r', label='Analytical PDF')
    ax[i].set_xlabel('Underlying Value')
    ax[i].set_ylabel('Probability Density')
    ax[i].legend()

#save fig in output folder
output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..','Output' )) #ADO cannot handle r'..\Output'
time_str = time.strftime("%Y%m%d-%H%M%S")
plt.savefig(os.path.join(output_dir, f'Assignment 1.1 {time_str}.pdf'), format = 'pdf', dpi = 600)
#plt.savefig(os.path.join(r'..\Output', f'Assignment 1.1 {time_str}.pdf'), format = 'pdf', dpi = 600)

# the amount of height reserved for space between subplots,
# expressed as a fraction of the average axis height
plt.subplots_adjust(hspace=0.5)

#fig.tight_layout()
plt.show()

