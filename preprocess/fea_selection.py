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



parser = ArgumentParser()
parser.add_argument('--model', type=str, default="fea_selection", help='model name')
parser.add_argument('--topk', type=int, default=23, help='feature count in chi2, anova and mutual_info set')
parser.add_argument('--target_outcome', type=str, default='SEVER')
args = parser.parse_args()

tgt_col = args.target_outcome
model_str = args.model

output_folder='out_' + model_str +'_' + tgt_col
if not os.path.exists(output_folder):
    os.mkdir(output_folder)
path = './'
file_name = 'COVID_V6.xlsx'
full_file_path = path + file_name

all_data = pd.read_excel(full_file_path, sheet_name='Sheet1')
print('all_data len:', len(all_data.index))
print('all_data columns len:', len(all_data.columns))



col_type_dict = {'Age':True, 'SEX':True, 'BMI':False, 'Prior_Co1':True, 'Prior_Co2':True, 'Prior_Co3':True, 'Prior_Co6':True,
       'Prior_Co24':True, 'Alco':True, 'Smoke':True, 'SYMP1':True, 'SYMP2':True, 'SYMP3':True, 'SYMP5':True,
       'SYMP6':True, 'SYMP11':True, 'SYMP12':True, 'SYMP20':True, 'SPO':False, 'WBC':False, 'Hgb':False,
       'Hct':False, 'MCV':False, 'Plate':False, 'Neutro':False, 'Lymp':False, 'DIMER':True, 'Glucose':True, 'BUN':True,
       'CR':False, 'GFR_BIN':True, 'AKI':True, 'NA_I':True, 'K_I':False, 'BIC':False, 'ALB_I':False, 'TBILI':False, 'ALK_I':True,
       'ALT_I':True, 'AST_I':True, 'Trop_BIN':True, 'CRP':False, 'CXR2':True, 'CXR6':True, 'CXR7':True, 'EKG':True,
       'SEVER':True, 'RACE_E':True}

# Creating the time and event columns
died_col = 'DIED'
icu_col = 'ICU'
sever_col = 'SEVER'
mech_col = 'Mech'
leng_col = 'LENG'
leng_icu_col = 'LENG_ICU'
result_cols = [died_col, icu_col, sever_col, mech_col, leng_col, leng_icu_col]

# Extracting the features which are non outcome columns
features = np.setdiff1d(all_data.columns,  result_cols).tolist()


from sklearn.feature_selection import mutual_info_classif
info = {}
for col_name in features:
    fea_np = all_data[col_name].to_numpy()
    tgt_np = all_data[tgt_col].to_numpy()
    nan_idx = np.argwhere(np.isnan(fea_np))
    fea_np = np.delete(fea_np, nan_idx, axis=0)
    tgt_np = np.delete(tgt_np, nan_idx, axis=0)
    a = mutual_info_classif(fea_np.reshape(-1, 1), tgt_np, discrete_features=col_type_dict[col_name], random_state=11)
    info[col_name] = (a, len(fea_np))

sorted_fea = {k: v for k, v in reversed(sorted(info.items(), key=lambda item: item[1]))}

f_name = output_folder + f'/mutual_info_before_normalization.txt'
f = open(f_name, 'w+')
text = '----------------Mutual Info--------------\n'

for m in sorted_fea:
    text += '{}{}\n'.format(m, sorted_fea[m])
arr = []
i = 0

text += 'top {} features'.format(args.topk)
for m in sorted_fea:
    arr.append(m)
    i += 1
    text += '{}\n'.format(m)
    if i == args.topk:
        break
f.write(text)
f.close()

arr += result_cols
all_data = all_data[arr]

# check from the correlation plot which features have very high correlation and get rid of them
# I removed the features where correlation is > 0.9 or correlation > -1
high_corr_cols = ['ALT_I', 'Hgb', 'SPO']
features = np.setdiff1d(all_data.columns,  high_corr_cols).tolist()
all_data = all_data[features]

writer = pd.ExcelWriter('COVID_V7.xlsx')
all_data.to_excel(writer, sheet_name='Sheet1', index=False)
writer.save()

all_data_copy = all_data.copy()

result_cols.remove(tgt_col)
features = np.setdiff1d(all_data.columns,  result_cols).tolist()
all_data = all_data[features]

f = plt.figure(figsize=(10, 10))
plt.matshow(all_data.corr(), fignum=f.number)
plt.xticks(range(all_data.shape[1]), all_data.columns, fontsize=14, rotation=45)
plt.yticks(range(all_data.shape[1]), all_data.columns, fontsize=14)
cb = plt.colorbar()
cb.ax.tick_params(labelsize=14)
filename = path + output_folder + '/feature_corr_outcome_heatmap2.png'
plt.savefig(filename)
plt.show()
plt.gcf().clear()

