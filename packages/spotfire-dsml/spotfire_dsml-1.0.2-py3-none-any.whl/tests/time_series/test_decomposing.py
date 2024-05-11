
"""
to run the test, from the root folder open terminal and run:

pytest .\\src\\tests\\test.py


TODO: 
- Types checking
- Combined different phase signal test

Test Cases (for both Convolution and Fouier, total = 16 tests):
test1: 
    inputs: ts, index = -1, ts_delta not provided
    expected output: No errors, no null, 4 components
test2:
    inputs: ts, index = -1, ts_delta provided
    expected output: No errors, no null, 4 components
test3:
    inputs: ts
    expected output: No errors, no null, 4 components
test4:
    input: index is provides as int, 1
    expected output: No errors, no null
test5:
    input: only ts
    output: expected output: No errors, no null
test6:
    input: no index, data_col is provided as a name
    output: expected output: No errors, no null
test7:
    input: no index, data_col is provided as a int
    output: expected output: No errors, no null
test8:
    input: index provided as name
    output: expected output: No errors, no null
test9:
    input: one data column, no index
    out: expected output: No errors, no null

test10-end: Repeated above tests for Fourier
"""
from pathlib import Path
import sys
import os

# Get the current working directory
current_dir = Path(os.getcwd())

# Assuming the current directory is tests/time_series or a subdirectory of the project
# Adjust the number of parent calls as needed based on your actual directory structure
project_root = current_dir.parent.parent

# Add the project root to sys.path
sys.path.append(str(project_root))

import numpy as np
import pytest
import pandas as pd
import os
from io import StringIO
from spotfire_dsml.time_series.decomposing import fftInverse, FftDecompose, ConvDecompose







#df_2cols = pd.read_csv('.\\tests\\time_series\\decomposing_data\\dataset_ind_var.csv')
df_2cols = pd.read_csv(StringIO("""Month,Passengers
1949-01,112
1949-02,118
1949-03,132
1949-04,129
1949-05,121
1949-06,135
1949-07,148
1949-08,148
1949-09,136
1949-10,119
1949-11,104
1949-12,118
1950-01,115
1950-02,126
1950-03,141
1950-04,135
1950-05,125
1950-06,149
1950-07,170
1950-08,170
1950-09,158
1950-10,133
1950-11,114
1950-12,140
1951-01,145
1951-02,150
1951-03,178
1951-04,163
1951-05,172
1951-06,178
1951-07,199
1951-08,199
1951-09,184
1951-10,162
1951-11,146
1951-12,166
1952-01,171
1952-02,180
1952-03,193
1952-04,181
1952-05,183
1952-06,218
1952-07,230
1952-08,242
1952-09,209
1952-10,191
1952-11,172
1952-12,194
1953-01,196
1953-02,196
1953-03,236
1953-04,235
1953-05,229
1953-06,243
1953-07,264
1953-08,272
1953-09,237
1953-10,211
1953-11,180
1953-12,201
1954-01,204
1954-02,188
1954-03,235
1954-04,227
1954-05,234
1954-06,264
1954-07,302
1954-08,293
1954-09,259
1954-10,229
1954-11,203
1954-12,229
1955-01,242
1955-02,233
1955-03,267
1955-04,269
1955-05,270
1955-06,315
1955-07,364
1955-08,347
1955-09,312
1955-10,274
1955-11,237
1955-12,278
1956-01,284
1956-02,277
1956-03,317
1956-04,313
1956-05,318
1956-06,374
1956-07,413
1956-08,405
1956-09,355
1956-10,306
1956-11,271
1956-12,306
1957-01,315
1957-02,301
1957-03,356
1957-04,348
1957-05,355
1957-06,422
1957-07,465
1957-08,467
1957-09,404
1957-10,347
1957-11,305
1957-12,336
1958-01,340
1958-02,318
1958-03,362
1958-04,348
1958-05,363
1958-06,435
1958-07,491
1958-08,505
1958-09,404
1958-10,359
1958-11,310
1958-12,337
1959-01,360
1959-02,342
1959-03,406
1959-04,396
1959-05,420
1959-06,472
1959-07,548
1959-08,559
1959-09,463
1959-10,407
1959-11,362
1959-12,405
1960-01,417
1960-02,391
1960-03,419
1960-04,461
1960-05,472
1960-06,535
1960-07,622
1960-08,606
1960-09,508
1960-10,461
1960-11,390
1960-12,432
"""))

#df_4cols = pd.read_csv('.\\tests\\time_series\\decomposing_data\\dataset_2ind_2vars.csv')
df_4cols = pd.read_csv(StringIO("""date,data,data2,date2
1949-01,112,1,1949-01
1949-02,118,2,1949-02
1949-03,132,3,1949-03
1949-04,129,4,1949-04
1949-05,121,5,1949-05
1949-06,135,6,1949-06
1949-07,148,7,1949-07
1949-08,148,8,1949-08
1949-09,136,9,1949-09
1949-10,119,10,1949-10
1949-11,104,11,1949-11
1949-12,118,12,1949-12
1950-01,115,13,1950-01
1950-02,126,14,1950-02
1950-03,141,15,1950-03
1950-04,135,16,1950-04
1950-05,125,17,1950-05
1950-06,149,18,1950-06
1950-07,170,19,1950-07
1950-08,170,20,1950-08
1950-09,158,21,1950-09
1950-10,133,22,1950-10
1950-11,114,23,1950-11
1950-12,140,24,1950-12
1951-01,145,25,1951-01
1951-02,150,26,1951-02
1951-03,178,27,1951-03
1951-04,163,28,1951-04
1951-05,172,29,1951-05
1951-06,178,30,1951-06
1951-07,199,31,1951-07
1951-08,199,32,1951-08
1951-09,184,33,1951-09
1951-10,162,34,1951-10
1951-11,146,35,1951-11
1951-12,166,36,1951-12
1952-01,171,37,1952-01
1952-02,180,38,1952-02
1952-03,193,39,1952-03
1952-04,181,40,1952-04
1952-05,183,41,1952-05
1952-06,218,42,1952-06
1952-07,230,43,1952-07
1952-08,242,44,1952-08
1952-09,209,45,1952-09
1952-10,191,46,1952-10
1952-11,172,47,1952-11
1952-12,194,48,1952-12
1953-01,196,49,1953-01
1953-02,196,50,1953-02
1953-03,236,51,1953-03
1953-04,235,52,1953-04
1953-05,229,53,1953-05
1953-06,243,54,1953-06
1953-07,264,55,1953-07
1953-08,272,56,1953-08
1953-09,237,57,1953-09
1953-10,211,58,1953-10
1953-11,180,59,1953-11
1953-12,201,60,1953-12
1954-01,204,61,1954-01
1954-02,188,62,1954-02
1954-03,235,63,1954-03
1954-04,227,64,1954-04
1954-05,234,65,1954-05
1954-06,264,66,1954-06
1954-07,302,67,1954-07
1954-08,293,68,1954-08
1954-09,259,69,1954-09
1954-10,229,70,1954-10
1954-11,203,71,1954-11
1954-12,229,72,1954-12
1955-01,242,73,1955-01
1955-02,233,74,1955-02
1955-03,267,75,1955-03
1955-04,269,76,1955-04
1955-05,270,77,1955-05
1955-06,315,78,1955-06
1955-07,364,79,1955-07
1955-08,347,80,1955-08
1955-09,312,81,1955-09
1955-10,274,82,1955-10
1955-11,237,83,1955-11
1955-12,278,84,1955-12
1956-01,284,85,1956-01
1956-02,277,86,1956-02
1956-03,317,87,1956-03
1956-04,313,88,1956-04
1956-05,318,89,1956-05
1956-06,374,90,1956-06
1956-07,413,91,1956-07
1956-08,405,92,1956-08
1956-09,355,93,1956-09
1956-10,306,94,1956-10
1956-11,271,95,1956-11
1956-12,306,96,1956-12
1957-01,315,97,1957-01
1957-02,301,98,1957-02
1957-03,356,99,1957-03
1957-04,348,100,1957-04
1957-05,355,101,1957-05
1957-06,422,102,1957-06
1957-07,465,103,1957-07
1957-08,467,104,1957-08
1957-09,404,105,1957-09
1957-10,347,106,1957-10
1957-11,305,107,1957-11
1957-12,336,108,1957-12
1958-01,340,109,1958-01
1958-02,318,110,1958-02
1958-03,362,111,1958-03
1958-04,348,112,1958-04
1958-05,363,113,1958-05
1958-06,435,114,1958-06
1958-07,491,115,1958-07
1958-08,505,116,1958-08
1958-09,404,117,1958-09
1958-10,359,118,1958-10
1958-11,310,119,1958-11
1958-12,337,120,1958-12
1959-01,360,121,1959-01
1959-02,342,122,1959-02
1959-03,406,123,1959-03
1959-04,396,124,1959-04
1959-05,420,125,1959-05
1959-06,472,126,1959-06
1959-07,548,127,1959-07
1959-08,559,128,1959-08
1959-09,463,129,1959-09
1959-10,407,130,1959-10
1959-11,362,131,1959-11
1959-12,405,132,1959-12
1960-01,417,133,1960-01
1960-02,391,134,1960-02
1960-03,419,135,1960-03
1960-04,461,136,1960-04
1960-05,472,137,1960-05
1960-06,535,138,1960-06
1960-07,622,139,1960-07
1960-08,606,140,1960-08
1960-09,508,141,1960-09
1960-10,461,142,1960-10
1960-11,390,143,1960-11
1960-12,432,144,1960-12
"""))


#df_swapped_ind = pd.read_csv('.\\tests\\time_series\\decomposing_data\\dataset_var_ind.csv')
df_swapped_ind = pd.read_csv(StringIO("""Passengers,Month
112,1949-01
118,1949-02
132,1949-03
129,1949-04
121,1949-05
135,1949-06
148,1949-07
148,1949-08
136,1949-09
119,1949-10
104,1949-11
118,1949-12
115,1950-01
126,1950-02
141,1950-03
135,1950-04
125,1950-05
149,1950-06
170,1950-07
170,1950-08
158,1950-09
133,1950-10
114,1950-11
140,1950-12
145,1951-01
150,1951-02
178,1951-03
163,1951-04
172,1951-05
178,1951-06
199,1951-07
199,1951-08
184,1951-09
162,1951-10
146,1951-11
166,1951-12
171,1952-01
180,1952-02
193,1952-03
181,1952-04
183,1952-05
218,1952-06
230,1952-07
242,1952-08
209,1952-09
191,1952-10
172,1952-11
194,1952-12
196,1953-01
196,1953-02
236,1953-03
235,1953-04
229,1953-05
243,1953-06
264,1953-07
272,1953-08
237,1953-09
211,1953-10
180,1953-11
201,1953-12
204,1954-01
188,1954-02
235,1954-03
227,1954-04
234,1954-05
264,1954-06
302,1954-07
293,1954-08
259,1954-09
229,1954-10
203,1954-11
229,1954-12
242,1955-01
233,1955-02
267,1955-03
269,1955-04
270,1955-05
315,1955-06
364,1955-07
347,1955-08
312,1955-09
274,1955-10
237,1955-11
278,1955-12
284,1956-01
277,1956-02
317,1956-03
313,1956-04
318,1956-05
374,1956-06
413,1956-07
405,1956-08
355,1956-09
306,1956-10
271,1956-11
306,1956-12
315,1957-01
301,1957-02
356,1957-03
348,1957-04
355,1957-05
422,1957-06
465,1957-07
467,1957-08
404,1957-09
347,1957-10
305,1957-11
336,1957-12
340,1958-01
318,1958-02
362,1958-03
348,1958-04
363,1958-05
435,1958-06
491,1958-07
505,1958-08
404,1958-09
359,1958-10
310,1958-11
337,1958-12
360,1959-01
342,1959-02
406,1959-03
396,1959-04
420,1959-05
472,1959-06
548,1959-07
559,1959-08
463,1959-09
407,1959-10
362,1959-11
405,1959-12
417,1960-01
391,1960-02
419,1960-03
461,1960-04
472,1960-05
535,1960-06
622,1960-07
606,1960-08
508,1960-09
461,1960-10
390,1960-11
432,1960-12
"""))


#df_2_vars = pd.read_csv('.\\tests\\time_series\\decomposing_data\\dataset_2_var.csv')
df_2_vars = pd.read_csv(StringIO("""Passengers,Passengers1
112,112
118,118
132,132
129,129
121,121
135,135
148,148
148,148
136,136
119,119
104,104
118,118
115,115
126,126
141,141
135,135
125,125
149,149
170,170
170,170
158,158
133,133
114,114
140,140
145,145
150,150
178,178
163,163
172,172
178,178
199,199
199,199
184,184
162,162
146,146
166,166
171,171
180,180
193,193
181,181
183,183
218,218
230,230
242,242
209,209
191,191
172,172
194,194
196,196
196,196
236,236
235,235
229,229
243,243
264,264
272,272
237,237
211,211
180,180
201,201
204,204
188,188
235,235
227,227
234,234
264,264
302,302
293,293
259,259
229,229
203,203
229,229
242,242
233,233
267,267
269,269
270,270
315,315
364,364
347,347
312,312
274,274
237,237
278,278
284,284
277,277
317,317
313,313
318,318
374,374
413,413
405,405
355,355
306,306
271,271
306,306
315,315
301,301
356,356
348,348
355,355
422,422
465,465
467,467
404,404
347,347
305,305
336,336
340,340
318,318
362,362
348,348
363,363
435,435
491,491
505,505
404,404
359,359
310,310
337,337
360,360
342,342
406,406
396,396
420,420
472,472
548,548
559,559
463,463
407,407
362,362
405,405
417,417
391,391
419,419
461,461
472,472
535,535
622,622
606,606
508,508
461,461
390,390
432,432
"""))

df_1_var = df_2cols[['Passengers']]
random_rows = np.random.choice(df_2cols.index, size=10, replace=False)
df_uneven = df_2cols.drop(random_rows)


#Testing ConvDecompose
def test_conv1():
    print('Convolution testing 2 cols dataset with index =-1')
    assert ConvDecompose(df_2cols, index = -1).shape[1] == 4
def test_conv2():
    print('Convolution testing 2 cols dataset with index =-1 and delta is month')
    assert ConvDecompose(df_2cols, index = -1, ts_delta='M').\
    shape[1] == 4
def test_conv3():
    print('Convolution testing 2 cols dataset with everything set to default')
    assert ConvDecompose(df_2cols).shape[1] == 4
def test_conv4():
    print('Convolution testing 2 cols dataset with index and data columns are the same')
    with pytest.raises(Exception):
        ConvDecompose(df_swapped_ind, index = 1)
def test_conv5():
    with pytest.raises(Exception):
        print('Convolution testing more than 2 columns')
        ConvDecompose(df_4cols)
def test_conv6():
    print('Convolution testing providing a column name for data column')
    assert ConvDecompose(df_2_vars, index = -1, data_col='Passengers1').shape[1] == 4
def test_conv7():
    print('Convolution testing no index provided')
    assert ConvDecompose(df_2_vars, index = -1, data_col=1).shape[1] == 4
def test_conv8():
    print('Convolution testing index column name provided')
    assert ConvDecompose(df_swapped_ind, index = 'Month').shape[1] == 4
def test_conv9():
    print('Convolution testing one column dataset')
    assert ConvDecompose(df_1_var).shape[1]==4
def test_conv10():
    print('Convolution testing that timeseries type is DataFrame')
    assert type(ConvDecompose(df_1_var)) is pd.DataFrame
def test_conv11():
    print('Convolution testing unequally spaced index')
    assert ConvDecompose(df_uneven, index = -1).shape[1] == 4

# # testing FftDecompose
def test_fft1():
     print('Fourier testing 2 column with index = -1 ')
     assert FftDecompose(df_2cols, index = -1).all()
def test_fft2():
    print('Fourier testing with delta = month')
    assert FftDecompose(df_2cols, index = -1, ts_delta='M').all()
def test_fft3():
     print('Fourier testing with 2 columns, all default')
     assert FftDecompose(df_2cols).all()
def test_fft4():
     print('Fourier testing with swapped index')
     assert FftDecompose(df_swapped_ind, index = 1, data_col=0).all()
def test_fft5():
     print('Fourier testing with 4 columns')
     with pytest.raises(Exception):
         FftDecompose(df_4cols).all()
def test_fft6():
     print('Fourier testing with data column provided as string')
     assert FftDecompose(df_2_vars, index = -1, data_col='Passengers1').all()
def test_fft7():
     print('Fourier testing with no valid index, data column location provided')
     assert FftDecompose(df_2_vars, index = -1, data_col=1).all()
def test_fft8():
     print('Fourier testing with index column name provided')
     assert FftDecompose(df_swapped_ind, index = 'Month').all()
def test_fft9():
    print('Fourier testing with one column proivded')
    assert FftDecompose(df_1_var).all()
def test_fft10():
    print('Fourier testing output is complex')
    assert np.iscomplexobj (FftDecompose(df_1_var))
def test_fft11():
     print('Fourier testing index and data cols are the same')
     with pytest.raises(Exception):
         FftDecompose(df_2cols, index = 1).all()
def test_fft12():
     print('Fourier testing with unequally spaced index')
     assert FftDecompose(df_uneven).all()

# testing fft_inverse
def test_fftinv1():
    signal = FftDecompose(df_1_var)
    assert fftInverse(signal).all()
    assert np.isreal(fftInverse(signal)).all()
#Testing ConvDecompose
def test_conv1():
    print('Convolution testing 2 cols dataset with index =-1')
    assert ConvDecompose(df_2cols, index = -1).shape[1] == 4
def test_conv2():
    print('Convolution testing 2 cols dataset with index =-1 and delta is month')
    assert ConvDecompose(df_2cols, index = -1, ts_delta='M').\
    shape[1] == 4
def test_conv3():
    print('Convolution testing 2 cols dataset with everything set to default')
    assert ConvDecompose(df_2cols).shape[1] == 4
def test_conv4():
    print('Convolution testing 2 cols dataset with index and data columns are the same')
    with pytest.raises(Exception):
        ConvDecompose(df_swapped_ind, index = 1)
def test_conv5():
    with pytest.raises(Exception):
        print('Convolution testing more than 2 columns')
        ConvDecompose(df_4cols)
def test_conv6():
    print('Convolution testing providing a column name for data column')
    assert ConvDecompose(df_2_vars, index = -1, data_col='Passengers1').shape[1] == 4
def test_conv7():
    print('Convolution testing no index provided')
    assert ConvDecompose(df_2_vars, index = -1, data_col=1).shape[1] == 4
def test_conv8():
    print('Convolution testing index column name provided')
    assert ConvDecompose(df_swapped_ind, index = 'Month').shape[1] == 4
def test_conv9():
    print('Convolution testing one column dataset')
    assert ConvDecompose(df_1_var).shape[1]==4
def test_conv10():
    print('Convolution testing that timeseries type is DataFrame')
    assert type(ConvDecompose(df_1_var)) is pd.DataFrame
def test_conv11():
    print('Convolution testing unequally spaced index')
    assert ConvDecompose(df_uneven, index = -1).shape[1] == 4

# # testing FftDecompose
def test_fft1():
     print('Fourier testing 2 column with index = -1 ')
     assert FftDecompose(df_2cols, index = -1).all()
def test_fft2():
    print('Fourier testing with delta = month')
    assert FftDecompose(df_2cols, index = -1, ts_delta='M').all()
def test_fft3():
     print('Fourier testing with 2 columns, all default')
     assert FftDecompose(df_2cols).all()
def test_fft4():
     print('Fourier testing with swapped index')
     assert FftDecompose(df_swapped_ind, index = 1, data_col=0).all()
def test_fft5():
     print('Fourier testing with 4 columns')
     with pytest.raises(Exception):
         FftDecompose(df_4cols).all()
def test_fft6():
     print('Fourier testing with data column provided as string')
     assert FftDecompose(df_2_vars, index = -1, data_col='Passengers1').all()
def test_fft7():
     print('Fourier testing with no valid index, data column location provided')
     assert FftDecompose(df_2_vars, index = -1, data_col=1).all()
def test_fft8():
     print('Fourier testing with index column name provided')
     assert FftDecompose(df_swapped_ind, index = 'Month').all()
def test_fft9():
    print('Fourier testing with one column proivded')
    assert FftDecompose(df_1_var).all()
def test_fft10():
    print('Fourier testing output is complex')
    assert np.iscomplexobj (FftDecompose(df_1_var))
def test_fft11():
     print('Fourier testing index and data cols are the same')
     with pytest.raises(Exception):
         FftDecompose(df_2cols, index = 1).all()
def test_fft12():
     print('Fourier testing with unequally spaced index')
     assert FftDecompose(df_uneven).all()

# testing fft_inverse
def test_fftinv1():
    signal = FftDecompose(df_1_var)
    assert fftInverse(signal).all()
    assert np.isreal(fftInverse(signal)).all()
