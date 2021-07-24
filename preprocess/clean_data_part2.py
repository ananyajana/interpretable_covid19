from __future__ import print_function
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math
import os
from argparse import ArgumentParser
from scipy.stats import uniform, randint
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import SelectKBest
import warnings
warnings.filterwarnings("ignore")
import numpy as np
import scipy.stats
from utils import perf_measure, draw_auc, write_stats, find_mutual_info



parser = ArgumentParser()
parser.add_argument('--model', type=str, default="fea_selection", help='model name')
parser.add_argument('--max_nans', type=int, default=20, help='maximum number of allowed nan vals in a row')
parser.add_argument('--rem_max_nans', type=bool, default=True, help='remove the rows with > max_nans')
parser.add_argument('--var_thresh', type=float, default=0.1, help='threshols value for variance cutoff')
parser.add_argument('--do_var_thresh', type=bool, default=True, help='perform variance thresholding? True  or False')
parser.add_argument('--max_nans_in_col_ratio', type=float, default=0.2, help='maximum number of allowed nan vals in a column')
parser.add_argument('--drop_nan_cols', type=bool, default=True)
parser.add_argument('--target_outcome', type=str, default='SEVER')
args = parser.parse_args()

tgt_col = args.target_outcome
model_str = args.model

output_folder='out_' + model_str +'_' + tgt_col
if not os.path.exists(output_folder):
    os.mkdir(output_folder)
path = './'
file_name = 'COVID_V5.xlsx'
full_file_path = path + file_name


k = 0
all_data = pd.read_excel(full_file_path, sheet_name='Sheet1')
print('all_data len:', len(all_data.index))
print('all_data columns len:', len(all_data.columns))


f_name = output_folder + '/bin_column_stats_before_row_deletion.txt'
f = open(f_name, 'w+')
text = '---------------Check the binary created cols stat-------------- \n\n'
strings = ['prior_med', 'prior_co', 'symp', 'malig', 'co_inf', 'gicom', 'treat']
for str in strings:
    for i in range(len(all_data.columns)):
        if str in all_data.columns[i].lower():
            temp = all_data[all_data.columns[i]].to_numpy()
            nan_temp = np.isnan(temp)
            not_nan_temp = ~nan_temp
            temp2 = temp[not_nan_temp]
            arr = np.unique(temp2, return_counts = True)
            text += '{} has vals:{} counts{}\n'.format(all_data.columns[i], arr[0], arr[1])
f.write(text)
f.close()


sorted_fea = None

# result or target columns are those which have the strind died, icu or mech or sever in them
# we use this to get rid of the date columns as well
result_cols = []
for i in range(len(all_data.columns)):
    val = all_data.columns[i]
    if val.lower().find('date') != -1 or val.lower().find('id') != -1 or \
    val.lower().find('t_stay') != -1 or val.lower().find('treat') != -1 or \
    val.lower().find('_w') != -1 or val.lower().find('_d') != -1 or \
    val.lower().find('prior_med') != -1 or val.lower().find('method') != -1 :
        result_cols.append(val)

all_data.drop(columns = result_cols, inplace=True)
print('all_data len:', len(all_data.index))
print('all_data columns len:', len(all_data.columns))


# get rid of the features that have very less variance i.e. 80% of the columns contain the same value
from sklearn.feature_selection import VarianceThreshold
#Select Model
selector = VarianceThreshold(0.1) #Defaults to 0.0, e.g. only remove features with the same value in all samples
#Fit the Model
selector.fit(all_data)
all_data = all_data.loc[:, selector.get_support()]
print('all_data len:', len(all_data.index))
print('all_data columns len:', len(all_data.columns))

f_name = output_folder + '/bin_column_stats.txt'
f = open(f_name, 'w+')
text = '---------------Check the binary created cols stat-------------- \n\n'
strings = ['prior_med', 'prior_co', 'symp', 'malig', 'co_inf', 'gicom', 'treat']
for str in strings:
    for i in range(len(all_data.columns)):
        if str in all_data.columns[i].lower():
            temp = all_data[all_data.columns[i]].to_numpy()
            nan_temp = np.isnan(temp)
            not_nan_temp = ~nan_temp
            temp2 = temp[not_nan_temp]
            arr = np.unique(temp2, return_counts = True)
            text += '{} has vals:{} counts{}\n'.format(all_data.columns[i], arr[0], arr[1])
f.write(text)



ratio = args.max_nans_in_col_ratio
THRESH = len(all_data.index) * ratio  # if a column has greater than THRESH nan values, then that should be deleted

f_name = output_folder + '/col_nan_stats.txt'
f = open(f_name, 'w+')
text = ''
nan_idx = []
nan_cols = []
for i in range(len(all_data.columns)):
    cnt = all_data[all_data.columns[i]].isna().sum()
    if cnt != 0:
        if cnt > THRESH:
            nan_cols.append(all_data.columns[i])
            text += '{} '.format(all_data.columns[i])
            text += f'(column {i}) has {cnt} > {THRESH} nan value\n'


text += f'nan_idx :{set(nan_idx)}\n'
text += f'nan_cols: {nan_cols}\n'
f.write(text)
f.close()


if args.drop_nan_cols is True:
    all_data.drop(columns = nan_cols, inplace=True)

writer = pd.ExcelWriter('COVID_V6.xlsx')
all_data.to_excel(writer, sheet_name='Sheet1', index=False)
writer.save()

