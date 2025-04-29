import sys

import pandas as pd

from finrl.meta.preprocessor.yahoodownloader import YahooDownloader

sys.path.append("../FinRL")

import itertools

from finrl import config_tickers
import os


def download_file():
    TRAIN_START_DATE = '2009-01-01'
    TRADE_END_DATE = '2021-10-31'
    if os.path.exists("./datasets/yahoo.csv"):
        df = pd.read_csv('./datasets/yahoo.csv')
    else:
        print("download")
        try:
            df = YahooDownloader(start_date=TRAIN_START_DATE,
                                 end_date=TRADE_END_DATE,
                                 ticker_list=config_tickers.DOW_30_TICKER).fetch_data()
        except:
            df = pd.read_csv('./datasets/yahoo.csv')
    return df


def process_data(processed):
    list_ticker = processed["tic"].unique().tolist()
    list_date = list(pd.date_range(processed['date'].min(), processed['date'].max()).astype(str))
    combination = list(itertools.product(list_date, list_ticker))

    processed_full = pd.DataFrame(combination, columns=["date", "tic"]).merge(processed, on=["date", "tic"], how="left")
    processed_full = processed_full[processed_full['date'].isin(processed['date'])]
    processed_full = processed_full.sort_values(['date', 'tic'])

    processed_full = processed_full.fillna(0)
    # 设置 pandas 显示选项
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', None)
    print(processed_full.sort_values(['date', 'tic'], ignore_index=True).head(10))


if __name__ == '__main__':
    # check_and_make_directories([DATA_SAVE_DIR, TRAINED_MODEL_DIR, TENSORBOARD_LOG_DIR, RESULTS_DIR])
    # df = download_file()
    # print(config_tickers.DOW_30_TICKER)
    # df.shape
    # df.sort_values(['date', 'tic'], ignore_index=True).head()

    processed = pd.read_csv('./datasets/processed.csv')
    process_data(processed)
