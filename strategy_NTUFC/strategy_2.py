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
from phandas.operators import ts_scale, ts_sum, rank, ts_rank
from phandas.backtest import Backtester
from phandas.plot import BacktestPlotter

# 策略參數
symbols = ['BTC', 'ETH', 'SOL', 'XRP', 'BNB', 'DOGE', 'LINK', 'ADA', 'AVAX', 'LTC', 'AAVE', 'SHIB', 'HBAR']
timeframe = '1h'
start_date = '2025-01-01'

print(f"Step 1: Fetching 1h data for {len(symbols)} symbols...")
panel = fetch_data(symbols=symbols, timeframe=timeframe, start_date=start_date, sources=['binance', 'vwap'])

# 2. 提取數據
low = panel['low']
close = panel['close']

if 'vwap' in panel.columns:
    vwap = panel['vwap']
    print("Using VWAP from data source.")
else:
    print("VWAP not found, using Close as proxy.")
    vwap = close

print("Step 2: Calculating Strategy 2 Alpha...")
# 公式: ts_sum(rank((ts_scale(vwap, 512) + ts_scale(low, 512))), 72)
term1 = ts_scale(vwap, 512)
term2 = ts_scale(low, 512)
combined = term1 + term2
ranked = rank(combined)
alpha = ts_sum(ranked, 72)

alpha.name = "Strategy 2: VWAP/Low Scale"

print("Step 3: Running phandas Backtester (1h)...")
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
    save_path = os.path.join(script_dir, 'strategy_2_result.png')
    plt.savefig(save_path, dpi=300, bbox_inches='tight')

print(f"Results saved to {save_path}")

# 打印指標摘要
if hasattr(bt, 'metrics') and bt.metrics:
    print(f"\n--- Strategy 2 Performance Metrics ---")
    for k, v in bt.metrics.items():
        if k != 'drawdown_periods' and isinstance(v, float):
            print(f"{k}: {v:.4f}")
