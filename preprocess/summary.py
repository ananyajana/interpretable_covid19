import pandas as pd
import numpy as np
import math
import os
#input_file_name = 'output.xlsx'
output_folder='out'
if not os.path.exists(output_folder):
    os.mkdir(output_folder)
path='./'
file_name = 'COVID_V4.xlsx'
full_file_path = path + file_name

all_data = pd.read_excel(full_file_path, sheet_name='Sheet1')
num = 6

# handle SPO column
import re
k = 0
all_data = pd.read_excel(full_file_path, sheet_name='Sheet1')
for i in range(len(all_data.columns)):
    if 'SPO' in all_data.columns[i]:
        print(i)
        k = i

aa = all_data[all_data.columns[k]].unique().tolist()
#print('before :', aa)
col_copy  = all_data[all_data.columns[k]].copy()
print('cleaning SPO column')
for i, val in all_data[all_data.columns[k]].iteritems():
    #print(f"Index : {i}, Value : {val}")
    if np.isreal(val) is True:
        #print(f"real number: Index : {i}, Value : {val}")
        if val < 1:
            #print('{} is < 1'.format(val))
            val = val * (100.0)
            all_data.iloc[i, k] = val
    else:
        #print(f"Not a real number:Index : {i}, Value : {val}")
        if val.find('%') != -1 or val.find(' ') != -1 or val.find('s') != -1:
            num_val = re.split('%|\ |s', val)
            #print('num_val[0]: ', num_val[0])
            #print('float(num_val[0]): ', float(num_val[0]))
            all_data.iloc[i, k] = float(num_val[0])    

all_data['SPO'] = all_data['SPO'].astype(float)

# create a column for ICU from the ICU stay length column
nan_col = [np.nan for k in range(len(all_data.index))] 

for i in range(len(all_data.columns)):
    if 'icu' in all_data.columns[i].lower():
        print(all_data.columns[i])
        k = i
    print('the column index with icu string', k)

icu_cnt = 0
no_icu_cnt = 0
for idx, val in all_data[all_data.columns[k]].iteritems():
    if math.isnan(val) is False:
        if val == 0:
            print(f'found {val}, setting nan_col to 0')
            nan_col[idx] = 0
            no_icu_cnt += 1
        elif np.isreal(val) is True:
            print(f'found {val} nan_col->1')
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
    #print(f' DIED: {val}, ICU: {val1}, Mech: {val2})')
    if val == 1 or val1 == 1 or val2 == 1:
        nan_col2[idx] = 1
    elif (math.isnan(val) is False ) and (math.isnan(val1) is False) and (math.isnan(val2) is False):
        nan_col2[idx] = 0
all_data['SEVER'] = nan_col2

# the following does not work because for the non str numbers it returns nan
# ab = df[df.columns[25]].str.split('% ', n=-1, expand=True)
#all_data = pd.read_excel(input_file_name, sheet_name='cleaned_data')
feature = all_data.columns[num]
#summary_filename = output_folder + '/' + input_file_name[:-4] + feature + '_Summary_statistics.txt'
summary_filename = output_folder + '/' + 'column {}'.format(num) + feature + '_Summary_statistics.txt'
print(len(all_data.columns))
def print_draw_summary(summary_filename, feature, fea_str=None):
    f = open(summary_filename, 'w+')
    text = '\n\n######### ' + feature + ' #############\n\n'
    text = text + '------------ overall ---------------\n'
    text = text + '#Mean : ' + '{:0.2f}'.format(all_data[feature].mean())
    text = text + ' #Standard Deviation : ' + '{:0.2f}'.format(all_data[feature].std())
    text = text + ' #Median : ' + '{:0.2f}'.format(all_data[feature].median())
    text = text + ' #Min : ' + '{:0.2f}'.format(all_data[feature].min())
    text = text + ' #Max : ' + '{:0.2f}'.format(all_data[feature].max())
    text = text + ' #Mean : ' + '{:0.2f}'.format(all_data[feature].std())
    text = text + '\n\n'


    # statistics based on outcome Death
    death_data = all_data[all_data['DIED'] == 1]
    text = text + '------------- death --------------\n'
    text = text + '#Mean : ' + '{:0.2f}'.format(death_data[feature].mean())
    text = text + ' #Standard Deviation : ' + '{:0.2f}'.format(death_data[feature].std())
    text = text + ' #Median : ' + '{:0.2f}'.format(death_data[feature].median())
    text = text + ' #Min : ' + '{:0.2f}'.format(death_data[feature].min())
    text = text + ' #Max : ' + '{:0.2f}'.format(death_data[feature].max())
    text = text + ' #Mean : ' + '{:0.2f}'.format(death_data[feature].std())
    text = text + '\n\n'

    survive_data = all_data[all_data['DIED'] == 0]
    text = text + '------------- survival --------------\n'
    text = text + '#Mean : ' + '{:0.2f}'.format(survive_data[feature].mean())
    text = text + ' #Standard Deviation : ' + '{:0.2f}'.format(survive_data[feature].std())
    text = text + ' #Median : ' + '{:0.2f}'.format(survive_data[feature].median())
    text = text + ' #Min : ' + '{:0.2f}'.format(survive_data[feature].min())
    text = text + ' #Max : ' + '{:0.2f}'.format(survive_data[feature].max())
    text = text + ' #Mean : ' + '{:0.2f}'.format(survive_data[feature].std())
    text = text + '\n\n'
    

    # statistics based on icu requirements
    icu_data = all_data[all_data['ICU'] == 1]
    text = text + '------------- ICU was needed--------------\n'
    text = text + '#Mean : ' + '{:0.2f}'.format(icu_data[feature].mean())
    text = text + ' #Standard Deviation : ' + '{:0.2f}'.format(icu_data[feature].std())
    text = text + ' #Median : ' + '{:0.2f}'.format(icu_data[feature].median())
    text = text + ' #Min : ' + '{:0.2f}'.format(icu_data[feature].min())
    text = text + ' #Max : ' + '{:0.2f}'.format(icu_data[feature].max())
    text = text + ' #Mean : ' + '{:0.2f}'.format(icu_data[feature].std())
    text = text + '\n\n'

    no_icu_data = all_data[all_data['ICU'] == 0]
    text = text + '------------- ICU was not needed--------------\n'
    text = text + '#Mean : ' + '{:0.2f}'.format(no_icu_data[feature].mean())
    text = text + ' #Standard Deviation : ' + '{:0.2f}'.format(no_icu_data[feature].std())
    text = text + ' #Median : ' + '{:0.2f}'.format(no_icu_data[feature].median())
    text = text + ' #Min : ' + '{:0.2f}'.format(no_icu_data[feature].min())
    text = text + ' #Max : ' + '{:0.2f}'.format(no_icu_data[feature].max())
    text = text + ' #Mean : ' + '{:0.2f}'.format(no_icu_data[feature].std())
    text = text + '\n\n'


    # statistics based on mechanical ventialltion requirement
    mech_data = all_data[all_data['Mech'] == 1]
    text = text + '------------- Mechanical Ventialation was needed--------------\n'
    text = text + '#Mean : ' + '{:0.2f}'.format(mech_data[feature].mean())
    text = text + ' #Standard Deviation : ' + '{:0.2f}'.format(mech_data[feature].std())
    text = text + ' #Median : ' + '{:0.2f}'.format(mech_data[feature].median())
    text = text + ' #Min : ' + '{:0.2f}'.format(mech_data[feature].min())
    text = text + ' #Max : ' + '{:0.2f}'.format(mech_data[feature].max())
    text = text + ' #Mean : ' + '{:0.2f}'.format(mech_data[feature].std())
    text = text + '\n\n'

    no_mech_data = all_data[all_data['Mech'] == 0]
    text = text + '------------- Mechanical Ventilation was not needed--------------\n'
    text = text + '#Mean : ' + '{:0.2f}'.format(no_mech_data[feature].mean())
    text = text + ' #Standard Deviation : ' + '{:0.2f}'.format(no_mech_data[feature].std())
    text = text + ' #Median : ' + '{:0.2f}'.format(no_mech_data[feature].median())
    text = text + ' #Min : ' + '{:0.2f}'.format(no_mech_data[feature].min())
    text = text + ' #Max : ' + '{:0.2f}'.format(no_mech_data[feature].max())
    text = text + ' #Mean : ' + '{:0.2f}'.format(no_mech_data[feature].std())
    text = text + '\n\n'
    f.write(text)
    f.close()

#print_draw_summary(summary_filename, feature)
def print_draw_summary_binary(summary_filename, feature, fea_str=None):
    f = open(summary_filename, 'w+')
    text = '\n\n######### ' + feature + ' #############\n\n'
    text = text + '------------ overall ---------------\n'
    uniq_vals = np.sort(all_data[feature].unique().tolist())
    for i in range(len(uniq_vals)):
        if math.isnan(uniq_vals[i]) is False:
            text = text + '# {0}s : '.format(int(uniq_vals[i])) + '{0} '.format(len(all_data[all_data[feature] == uniq_vals[i]]))
    text = text + '\n\n'

    # statistics based on outcome Death
    death_data = all_data[all_data['DIED'] == 1]
    text = text + '------------- death --------------\n'
    uniq_vals = np.sort(death_data[feature].unique().tolist())
    for i in range(len(uniq_vals)):
        if math.isnan(uniq_vals[i]) is False:
            text = text + '# {0}s : '.format(int(uniq_vals[i])) + '{0} '.format(len(death_data[death_data[feature] == uniq_vals[i]]))
    text = text + '\n\n'

    survive_data = all_data[all_data['DIED'] == 0]
    text = text + '------------- survival --------------\n'
    uniq_vals = np.sort(survive_data[feature].unique().tolist())
    for i in range(len(uniq_vals)):
        if math.isnan(uniq_vals[i]) is False:
            text = text + '# {0}s : '.format(int(uniq_vals[i])) + '{0} '.format(len(survive_data[survive_data[feature] == uniq_vals[i]]))
    text = text + '\n\n'


    # statistics based on icu requirements
    icu_data = all_data[all_data['ICU'] == 1]
    text = text + '------------- ICU was needed --------------\n'
    uniq_vals = np.sort(icu_data[feature].unique().tolist())
    for i in range(len(uniq_vals)):
        if math.isnan(uniq_vals[i]) is False:
            text = text + '# {0}s : '.format(int(uniq_vals[i])) + '{0} '.format(len(icu_data[icu_data[feature] == uniq_vals[i]]))
    text = text + '\n\n'

    no_icu_data = all_data[all_data['ICU'] == 0]
    text = text + '------------- ICU was not needed --------------\n'
    uniq_vals = np.sort(no_icu_data[feature].unique().tolist())
    for i in range(len(uniq_vals)):
        if math.isnan(uniq_vals[i]) is False:
            text = text + '# {0}s : '.format(int(uniq_vals[i])) + '{0} '.format(len(no_icu_data[no_icu_data[feature] == uniq_vals[i]]))
    text = text + '\n\n'

    # statistics based on mechanical ventialltion requirement
    mech_data = all_data[all_data['Mech'] == 1]
    text = text + '------------- Mechanical Ventilation was needed --------------\n'
    uniq_vals = np.sort(mech_data[feature].unique().tolist())
    for i in range(len(uniq_vals)):
        if math.isnan(uniq_vals[i]) is False:
            text = text + '# {0}s : '.format(int(uniq_vals[i])) + '{0} '.format(len(mech_data[mech_data[feature] == uniq_vals[i]]))
    text = text + '\n\n'

    no_mech_data = all_data[all_data['Mech'] == 0]
    text = text + '------------- Mechanical Ventilation was not needed --------------\n'
    uniq_vals = np.sort(no_mech_data[feature].unique().tolist())
    for i in range(len(uniq_vals)):
        if math.isnan(uniq_vals[i]) is False:
            text = text + '# {0}s : '.format(int(uniq_vals[i])) + '{0} '.format(len(no_mech_data[no_mech_data[feature] == uniq_vals[i]]))
    text = text + '\n\n'

    f.write(text)
    f.close()

all_data.dtypes
# RE_ADM type is object, but do not need to processs it as multi flag gives the info
# these are categorical variables
except_cols = ['Stool', 'Race', 'Smoke', 'Method', 'Alco']
for i in range(len(all_data.dtypes)):
    t = all_data.dtypes[i]
    if t != np.int64 and t != np.float64:
        print('col {} is not a number: {}'.format(i, t))
    else:
        feature = all_data.columns[i]
        summary_filename = output_folder + '/' + feature + '_Summary_statistics.txt'
        if len(all_data[all_data.columns[i]].unique()) > 3 and all_data.columns[i] not in except_cols:
            print_draw_summary(summary_filename, feature)
        else:
            print_draw_summary_binary(summary_filename, feature)

import matplotlib.pyplot as plt
#plt.matshow(all_data.corr())
#plt.show()
'''
f = plt.figure(figsize=(19, 15))
plt.matshow(all_data.corr(), fignum=f.number)
plt.xticks(range(all_data.shape[1]), all_data.columns, font_size=14, rotation=45)
plt.yticks(range(all_data.shape[1]), all_data.columns, font_size=14)
cb = plt.colorbar()
cb.ax.tick_params(labelsize=14)
plt.title('Correlation Matrix', fontsize=16)
'''

#pd.plotting.scatter_matrix(all_data, alpha = 0.3, figsize = (14, 8), diagonal = 'kde')
'''
corrMatrix = all_data.corr()
import seaborn as sn
sn.heatmap(corrMatrix, annot=True)
plt.show()
'''
