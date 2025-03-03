import numpy as np
import pandas as pd

# Install and import opendatasets

# Read the CSV file
df = pd.read_csv('prices-split-adjusted.csv')

# Display first few rows
# print(df.head())
#
# check1 Q1: How many different stocks are there?
stock_set = set(df['symbol'])
print(len(stock_set))

# check1 Q2: What is the average closing price for EBAY stock?
s_sum=0
nums=0
for i in range(len(df)):
    if df['symbol'][i]=='EBAY':
        s_sum+=df['close'][i]
        nums+=1
print(s_sum/nums)

# check1 Q3: What is the std of the open price?
std=np.std(df["open"])
print(std)


# check1 Q4: How many entries are in this table?
print(len(df))

# check1 Q5: How many records from the WLTL stock have a volume of larger than 2 million?
wltl_nums=0
for i in range(len(df)):
    if df['symbol'][i]=='WLTW' and df['volume'][i]>2000000:
        wltl_nums+=1
print(wltl_nums)

# check1 Q6: How many stocks had a closing price higher than their opening price?
close_list=list()
for i in range(len(df)):
    if df['close'][i]>df['open'][i]:
        close_list.append(df['symbol'][i])
print(len(close_list))
