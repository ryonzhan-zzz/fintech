import numpy as np
import pandas as pd
import math
import sklearn
import sklearn.preprocessing
import datetime
import os
import matplotlib.pyplot as plt
import torch
import torch.nn as nn


# Install and import opendatasets

# Read the CSV file
df = pd.read_csv('prices-split-adjusted.csv')


# check2
## Make a figure

# a width of 15 inches and a height of 5 inches.
plt.figure(figsize=(15, 5))

# split into two sub-figures
plt.subplot(1, 2, 1)
# TODO: Fill in here to make the left figure, using plt.plot(...)

# YOUR TASK: plot the trend of open and close values of the EQIX stock, with:
# 1. different colors for each
# 2. a legend showing proper labels
# 3. meaningful x-axis and y-axis labels
# 4. a meaningful title
open_list=[]
close_list=[]
for i in range(len(df)):
    if df['symbol'][i]=='EQIX':
        open_list.append(df['open'][i])
        close_list.append(df['close'][i])

plt.plot(open_list,label='open')
plt.plot(close_list,label='close')
plt.legend()
plt.xlabel('time')
plt.ylabel('price')
plt.title('EQIX')
plt.show()


plt.subplot(1, 2, 2)
# # TODO: Fill in here to make the right figure, using plt.plot(...)
#
# # YOUR TASK: plot the trend of volumes of the AAL stock, with:
# # 1. a legend showing proper labels
# # 2. meaningful x-axis and y-axis labels
# # 3. a meaningful title
# # 4. as a sanity check, there should be a peak between x=1250 and x=1500

aal_list=[]
for i in range(len(df)):
    if df['symbol'][i]=='AAL':
        aal_list.append(df['volume'][i])
plt.plot(aal_list,label='AAL volumes')
plt.legend()
plt.xlabel('time')
plt.ylabel('volumes')
plt.title('AAL')
plt.show()
