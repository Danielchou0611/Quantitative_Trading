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
from phandas.operators import ts_mean, ts_median, normalize
from phandas.backtest import Backtester
from phandas.plot import BacktestPlotter

# 策略參數
symbols = ['BTC', 'ETH', 'SOL', 'XRP', 'BNB', 'DOGE', 'LINK', 'ADA', 'AVAX', 'LTC', 'AAVE', 'SHIB', 'HBAR']
timeframe = '1h'
# 為了從 2026-01-01 開始有信號，數據獲取會自動提前以滿足回溯期
start_date = '2025-01-01' 

print(f"Step 1: Fetching 1h data starting from {start_date}...")
panel = fetch_data(symbols=symbols, timeframe=timeframe, start_date=start_date)

# 2. 提取數據
open_p = panel['open']
close_p = panel['close']

print("Step 2: Calculating Strategy 3 Alpha...")
# 公式: ts_mean(normalize(ts_median(close/open - 1, 300)), 500)
returns_factor = (close_p / open_p) - 1
median_300 = ts_median(returns_factor, 300)
norm_median = normalize(median_300)
alpha = ts_mean(norm_median, 500)

alpha.name = "Strategy 3: Median-Mean Reversion"

print(f"Step 3: Running phandas Backtester (1h)...")
bt = Backtester(
    entry_price_factor=close_p,
    strategy_factor=alpha,
    transaction_cost=0.0003,
    initial_capital=1000000,
    neutralization="market"
)
bt.run()

# 手動計算指標以確保圖表顯示
print("Calculating performance metrics...")
bt.calculate_metrics()

print("\nStep 4: Generating professional plots...")
plotter = BacktestPlotter(bt)

with patch('matplotlib.pyplot.show'):
    plotter.plot_equity(figsize=(16, 10))
    # 【修正】將圖片儲存在腳本所在的同一個目錄下
    save_path = os.path.join(script_dir, 'strategy_3_result.png')
    plt.savefig(save_path, dpi=300, bbox_inches='tight')

print(f"Results saved to {save_path}")

# 打印指標摘要
if hasattr(bt, 'metrics') and bt.metrics:
    print(f"\n--- Strategy 3 Performance Metrics (from 2026-01-01) ---")
    for k, v in bt.metrics.items():
        if k != 'drawdown_periods' and isinstance(v, (float, int)):
            print(f"{k}: {v:.4f}")
