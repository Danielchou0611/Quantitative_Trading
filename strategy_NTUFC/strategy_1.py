import sys
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from unittest.mock import patch

# 穩健導入 phandas：無論從哪裡執行都能正確定位
script_dir = os.path.dirname(os.path.abspath(__file__))
phandas_path = os.path.abspath(os.path.join(script_dir, '..', 'phandas'))
sys.path.append(phandas_path)

from phandas.data import fetch_data
from phandas.operators import ts_rank, ts_mean, normalize
from phandas.backtest import Backtester
from phandas.plot import BacktestPlotter

# 策略參數
symbols = ['BTC', 'ETH', 'SOL', 'XRP', 'BNB', 'DOGE', 'LINK', 'ADA', 'AVAX', 'LTC', 'AAVE', 'SHIB', 'HBAR']
timeframe = '1h'
lookback = 512
start_date = '2025-01-01'

print("Step 1: Fetching data using phandas...")
panel = fetch_data(symbols=symbols, timeframe=timeframe, start_date=start_date)

# 2. 提取 Volume 和 Close
volume = panel['volume']
close = panel['close']

print("Step 2: Calculating Strategy Alpha...")
rank_vol = ts_rank(volume, lookback)
norm_rank = normalize(rank_vol)
alpha = ts_mean(norm_rank, lookback)
alpha.name = "Strategy 1: Volume Rank"

print("Step 3: Running phandas Backtester...")
bt = Backtester(
    entry_price_factor=close,
    strategy_factor=alpha,
    transaction_cost=0.0003,
    initial_capital=1000000,
    neutralization="market"
)
bt.run()
bt.calculate_metrics()

print("\nStep 4: Generating professional plots...")
plotter = BacktestPlotter(bt)
with patch('matplotlib.pyplot.show'):
    plotter.plot_equity(figsize=(16, 10))
    # 【修正】將圖片儲存在腳本所在的同一個目錄下
    save_path = os.path.join(script_dir, 'strategy_1_result.png')
    plt.savefig(save_path, dpi=300, bbox_inches='tight')

print(f"Results saved to {save_path}")

# 打印回測指標
if hasattr(bt, 'metrics') and bt.metrics:
    print(f"\n--- Strategy 1 Performance Metrics ---")
    for key, value in bt.metrics.items():
        if key != 'drawdown_periods' and isinstance(value, (float, int)):
            print(f"{key}: {value:.4f}")
