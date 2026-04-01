# Crypto Strategy Backtesting (NTUFC)

這是一個基於 `phandas` 回測框架的加密貨幣多幣種策略回測專案。

## 專案結構

建議的目錄結構如下，以確保腳本能正確引用 `phandas` 套件：

```text
Quantitative/
├── phandas/             # phandas 回測框架核心套件
└── strategy_NTUFC/      # 本專案目錄
    ├── strategy_1.py    # 策略 1：成交量排名策略
    ├── strategy_2.py    # 策略 2：VWAP/Low 標準化加總策略
    ├── strategy_3.py    # 策略 3：收益中位數均值回歸策略
    └── README.md
```

## 環境

已安裝以下 Python library：
- `pandas`
- `numpy`
- `ccxt`
- `matplotlib`

## 策略說明

本專案包含三個量化策略，針對 13 個主要幣種（BTC, ETH, SOL, XRP, BNB, DOGE, LINK, ADA, AVAX, LTC, AAVE, SHIB, HBAR）進行回測：

### 1. Strategy 1: Volume Rank
- **公式**: `ts_mean(normalize(ts_rank(volume, 512)), 512)`
- **邏輯**: 捕捉成交量的相對變化，透過 512 週期的滾動排名與標準化，尋找交易量異常帶來的動能機會。
- **週期**: 1h

### 2. Strategy 2: VWAP/Low Scale
- **公式**: `ts_sum(rank(ts_scale(vwap, 512) + ts_scale(low, 512)), 72)`
- **邏輯**: 結合 VWAP（成交量加權平均價）與最低價的標準化數值，進行橫截面排名後加總，旨在捕捉價格與價量的協同效應。
- **週期**: 1h

### 3. Strategy 3: Median-Mean Reversion
- **公式**: `ts_mean(normalize(ts_median(close/open - 1, 300)), 500)`
- **邏輯**: 使用日內漲跌幅的中位數進行長週期平滑，透過標準化尋找市場超漲或超跌的均值回歸機會。
- **週期**: 1h

## 執行方式

從 `Quantitative` 父目錄執行任何策略腳本：

```bash
python .\strategy_NTUFC\strategy_1.py
python .\strategy_NTUFC\strategy_2.py
python .\strategy_NTUFC\strategy_3.py
```

## 產出績效結果

執行完成後，會自動在 `strategy_NTUFC` 目錄下生成對應的結果圖片：
- `strategy_1_result.png`
- `strategy_2_result.png`
- `strategy_3_result.png`

