import pandas as pd
import  math
import numpy as np
import re


# the path ti the file
path = './'
file_name = 'Data Abstraction Sheet- COMPLETED-WITH UNIQUE ID Gastro manisfestations in COVID19 5-26-2020 .xlsx'
full_file_path = path + file_name

# thse indices are entered manually after scanning the column F
# in the excel sheet
blacklist_idx = [812, 811, 806, 804, 803, 798, 794, 793, 792, 790, 
        789, 788, 787, 785, 784, 779, 778, 776, 774, 773, 772, 770,
        759, 758, 757, 756, 755, 754, 753, 752, 751, 750, 749, 748, 
        747, 746, 745, 744, 743, 742, 741, 740, 739, 738, 737, 736,
        735, 734, 733, 732, 731, 730, 707, 708, 709, 710, 711, 712, 
        714, 715, 716, 717, 718, 719, 720, 721, 723, 724, 
        725, 726, 727, 728, 729, 702, 691, 692, 693, 694, 695, 696, 
        689, 685, 675, 676, 677, 678, 679, 680, 681, 682, 683, 684]

print('before blacklist_idx: ',blacklist_idx)
# the excel sheet index and the actual df index differ by 2, hence
blacklist_idx = [x-2 for x in blacklist_idx]
print('after blacklist_idx: ',blacklist_idx)

df = pd.read_excel(full_file_path, sheet_name='Sheet1')
# number of rows and columns
print('rows: ', len(df.index))
print('columns: ', len(df.columns))

# ---------------- Preprocessing ------------------
# --------deleting unnecessary columns and rows
# delete unnamed columns, is it needed?
df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

print('after deleting')
print(len(df.columns))

# the rows from 567 to 672 in excel sheet have non covid patients data
# and hence being removed. We will perform the delete NaN row operation after this
# because deleting the NaN rows might change the row indices
x = 565
y = 671
#print(df.loc[x])
#print(df.loc[y])
# create a list containing all the indices in the range (x, y+1)
idx = [i for i in range(x, y)]
print('idx :', idx)
# delete the rows with indices in the list idx
#df = df.reset_index()
print(df.columns[0])
print(df.columns[1])
# add the blacklist_idx to the list of indices to be dropped, because sequentially doing them
# could change the row numbers
final_idx = idx + blacklist_idx
df.drop(df.index[final_idx], inplace=True)
#plrint(df.columns)
print(df.columns[0])
print(df.columns[1])
print('rows: ', len(df.index))
print('columns: ', len(df.columns))
# the drop parameter ensures that index does not get added as a separate column
df.reset_index(drop=True, inplace=True)
print(df.columns[0])
print(df.columns[1])
#print(df.loc[x])
print('rows: ', len(df.index))
print('columns: ', len(df.columns))
first_col_name = df.columns[0]

# get the contents of the first column
first_col_contents = df[first_col_name]
#print(first_col_contents)
print('rows: ', len(df.index))
print('columns: ', len(df.columns))


# printing the contents of the first column
# by traversing over the rows
#print(df.iloc[538, :])
# check for the presence of NaN value under the first column
print('does the first column have any NaN value>', df[first_col_name].isnull().values.any())
# check for the count of NaN valuies under the first column
print('count of NaN values under the first columns', df[first_col_name].isnull().values.sum())
# get the row indices where UNIQ_PT value is NaN
nan_row_idx = []
for i, j in first_col_contents.iteritems():
    if math.isnan(j):
        #print(i)
        nan_row_idx.append(i)

# check the list of indices with NaN value in first column
print(nan_row_idx)
# mae sure the indices are integer
print(isinstance(nan_row_idx[0], int))

# filtered_df to hold the preprocessed df
#filtered_df = None
# delete the specific rows with NaN values in first column
prev_len = len(df.index)    # keep the previous no. of rows for a cross-check
df.drop(df.index[nan_row_idx], inplace=True)
df.reset_index(drop=True, inplace=True)
print('rows: ', len(df.index))
print('columns: ', len(df.columns))

# check again whether the values are actually deleted, this time we should get False and 0
# check for the presence of NaN value under the first column
print('does the first column have any NaN value>', df[first_col_name].isnull().values.any())
# check for the count of NaN valuies under the first column
print('count of NaN values under the first columns', df[first_col_name].isnull().values.sum())
if len(nan_row_idx) != (prev_len - len(df.index)):
    print('prev #rows: ', prev_len)
    print('cur #rows: ', len(df.index))
    print('columns: ', len(df.columns))
    #raise ValueError 'Mismatch in size after deletion'
    print('Mismatch in size after deletion')
    raise ValueError('Mismatch in size after deletion')
else:
    print('prev #rows: ', prev_len)
    print('cur #rows: ', len(df.index))
    print('columns: ', len(df.columns))
    print('no mimatch')


# ---------- Preprocessing----------------- #
# the columns UNIQ_PT and UNIQ_VIS can be deleted
# because they do not contain any important information
# regarding the disease of the patient
del_pat_ids = False
offset = 2
if del_pat_ids is True:
    df.drop(columns=['UNIQ_PT', 'UNIQ_VIS'], inplace=True)
    print('rows: ', len(df.index))
    print('columns: ', len(df.columns))

# ---------- Preprocessing----------------- #
# TBD: blacklisted columns to be deleted and non numeric values in 
# column F to be replaced with 0
# done above: blacklist_idx

# ---------- Verification preparation ----- #
# At the end of the entire pre-processing the
# entries need to be verified. Our verification
# mechanism is:
# 1. create copy of the df at this step
# 2. create a list of idx for each column where entries are not real numbers
# 3. At the end of all preprocessing, compare the final df
# with the df created at step 1 and list all the idx of the columns
# where the entries do not match
# 4. the list of idx created at step 2 should match with the idx list created at step 3
# 5. create file with the prev and cur entries for those idx
# 6. check the final df to ensure that there are no non-real values
# 7. report the columns which have the non matching entries
df_copy = df.copy()
init_idx_list = []  # contains the initial list of idx from all columns, list of lists
for i in range(len(df.columns)):
    sub_list = []       # to hold the idx for a particular column
    for j, val in df[df.columns[i]].iteritems():
        if np.isreal(val) is False:
            sub_list.append(j)
    init_idx_list.append(sub_list)
print(init_idx_list)

#------------- Preprocessing----------------#
# setting the non numeric values in triage column to 0
def map_non_numeric_to_zero(x):
    if np.isreal(x) is False:
        x = 0.0
    return x

COL = 3
if del_pat_ids is False:
    COL = COL + offset
df[df.columns[COL]] = df[df.columns[COL]].map(map_non_numeric_to_zero)
print(df[df.columns[COL]])

# ------------- Preprocessing --------------#
# handle the comma separated values by augmenting the
# variables

# ------------ Preprocessing ---------------#
# get the column SpO2 and the percentage sign out of it
k = 0
for i in range(len(df.columns)):
    if df.columns[i].find('SpO2') != -1:
        print(df.columns[i])
        print(i)    # the column at this index has SpO2 in its heading
        k = i

# checking what kind of elements are in SpO2 columns - str, float, and nan
# SpO2 column no., is 25
aa = df[df.columns[k]].unique().tolist()
print(aa)
col_copy  = df[df.columns[k]].copy()
for i, val in df[df.columns[k]].iteritems():
    print(f"Index : {i}, Value : {val}")
    if np.isreal(val) is True:
        print(f"real number: Index : {i}, Value : {val}")
        if val < 1:
            print('{} is < 1'.format(val))
            val = val * (100.0)
            df.iloc[i, k] = val
    else:
        print(f"Not a real number:Index : {i}, Value : {val}")
        if val.find('%') != -1 or val.find(' ') != -1 or val.find('s') != -1:
            num_val = re.split('%|\ |s', val)
            print('num_val[0]: ', num_val[0])
            print('float(num_val[0]): ', float(num_val[0]))
            df.iloc[i, k] = float(num_val[0])    
# the following does not work because for the non str numbers it returns nan
# ab = df[df.columns[25]].str.split('% ', n=-1, expand=True)

# ----------- Preprocessing ----------------#
# format the '>' and '<' symbol
uniq_vals = []
for j in range(len(df.columns)): 
    aa = df[df.columns[j]].unique().tolist() 
    uniq_vals.append(aa) 
    for i in range(len(aa)): 
        if np.isreal(aa[i]) is False: 
            if aa[i].find('>') != -1 or aa[i].find('<') != -1: 
                print(j) 
                print(df.columns[j]) 

# ----------- Preprocessing ----------------#
# check the datatype of the columns. The columns
# which has object as datatype are the onbes that
# need cleaning, again most of them would be object
# because of the presence of the 'n/a' string
for i in range(len(df.columns)):
    print(df[df.columns[i]].dtypes)

# count of object columns and obj_idx to hold the indices
# where the dtype is object
cnt = 0
obj_idx = []
for i in range(len(df.columns)): 
    if df[df.columns[i]].dtypes == np.dtype('O'): 
        #print('column {} is: {}'.format(i, df[df.columns[i]].dtypes))
        cnt += 1
        obj_idx.append(i)

print(cnt)
print(obj_idx)

# take the unique objects before preprocessing in aa_v (v is the index)
v = 2 # column for stay duration, this contains some extraneous strings
if del_pat_ids is False:
    v = v + offset
aa_v = df[df.columns[v]].unique().tolist()
# make a copy of the column just to verify after preprocessing
# here the preprocessing was to convert strings like '43, covid' to 43
col_copy_v  = df[df.columns[v]].copy()
cnt = 0
for i, val in df[df.columns[v]].iteritems():
    #print(f"Index : {i}, Value : {val}")
    if np.isreal(val) is False:
        #print(f"Not a real number:Index : {i}, Value : {val}")
        if val.find('%') != -1 or val.find(' ') != -1 or val.find('s') != -1 or val.find(',') != -1:
            num_val = re.split('%|\ |s|,', val)
            #print('num_val[0]: ', num_val[0])
            if num_val[0].isnumeric() is True:
                print('float(num_val[0]): ', float(num_val[0]))
                df.iloc[i, v] = float(num_val[0])
                cnt += 1
print('entries modified in col {} is :{}'.format(v, cnt))

# column 4 does not need any cleanup because there are no strings
v = 4
if del_pat_ids is False:
    v = v + offset
cnt = 0
for i, val in df[df.columns[v]].iteritems():
    #print(f"Index : {i}, Value : {val}")
    if np.isreal(val) is False:
        print(f"Index : {i}, Value : {val}") 
        cnt += 1

if cnt == 0:
    print('no string/value to be edited')

# filter those columns which are object columns and yet need to be modified
# i.e. columns which contains values other than float64 and nan(which is a real number)
filtered_obj_idx = []                                                                                                                                                                               

for m in range(len(obj_idx)): 
    cnt = 0  
    for i, val in df[df.columns[obj_idx[m]]].iteritems():  
        #print(f"Index : {i}, Value : {val}")  
        if np.isreal(val) is False:  
            #print(f"Index : {i}, Value : {val}")  
            cnt += 1    
    if cnt != 0:  
        filtered_obj_idx.append(obj_idx[m]) 

# preprocessing column 6 (Gender). Map the 'Male', 'Female' string to
# proper values and map every other number to nan
v = 6 # column for stay duration, this contains some extraneous strings 
if del_pat_ids is False:
    v = v + offset
aa_v = df[df.columns[v]].unique().tolist() 
# make a copy of the column just to verify after preprocessing 
# here the preprocessing was to convert strings like '43, covid' to 43 
col_copy_v  = df[df.columns[v]].copy() 
cnt = 0 
for i, val in df[df.columns[v]].iteritems(): 
    #print(f"Index : {i}, Value : {val}") 
    if np.isreal(val) is False: 
        if val.lower().find('female') != -1 or val.lower().find('f') != -1: 
            df.iloc[i, v] = float(1.0) 
        elif val.lower().find('male') != -1 or val.lower().find('m') != -1: 
            df.iloc[i, v] = float(0.0) 
aa_v = df[df.columns[v]].unique().tolist() 
#print(aa_v)
#print(ab_v)

# column 10, 11, 12, 13 are comma separated, need separate processing.
v = 14 # column for stay duration, this contains some extraneous strings 
if del_pat_ids is False:
    v = v + offset
aa_v = df[df.columns[v]].unique().tolist() 
# make a copy of the column just to verify after preprocessing 
# here the preprocessing was to convert strings like '43, covid' to 43 
col_copy_v  = df[df.columns[v]].copy() 
cnt = 0  
for i, val in df[df.columns[v]].iteritems(): 
    #print(f"Index : {i}, Value : {val}") 
    if np.isreal(val) is False:
        if val in 'o':
            df.iloc[i, v] = float(0.0)
aa_v = df[df.columns[v]].unique().tolist()
print(aa_v)


# column 15 has strings like '<5', '6 beers', 'o' , 'unknown' etc
# make a copy of the column just to verify after preprocessing
# here the preprocessing was to convert strings like '43, covid' to 43
v = 15 # column for stay duration, this contains some extraneous strings 
if del_pat_ids is False:
    v = v + offset
aa_v = df[df.columns[v]].unique().tolist() 
print(aa_v)
col_copy_v  = df[df.columns[v]].copy()
cnt = 0
for i, val in df[df.columns[v]].iteritems():
    #print(f"Index : {i}, Value : {val}")
    if np.isreal(val) is False:
        if val in 'o':
            df.iloc[i, v] = float(0.0)
             #print(f"Not a real number:Index : {i}, Value : {val}")
        elif val.find('%') != -1 or val.find(' ') != -1 or val.find('s') != -1 or val.find(',') != -1:
            num_val = re.split('%|\ |s|,', val)
            #print('num_val[0]: ', num_val[0])
            if num_val[0].isnumeric() is True:
                #print('float(num_val[0]): ', float(num_val[0]))
                df.iloc[i, v] = float(num_val[0])
        elif val.find('<') != -1 or val.find('>') != -1:
            num_val = re.split('<|>', val)
            print(num_val)
            if num_val[1].isnumeric() is True:
                if val.find('<') != -1:
                    num_val[1] = float(num_val[1]) - 0.5
                elif val.find('>') != -1:
                    num_val[1] = float(num_val[1]) + 0.5
                print('float(num_val[1]): ', float(num_val[1]))
                df.iloc[i, v] = float(num_val[1])

aa_v = df[df.columns[v]].unique().tolist()
print(aa_v)

v = 16 # column for smokes per week
if del_pat_ids is False:
    v = v + offset
aa_v = df[df.columns[v]].unique().tolist() 
print(aa_v)
col_copy_v  = df[df.columns[v]].copy()
cnt = 0
for i, val in df[df.columns[v]].iteritems():
    #print(f"Index : {i}, Value : {val}")
    if np.isreal(val) is False:
        if val in 'o' or val in 'n':
            df.iloc[i, v] = float(0.0)
    elif val == 3:      # assuming choice 3 means the 3rd option which is at index 2
        df.iloc[i, v] = float(2.0)


aa_v = df[df.columns[v]].unique().tolist()
print(aa_v)

# col 17 smoking pack years has extra valus like 'o' and 'n'. They are
# both assumed to be 0
v_list = [17, 76] # column for smoking pack year
if del_pat_ids is False:
    v_list = [v_list[i] + offset for i in range(len(v_list))] 
for v in v_list:
    aa_v = df[df.columns[v]].unique().tolist()
    print(aa_v)
    col_copy_v  = df[df.columns[v]].copy()
    cnt = 0
    for i, val in df[df.columns[v]].iteritems():
        #print(f"Index : {i}, Value : {val}")
        if np.isreal(val) is False:
            if val.strip() in 'o' or val in 'n':
                df.iloc[i, v] = float(0.0)
    #aa_v = df[df.columns[v]].unique().tolist()
    #print(aa_v)


v = 20 # column for s
if del_pat_ids is False:
    v = v + offset
aa_v = df[df.columns[v]].unique().tolist()
print(aa_v)
col_copy_v  = df[df.columns[v]].copy()
cnt = 0
for i, val in df[df.columns[v]].iteritems():
    #print(f"Index : {i}, Value : {val}")
    if np.isreal(val) is False:
        if val.lower() in 'n':
            df.iloc[i, v] = float(0.0)
aa_v = df[df.columns[v]].unique().tolist()
print(aa_v)

v = 22 # testing mechamism
if del_pat_ids is False:
    v = v + offset
# value 0 will be amapped to 1 , a=strings like '5( output)'
# will be mapped to the value
aa_v = df[df.columns[v]].unique().tolist()
print(aa_v)
col_copy_v  = df[df.columns[v]].copy()
cnt = 0
for i, val in df[df.columns[v]].iteritems():
    #print(f"Index : {i}, Value : {val}")
    if np.isreal(val) is False:
        if val.find('%') != -1 or val.find(' ') != -1 or val.find('s') != -1 or val.find(',') != -1 or val.find('(') != -1:
            num_val = re.split('%|\ |s|,|\(', val)
            #print('num_val[0]: ', num_val[0])
            if num_val[0].isnumeric() is True:
                #print('float(num_val[0]): ', float(num_val[0]))
                df.iloc[i, v] = float(num_val[0])
aa_v = df[df.columns[v]].unique().tolist()
print(aa_v)

v = 22
if del_pat_ids is False:
    v = v + offset
for i, val in df[df.columns[v]].iteritems():
    if np.isreal(val) is False:
        if val.find('5') != -1:
            print('{}:  {}'.format(i, val))


# column 26
v = 26
if del_pat_ids is False:
    v = v + offset
aa_v = df[df.columns[v]].unique().tolist()
print(aa_v)
col_copy_v  = df[df.columns[v]].copy()
for i, val in df[df.columns[v]].iteritems(): 
    if np.isreal(val) is False: 
        if val.find('days') != -1: 
            print('{} :{} '.format(i, val)) 
            num_val = re.split('%|\ |s|,|\(', val) 
            for j in range(len(num_val)): 
                if num_val[j].isnumeric() is True: 
                    df.iloc[i, v] = float(num_val[j]) 


# column 32 and 33 iloc[169, 32] and iloc[482, 33] contains
# values '39/2' and '94/7' instead  of 39.3 and 94.7
v_list = [32, 33, 41]
if del_pat_ids is False:
    v_list = [v_list[i] + offset for i in range(len(v_list))] 
for v in v_list:
    aa_v = df[df.columns[v]].unique().tolist()
    print(aa_v)
    col_copy_v  = df[df.columns[v]].copy()
    for i, val in df[df.columns[v]].iteritems(): 
        if np.isreal(val) is False: 
            if val.find('/') != -1:
                num = float(val.replace('/', '.'))
                df.iloc[i, v] = float(num)




CONST = 0.005
v_list = [37, 38, 42, 63, 75, 76]
if del_pat_ids is False:
    v_list = [v_list[i] + offset for i in range(len(v_list))] 
for v in v_list:
    aa_v = df[df.columns[v]].unique().tolist()
    print(aa_v)
    col_copy_v  = df[df.columns[v]].copy()
    for i, val in df[df.columns[v]].iteritems():
        #print(f"Index : {i}, Value : {val}")
        if np.isreal(val) is False:
            if val.find('<') != -1 or val.find('>') != -1:
                num_val = re.split('<|>', val)
                print(num_val)
                if num_val[1].isnumeric() is True:
                    if val.find('<') != -1:
                        num_val[1] = float(num_val[1]) - CONST
                    elif val.find('>') != -1:
                        num_val[1] = float(num_val[1]) + CONST
                    print('float(num_val[1]): ', float(num_val[1]))
                    df.iloc[i, v] = float(num_val[1])

v = 47
if del_pat_ids is False:
    v = v + offset
aa_v = df[df.columns[v]].unique().tolist()
print(aa_v)
col_copy_v  = df[df.columns[v]].copy()
for i, val in df[df.columns[v]].iteritems():
    #print(f"Index : {i}, Value : {val}")
    if np.isreal(val) is False:
        if val.find('%') != -1 or val.find(' ') != -1 or val.find('s') != -1 or val.find(',') != -1 or val.find('(') != -1:
            num_val = re.split('%|\ |s|,|\(', val)
            #print('num_val[0]: ', num_val[0])
            if np.isreal(float(num_val[0])) is True:
                #print('float(num_val[0]): ', float(num_val[0]))
                df.iloc[i, v] = float(num_val[0])


v = 49      
if del_pat_ids is False:
    v = v + offset      
aa_v = df[df.columns[v]].unique().tolist()
print(aa_v)
col_copy_v  = df[df.columns[v]].copy()
for i, val in df[df.columns[v]].iteritems():
    if np.isreal(val) is False:
        if val.find(',') != -1:
            num = float(val.replace(',', '.'))
            df.iloc[i, v] = float(num)

CONST = 0.005
v_list = [51, 52, 56, 60, 61, 63, 66, 68, 74, 76]
if del_pat_ids is False:
    v_list = [v_list[i] + offset for i in range(len(v_list))]
for v in v_list:
    aa_v = df[df.columns[v]].unique().tolist()
    print(aa_v)
    col_copy_v  = df[df.columns[v]].copy()
    for i, val in df[df.columns[v]].iteritems():
        #print(f"Index : {i}, Value : {val}")
        if np.isreal(val) is False:
            if val.find('<') != -1 or val.find('>') != -1:
                num_val = re.split('<|>|\+', val)
                print(num_val)
                if np.isreal(float(num_val[1])) is True:
                    if val.find('<') != -1:
                        num_val[1] = float(num_val[1]) - CONST
                    elif val.find('>') != -1:
                        num_val[1] = float(num_val[1]) + CONST
                    print('float(num_val[1]): ', float(num_val[1]))
                    df.iloc[i, v] = float(num_val[1])
            if val.find('%') != -1 or val.find(' ') != -1 or val.find('s') != -1 or val.find(',') != -1 or val.find('(') != -1 or val.find('*') != -1:
                num_val = re.split('%|\ |s|,|\(|\*', val)
                #print('num_val[0]: ', num_val[0])
                if isinstance(num_val, str) is True and np.isreal(float(num_val[0])) is True:
                    #print('float(num_val[0]): ', float(num_val[0]))
                    df.iloc[i, v] = float(num_val[0])
            if val.find('+') != -1:
                num_val = val.split('+')
                for j in range(len(num_val)):
                    if num_val[j].isnumeric() is True:
                        print('float(num_val[j]): ', float(num_val[j]) + CONST)
                        df.iloc[i, v] = float(num_val[j]) + CONST


v_list = [64, 67]
if del_pat_ids is False:
    v_list = [v_list[i] + offset for i in range(len(v_list))]
for v in v_list:
    aa_v = df[df.columns[v]].unique().tolist()
    #print(aa_v)
    col_copy_v  = df[df.columns[v]].copy()
    for i, val in df[df.columns[v]].iteritems():
        #print(f"Index : {i}, Value : {val}")
        if np.isreal(val) is False:
            if val.find('(') != -1 or val.find(')') != -1 or val.find('`') != -1:
                num_val = re.split('\(|\)|`', val)
                print(num_val)
                for j in range(len(num_val)):
                    if num_val[j].isnumeric() is True:
                        print('float(num_val[1]): ', float(num_val[j]))
                        df.iloc[i, v] = float(num_val[j])

v_list = [76, 77]
if del_pat_ids is False:
    v_list = [v_list[i] + offset for i in range(len(v_list))]
for v in v_list:
    aa_v = df[df.columns[v]].unique().tolist()
    print(aa_v)
    col_copy_v  = df[df.columns[v]].copy()
    for i, val in df[df.columns[v]].iteritems():
        #print(f"Index : {i}, Value : {val}")
        if np.isreal(val) is False:
            if val.find('+') != -1:
                num_val = val.split('+')
                for j in range(len(num_val)):
                    if num_val[j].isnumeric() is True:
                        print('float(num_val[j]): ', float(num_val[j]) + CONST)
                        df.iloc[i, v] = float(num_val[j]) + CONST


v = 81
if del_pat_ids is False:
    v = v + offset
aa_v = df[df.columns[v]].unique().tolist()
print(aa_v)
col_copy_v  = df[df.columns[v]].copy()
for i, val in df[df.columns[v]].iteritems():
    #print(f"Index : {i}, Value : {val}")
    if np.isreal(val) is False:
        if  val.lower() in ['neg', 'negative']:
            df.iloc[i, v] = float(0.0)

comma_vals = []
comma_idx = []
for i in range(len(df.columns)):
    for j, val in df[df.columns[i]].iteritems():
        if np.isreal(val) is False:
            if ',' in val:
                comma_vals.append(df.columns[i])
                comma_idx.append(i)
                #print(df.columns[i])
                break
print(comma_idx)
print(len(comma_vals))

final_idx_list = []
mismatch_col_idx = []
new_file = open('mismatch_info.txt', 'w')
for i in range(len(df.columns)):
    new_file.write('col name: {}\n'.format(df.columns[i]))
    sub_list = []       # to hold the idx for a particular column
    for j, val in df[df.columns[i]].iteritems():
        if df.iloc[j, i] != df_copy.iloc[j, i] and not(math.isnan(df.iloc[j, i]) and math.isnan(df_copy.iloc[j, i])):
            new_file.write('col: {}, index: {}, prev value: {}, cur value: {}\n'.format(i, j, df_copy.iloc[j, i], df.iloc[j, i]))
            sub_list.append(j)
            if i not in mismatch_col_idx:
                mismatch_col_idx.append(i)
    final_idx_list.append(sub_list)
#`print(final_idx_list)
new_file.write('final_idx_list: {}\n'.format(final_idx_list))
new_file.write('mismatch_col_idx: {}\n'.format(mismatch_col_idx))
new_file.close()

# -------------------- Preprocessing ---------
# removing the column idx 15(Alcoholic drinks per week
# becaise this is not a truly comma separated value.
# this should have a single value
#rem_cols = [15, 80]
#for i in rem_cols:
#    comma_idx.remove(i)
#print(comma_idx)

# retaining a copy of df just for error checks
df_copy2 = df.copy()
#nan_column = [np.nan for i in range(len(df.index))]
#new_col_names = {}
comma_idx_copy = comma_idx
#comma_idx=[87]


df = df_copy2.copy()
# column 13 needs to be processed separately because of the different characters
v_list = [10, 11, 12, 13, 19, 21, 23, 29, 85, 86, 87]
if del_pat_ids is False:
    v_list = [v_list[i] + offset for i in range(len(v_list))]
for v in v_list:
    aa_v = df[df.columns[v]].unique().tolist()
    #print(aa_v)
    col_copy_v  = df[df.columns[v]].copy()
    for i, val in df[df.columns[v]].iteritems():
        #print(f"Index : {i}, Value : {val}")
        if np.isreal(val) is False:
            val = val.replace('.', ',')
            if val.find('-') or val.find(' ') or val.find('(') != -1 or val.find(')') != -1 or val.find(',') != -1 or val.find('`') != -1:
                num_val = re.split(',|\ |\(|\)|-|`', val)
                print(num_val)
                mod_str = ''
                for j in range(len(num_val)):
                    if len(num_val[j]) != 0:
                        if num_val[j].isnumeric() is True:
                            mod_str = mod_str + num_val[j] + ','
                if len(mod_str) != 0:
                    mod_str = mod_str[:-1] + ''
                    df.iloc[i, v] = mod_str
                    
            if 'unknown' in val.lower() or 'n/a' in val.lower():
                df.iloc[i, v] = np.nan
            if val.lower() in 'o'  or 'none' in val.lower() or val.lower() in 'n':
                df.iloc[i, v] = 0.0


# column 15 does not need extra rocessing, anyway non numeric values at the end
# will be replaced by np.nan


for i in range(len(comma_idx)):
    print(comma_idx[i])
    # get the name of the column
    col_name = df.columns[comma_idx[i]]
    print(col_name)
    # initialize an empty list which will hold new column names
    # created from thi sparticular column
    # split the column name to get the substrings separated by \r\n
    all_cols= []
    new_col_names = {}
    #col_name = col_name.replace('\r','')
    #col_name_subs = col_name.split('\n')
    col_name_subs = re.split('\r\n|\n', col_name)
    for j in range(1, len(col_name_subs)):
        # create the new column name by taking the first substr follwed by the specific option substring
        new_col_name = col_name_subs[0] + '_' + col_name_subs[j]
        # initially this column contains all nan values which is assigned as a dictionary value of the
        # keys corresponding to all the substring columns
        nan_column = [np.nan for l in range(len(df.index))]
        new_col_names[new_col_name] = nan_column
        all_cols.append(new_col_name)
    print(all_cols)
    #print(new_col_names)
    for k, val in df[col_name].iteritems():
        #print(k)
        # we have a string here, fo real numbers and np.nans control doesn't enter this loop
        if np.isreal(val) is False:
            print(f'val is {val}')
            #print('hi')
            # strip the string of all whitespaces
            val_mod = ''.join(val.split())
            #print(val_mod)
            #print(val_mod)
            # split the comma separated string to get individual number strings
            nums = []
            nums = val_mod.split(',')
            # iterate over the individual number strings to check which values
            # are present in a column name
            for y in range(len(nums)):
                num = nums[y]
                # two of the columns contain 'N' or 'n' instead of 0
                if 'N' in num or 'n' in num:
                    num = '0'
                    #print(nums)
                    #print(col_name)
                # the number can be part of the  newly formed column name in 4 way
                # forming those 4 possible substrings. If any of these substrings is
                # present in the col_names then
                poss_str = ['_' + num + '.', '_' + num + '=']
                print(poss_str)
                for l in new_col_names:
                    # flag to signal whether the number num is present in the column name or not
                    flag = False
                    for m in poss_str:
                        print('m is :', m)
                        flag = False
                        if m in l:
                            # number string num present in column name, setting flag to True and break
                            print(f'{m} is in {l}')
                            flag = True
                            # at least one of the popssible strings formed with num is present in the col name,
                            # hence we can break, no need of checking other possible strings
                            break
                    if flag is True:
                        print(f'{m} is found, setting {l} row {k} to 1')
                        # set the corresponding entry of the new column to 1
                        # this means this operation(option in the actual undivided heading column
                        # was performed or present in the (l, j) entry of the original table
                        # 0: absent, 1: present
                        new_col_names[l][k] = 1.0
                        #break
                    else:
                        if new_col_names[l][k] != 1.0 and new_col_names[l][k] != 0.0:
                            print(f'{m} is not found,  setting {l} row {k} to 0')
                            new_col_names[l][k] = 0.0
                        else:
                            print(f'{m} is not found,  setting {l} row {k} is not required, already set')
                # the values in new_col_names dictionary are modified according to the presence of the options
                # in the original dataframe column, time to create new dataframe columns corresponding to these
                # new columns and appending them to the original dataframe
                for l in new_col_names:
                    df[l] = new_col_names[l]


# ----------- Preprocessing ----------------#
# replace non numeric values in other columns with NaN or np.nan
# first collect all unique values from all of the columns in a list
# then filter it to have only the non-numeric values. any value 
# ----------- Preprocessing ----------------#
# replace non numeric values in other columns with NaN or np.nan
# first collect all unique values from all of the columns in a list
# then filter it to have only the non-numeric values. any value 
# appearing in any column from this filtered list has to be replaced
# np.nan
# where a non numeric valus is found in the dataframe 
# it is replaces with a nan value
#df = df.applymap(lambda x: x if np.isreal(x) is True else np.nan)
for i in range(len(df.columns)):
    if i > 3 and i not in comma_idx:
        df[df.columns[i]] = df[df.columns[i]].map(lambda x: x if np.isreal(x) is True else np.nan)


#f.columns[86]].str.contains('3')
# write to a acsv file
#df.to_csv('cleaned_data.csv')

# write to an excel file
#writer = pd.ExcelWriter('output.xlsx')
#df.to_excel(writer, 'cleaned_data', index = False)
#writer.save()
# write to an excel file, 3rd, 4th col datetime format
writer = pd.ExcelWriter('output.xlsx', datetime_format='dd/mm/yyyy')
df.to_excel(writer, 'cleaned_data', index = False)
workbook  = writer.book
worksheet = writer.sheets['cleaned_data']
if del_pat_ids is False:
    worksheet.set_column('C:C', 20)  # Assuming is the third column
    worksheet.set_column('D:D', 20)  # Assuming is the fourth column
else:
    worksheet.set_column('A:A', 20)  # Assuming is the first column when patient id columns are deleted
    worksheet.set_column('B:B', 20)  # Assuming is the escond column when patient id columns are deleted
writer.save()

