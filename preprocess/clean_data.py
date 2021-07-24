from __future__ import print_function
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math
import numpy as np
import scipy.stats




path = '../expt1/'
file_name = 'COVID_V4.xlsx'
full_file_path = path + file_name

num = 6
tgt_col = 'SEVER'
#from preprocess import clean_data
# handle SPO column
import re
k = 0
all_data = pd.read_excel(full_file_path, sheet_name='Sheet1')
print('all_data len:', len(all_data.index))
print('all_data columns len:', len(all_data.columns))
all_data.drop_duplicates(subset=['PAT_ID'], inplace=True, keep='last')
all_data.reset_index(drop=True, inplace=True)
print('after duplicate removal all_data len:', len(all_data.index))
print('after duplicate removal all_data columns len:', len(all_data.columns))
for i in range(len(all_data.columns)):
    if 'SPO' in all_data.columns[i]:
        k = i

aa = all_data[all_data.columns[k]].unique().tolist()
col_copy  = all_data[all_data.columns[k]].copy()
print('cleaning SPO column')
for i, val in all_data[all_data.columns[k]].iteritems():
    if np.isreal(val) is True:
        if val < 1:
            val = val * (100.0)
            all_data.iloc[i, k] = val
    else:
        if val.find('%') != -1 or val.find(' ') != -1 or val.find('s') != -1:
            num_val = re.split('%|\ |s', val)
            all_data.iloc[i, k] = float(num_val[0])    

all_data['SPO'] = all_data['SPO'].astype(float)

# create a column for ICU from the ICU stay length column
nan_col = [np.nan for k in range(len(all_data.index))] 

for i in range(len(all_data.columns)):
    if 'icu' in all_data.columns[i].lower():
        k = i


# creating a column whether a patient needed ICU or not
# depending on the column icu_length . If it is 0, that
# means(?) the patient did not need ICU
icu_cnt = 0
no_icu_cnt = 0
for idx, val in all_data[all_data.columns[k]].iteritems():
    if math.isnan(val) is False:
        if val == 0:
            nan_col[idx] = 0
            no_icu_cnt += 1
        elif np.isreal(val) is True:
            nan_col[idx] = 1
            icu_cnt += 1
            
print(f'{icu_cnt} needed ICU, {no_icu_cnt} patients did not need ICU')
all_data['ICU'] = nan_col

# create a SEVER column from DIED, ICU and Mech, this can be treated as the
# combined outcome sverity column
nan_col2 = [np.nan for k in range(len(all_data.index))]
for idx, val in all_data['DIED'].iteritems():
    val1 = all_data['ICU'][idx]
    val2 = all_data['Mech'][idx]
    if val == 1 or val1 == 1 or val2 == 1:
        nan_col2[idx] = 1
    elif (math.isnan(val) is False ) and (math.isnan(val1) is False) and (math.isnan(val2) is False):
        nan_col2[idx] = 0
    else:
        print(f'index:{idx} DIED: {val}, ICU: {val1}, Mech: {val2}')
all_data['SEVER'] = nan_col2


# also create an an array of row indices where this SEVER value is not defined
target_cols = []
for idx, val in all_data[tgt_col].iteritems():
    if math.isnan(val):
        target_cols.append(idx)
#print(target_cols)
all_data.drop(all_data.index[target_cols], inplace=True)
all_data.reset_index(drop=True, inplace=True)
print('chkpt: 18')
print('len all_data:', len(all_data.index))
print('columns len all_data:', len(all_data.columns))
print('columns  all_data:{}\n\n'.format(all_data.columns))
# check if the target rows have been deleted properly
target_cols = []
for idx, val in all_data[tgt_col].iteritems():
    if math.isnan(val):
        target_cols.append(idx)
#print(target_cols)

# result or target columns are those which have the strind died, icu or mech or sever in them
# we use this to get rid of the date columns as well
print('chkpt: 17')
print('len all_data:', len(all_data.index))
print('columns len all_data:', len(all_data.columns))
print('columns  all_data:{}\n\n'.format(all_data.columns))
# at this point 9 columns from the original table have been deleted and 1 row has been 
# deleted as SEVER was not defined
#print(all_data.columns)
#print(all_data.index)

# thcolumns Neutro, AST_F and ProBNP need preprocessing
# to convert them from obj to float, they contain one instance
# of a non real number value
CONST = 0.005
obj_cols_req_prep = ['Neutro', 'ProBNP', 'AST_F']
for i in obj_cols_req_prep:
    for k, val in all_data[i].iteritems():
        if np.isreal(val) is False:
            if not val.strip():
                idx = all_data.columns.get_loc(i)
                all_data.iloc[k, idx] = np.nan
            if val.find('<') != -1 or val.find('>') != -1:
                num_val = re.split('<|>', val)
                if num_val[1].isnumeric() is True:
                    if val.find('>') != -1:
                        num_val[1] = float(num_val[1]) + CONST
                        idx = all_data.columns.get_loc(i)
                        all_data.iloc[k, idx] = float(num_val[1])
    all_data[i] = all_data[i].astype(np.float64)

# Get rid of columns that have too many nan values


# get rid of some other columns which are of the type of object
# most of these columns have been added as binary columns
# if we want to add those columns back and preprocess them as numbers
# we can do that later: TBD
# we also normalize the real number columns here
obj_cols = []
# except_cols contains catgorical variables which have more than 3 categories or classes or values
except_cols = ['Stool', 'Race', 'Smoke', 'Method', 'Alco']
for i in range(len(all_data.dtypes)):
    t = all_data.dtypes[i]
    if t != np.int64 and t != np.float64:
        obj_cols.append(all_data.columns[i])
all_data.drop(columns = obj_cols, inplace=True)
print('chkpt: 16')
print('len all_data:', len(all_data.index))
print('columns len all_data:', len(all_data.columns))
print('columns  all_data:{}\n\n'.format(all_data.columns))
# at this point object columns have been deleted.



# check that every columns name is assigned a flag

# all data CPK contains all nan values and hence need to be deleted


# let's check the mutual info between individual feature columns from all_data
# and the all_data_new['SEVER'] column

# create a CT_C column for abnormal CT scan
nan_col_ct = [np.nan for k in range(len(all_data.index))]
for idx, val in all_data['CHEST7'].iteritems():
    val1 = all_data['CHEST1'][idx]
    val2 = all_data['CHEST2'][idx]
    val3 = all_data['CHEST3'][idx]
    val4 = all_data['CHEST4'][idx]
    val5 = all_data['CHEST5'][idx]
    val6 = all_data['CHEST6'][idx]
    if val == 1:    # if CHEST7 value is 1, that means the CT scan abnormality = 0
        nan_col_ct[idx] = 0
    elif val1 == 1 or val2 == 1 or val3 == 1 or val4 == 1 or val5 == 1 or val6 == 1: # if any of CHEST1 to CHEST6 is 1, that means CT scan abnormality = 1
        nan_col_ct[idx] = 1
all_data['CT_C'] = nan_col_ct


# we cannot do similar stuff for the Chest XRay because there are neought no. of samples
# of each class
# but CT has just 4 normal samples, 79 abnormal samples and for others CT data is not taken or not known

# we can drop the original Chest columns here
#chest_cols = [f'CHEST{i}' for i in range(1, 8)]
chest_cols = []
for i in range(len(all_data.columns)):
    if 'chest' in all_data.columns[i].lower():
        chest_cols.append(all_data.columns[i])

all_data.drop(columns = chest_cols, inplace=True)

# create a RACE_E column for Race and Ethnicity combined
# 1. White non-hispanic 2. Black non-hispanic, 3 hispanic 4. Other
nan_col_race_e = [np.nan for k in range(len(all_data.index))]
for idx, val in all_data['Latin'].iteritems():
    val1 = all_data['Race'][idx]
    if val == 1:    # if Latin value is 1, that means hispanic option(3)
        nan_col_race_e[idx] = 3 
    elif val1 == 1 or val1 == 2:
        nan_col_race_e[idx] = val1
    elif val1 == 4 or val1 == 5 or val1 == 6:
        nan_col_race_e[idx] = 4
all_data['RACE_E'] = nan_col_race_e

# drop Race and Latin columns
all_data.drop(columns = ['Race', 'Latin'], inplace=True)

writer = pd.ExcelWriter('COVID_V5.xlsx')
all_data.to_excel(writer, sheet_name='Sheet1', index=False)
writer.save()

