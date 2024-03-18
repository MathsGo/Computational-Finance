# standard python packages
import numpy as np
import matplotlib.pyplot as plt
import os
import sys
import time
from timeit import default_timer as timer
import pandas as pd

# import own functions
# Spyder and VSCode not always consistent for os.getcwd(), so set cwd explicitly

os.chdir(os.path.dirname(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Code')))
from payoffs import eur_opt_BS, eur_opt_MC
from paths import paths


# use default_time from timeit to measure the calculation time
#https://stackoverflow.com/questions/7370801/how-to-measure-elapsed-time-in-python

spot, strike, vol, rate, expiry = 443, 443, 0.20, 0.06, 2

# num_paths_arr = [5000, 10000, 50000, 100000] #use this for testing.
num_paths_arr = [5000, 10000, 50000, 100000, 150000, 200000, 400000, 600000, 800000, 1000000]

#time_arr stores the elapsed time to calculate MC option value for given number of paths
value_MC_arr, se_MC_arr, time_arr = [], [], []


#calculate analytical option value
value_BS = eur_opt_BS(spot, strike, expiry, rate, vol, phi=1)
value_BS_arr = value_BS * np.ones(len(num_paths_arr))


#calculate monte carlo option value
np.random.seed(seed = 11)
for num_paths in num_paths_arr:
    start_time = timer()
    Spaths = paths(spot, vol, rate, expiry, num_paths)
    opt_PV, st_err_PV = eur_opt_MC(Spaths, strike, np.exp(-rate * expiry), phi=1)
    end_time = timer()
    value_MC_arr.append(opt_PV)
    se_MC_arr.append(st_err_PV)
    time_arr.append(end_time - start_time)

#plot figures 
fig, (ax1, ax3) = plt.subplots(2, 1)
#setting properties

ax1.plot(num_paths_arr, value_BS_arr, label='Analytical Price')
ax1.errorbar(num_paths_arr, value_MC_arr, yerr=se_MC_arr, fmt='o', label='MC Price')
ax1.set_xlabel('Number of Paths')
ax1.set_ylabel('Option Price')
ax1.set_title('Assignment 1.2 - values + SE')
ax1.legend(loc=(0.1, 0.57))

ax2 = ax1.twinx()
ax2.plot(num_paths_arr, se_MC_arr, 'r+-', label='MC Standard Error')
ax2.set_ylabel('Standard Error')
ax2.legend()

ax3.set_title('Assignment 1.2 - calculation time')
ax3.plot(num_paths_arr, time_arr, 'g^-')
ax3.set_xlabel('Number of Paths')
ax3.set_ylabel('Time (seconds)')

# Tweak spacing between subplots to prevent labels from overlapping
plt.subplots_adjust(hspace=0.7)

#save fig in output folder
output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..','Output' )) #ADO cannot handle r'..\Output'
time_str = time.strftime("%Y%m%d-%H%M%S")
plt.savefig(os.path.join(output_dir, f'Assignment 1.2 {time_str}.pdf'), format = 'pdf', dpi = 600)

#show plot
fig.tight_layout()
plt.show()


#Save data used in plots in one csv file in the output folder
# use same date time stamp in file name as for pdf document  
data_dict = {'Num Paths': num_paths_arr, 'value_BS': value_BS_arr, 'value_MC': value_MC_arr, 'se_MC': se_MC_arr}
df = pd.DataFrame(data_dict)
df = df.set_index('Num Paths') #now set the index of the datafram to one of its columns
df.to_csv(os.path.join(output_dir, f'Assignment 1.2 {time_str}.csv'))

