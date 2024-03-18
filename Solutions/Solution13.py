#standard python packages
import matplotlib.pyplot as plt
import os
import sys
import time
import pandas as pd

# import own functions
# Spyder and VSCode not always consistent for os.getcwd(), so set cwd explicity

os.chdir(os.path.dirname(__file__)) 
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..','Code' )))
from bsfunctions import iv_eur_opt_BS1, iv_eur_opt_BS2

input_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..','Input' )) #ADO cannot handle r'..\Input'
df = pd.read_csv(os.path.join(input_dir, 'OptionPrices.csv'))

# Save data used in plots in one csv file in the output folder.
# Use same date time stamp in file name as for pdf document
vol_imp_arr, num_iter_arr = [], []
vol_imp_arr2, num_iter_arr2 = [], []

for idx, row in df.iterrows():
    strike = row['strikes']
    S = row['spots']
    K = row['strikes']
    T = row['expiries']
    r = row['rates']
    P = row['prices']
    phi = row['CP']

    vol_imp1, iter1 = iv_eur_opt_BS1(P, S, K, T, r, phi)
    vol_imp2, iter2 = iv_eur_opt_BS2(P, S, K, T, r, phi)

    vol_imp_arr.append(vol_imp1)
    num_iter_arr.append(iter1)
    vol_imp_arr2.append(vol_imp2)
    num_iter_arr2.append(iter2)

# plot figures    
fig, (ax1, ax3) = plt.subplots(2, 1)

ax1.plot(df['strikes'], vol_imp_arr, 'r*', label='IV-BS Bisection')
ax1.plot(df['strikes'], vol_imp_arr2,'g.', label='IV-BS Newton-Rhapson')
ax1.set_xlabel('strikes')
ax1.set_ylabel('Volatilities')

# setting properties
ax1.set_title('Assignment 1.3 - Implied Volatility (IV)')
ax1.legend(loc='upper left', framealpha=0.1)

ax2 = ax1.twinx()
ax2.plot(df['strikes'], df['prices'], 'x-', label='Prices')
ax2.set_ylabel('prices')
ax2.legend()


ax3.plot(df['strikes'], num_iter_arr, '.-', label='Iterations - BS Bisection')
ax3.plot(df['strikes'], num_iter_arr2, '*-', label='Iterations - BS Newton-Rhapson')
ax3.set_xlabel('Strikes')
ax3.set_ylabel('Number of Iterations')

ax3.set_title('Assignment 1.3 - Number of iterations (NI) ')
ax3.legend()

# Tweak spacing between subplots to prevent labels from overlapping
plt.subplots_adjust(hspace=0.5)

#save fig in output folder
output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..','Output' )) #ADO cannot handle r'..\Output'
time_str = time.strftime("%Y%m%d-%H%M%S")
plt.savefig(os.path.join(output_dir, f'Assignment 1.3 {time_str}.pdf'), format = 'pdf', dpi = 600)

# show plot
fig.tight_layout()
plt.show()

# Save data used in plots in one csv file in the output folder
# use same date time stamp in file name as for pdf document  
data_dict = {'Strikes': df.strikes, 'Prices': df.prices, 'IV-BS': vol_imp_arr , 'NI-BS': num_iter_arr,'IV-NR': vol_imp_arr2 , 'NI-NR': num_iter_arr2 }
df = pd.DataFrame(data_dict)
df = df.set_index('Strikes') #now set the index of the datafram to one of its columns
df.to_csv(os.path.join(output_dir, f'Assignment 1.3 {time_str}.csv'))
plt.show()
