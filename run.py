import os
import binance_data_fetch as bf

SYMBOL = 'ETHUSDT'
INTERVAL = '5m'
RAW_SAVE_DIR = 'D:/Research/crypto/historical_data/binance/' + SYMBOL + '/'
TSLAB_SAVE_DIR = 'D:/Research/crypto/historical_data/tslab/' + SYMBOL + '/'
RESULT_DIR = 'D:/Research/crypto/historical_data/tslab/merged/'

if not os.path.exists(RAW_SAVE_DIR):
    os.makedirs(RAW_SAVE_DIR)

if not os.path.exists(TSLAB_SAVE_DIR):
    os.makedirs(TSLAB_SAVE_DIR)

if not os.path.exists(RESULT_DIR):
    os.makedirs(RESULT_DIR)

print("Downloading data...")
bf.binance_data_fetch(SYMBOL, INTERVAL, RAW_SAVE_DIR)

print("Converting CSV files...")
bf.csv2tslab(RAW_SAVE_DIR, TSLAB_SAVE_DIR)

print("Merging CSV files...")
bf.merge_csv(TSLAB_SAVE_DIR, RESULT_DIR, SYMBOL + '.csv')

print("Done!")
