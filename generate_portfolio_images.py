"""
generate_portfolio_images.py — 產生作品集用的三張圖表（修正版 v2）

放到專案根目錄，跑一次產生 docs/images/ 下的三張 PNG。

修正內容：
  - 圖 1：含 SNDK 的 15 檔平均，跟 README 的 +114.48% 一致
  - 圖 2：拿掉「Ideal direction」箭頭，保持簡潔
  - 圖 3：改用真實的 Backtrader 跑 TSLA backtest 拿資產曲線

跑法：
    python generate_portfolio_images.py

需要 matplotlib + backtrader（專案本來就有）。
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from dotenv import load_dotenv
load_dotenv(ROOT / "config" / ".env")

import matplotlib
matplotlib.use("Agg")  # 不開 GUI 視窗
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd

OUTPUT_DIR = ROOT / "docs" / "images"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# 實驗資料（跟 README 完全一致）
# ============================================================
# 注意：這裡含 SNDK，平均跟 README +114.48% 一致
RESULTS = [
    # ticker, 4a, 4b, 4c, B&H
    ("TSLA",  72.65,   26.98,   39.56,   -12.75),
    ("GOOGL",  -8.91,   23.60,   -1.69,  118.80),
    ("PLTR",  67.57,   27.70,    7.37,  591.10),
    ("MU",    67.68,   98.29,   42.96,  339.26),
    ("SNDK", 507.98,  497.29,  391.97, 2605.75),
    ("NVDA", 208.15,    1.96,  -15.12,  526.24),
    ("TSM",   81.87,    0.54,   -5.57,  187.73),
    ("RKLB", 399.75,  370.32,  269.33,  457.79),
    ("SOFI",  20.37,   -5.83,    4.56,    3.44),
    ("AAPL",  30.51,   19.64,    9.22,   43.11),
    ("META",  97.33,  -11.47,  -29.25,   86.05),
    ("MSFT",  22.86,   14.38,  -12.02,   10.79),
    ("AMD",   27.12,   52.70,   59.96,   63.10),
    ("AVGO", 112.14,   52.33,   49.50,  460.14),
    ("CRWD",  10.05,  -15.98,  -14.66,   91.11),
]

# 配色
COLOR_4A = "#2E7D32"    # 深綠
COLOR_4B = "#F57F17"    # 橙
COLOR_4C = "#1565C0"    # 藍
COLOR_BH = "#9E9E9E"    # 灰


# ============================================================
# 圖 1：三方報酬對照條形圖（15 檔，含 SNDK）
# ============================================================
def plot_returns_comparison():
    """
    畫 14 檔（排除 SNDK）的報酬對照。
    SNDK 2025-02 才從 WDC 分拆上市，只有 14 個月資料，
    無法跟其他 14 檔的 4 年資料公平對比。
    排除它是為了視覺清晰，不是隱藏資料；
    15 檔含 SNDK 的平均值仍在文字中保留。
    """
    # 排除 SNDK
    results = [r for r in RESULTS if r[0] != "SNDK"]

    tickers = [r[0] for r in results]
    returns_4a = [r[1] for r in results]
    returns_4b = [r[2] for r in results]
    returns_4c = [r[3] for r in results]
    returns_bh = [r[4] for r in results]

    x = np.arange(len(tickers))
    width = 0.2

    fig, ax = plt.subplots(figsize=(15, 7))

    ax.bar(x - 1.5 * width, returns_4a, width,
           label="4a Baseline (pure technical)", color=COLOR_4A)
    ax.bar(x - 0.5 * width, returns_4b, width,
           label="4b + Sentiment filter", color=COLOR_4B)
    ax.bar(x + 0.5 * width, returns_4c, width,
           label="4c + Regime sizer", color=COLOR_4C)
    ax.bar(x + 1.5 * width, returns_bh, width,
           label="Buy & Hold", color=COLOR_BH)

    ax.set_xlabel("Ticker", fontsize=12)
    ax.set_ylabel("Cumulative Return (%)", fontsize=12)
    ax.set_title(
        "4-Year Cross-Bear-Market Backtest (2022-01 to 2026-04)\n"
        "14 US Large-Cap Stocks (SNDK excluded — IPO'd in 2025, insufficient history)",
        fontsize=13, fontweight="bold", pad=15,
    )
    ax.set_xticks(x)
    ax.set_xticklabels(tickers, rotation=45, ha="right")
    ax.axhline(0, color="black", linewidth=0.5)
    ax.legend(loc="upper left", fontsize=10)
    ax.grid(axis="y", alpha=0.3)

    # 平均值：只算這 14 檔（跟圖上一致）
    avg_4a = np.mean(returns_4a)
    avg_4b = np.mean(returns_4b)
    avg_4c = np.mean(returns_4c)
    avg_bh = np.mean(returns_bh)

    # 但也要把「15 檔含 SNDK」的平均列出來，以便讀者交叉驗證
    full_4a = np.mean([r[1] for r in RESULTS])
    full_4b = np.mean([r[2] for r in RESULTS])
    full_4c = np.mean([r[3] for r in RESULTS])
    full_bh = np.mean([r[4] for r in RESULTS])

    textstr = (
        f"Average returns (14 stocks shown):\n"
        f"  4a Baseline:  +{avg_4a:.2f}%\n"
        f"  4b +Sent:     +{avg_4b:.2f}%\n"
        f"  4c +Regime:   +{avg_4c:.2f}%\n"
        f"  Buy & Hold:   +{avg_bh:.2f}%\n"
        f"\n"
        f"15 stocks incl. SNDK:\n"
        f"  4a Baseline:  +{full_4a:.2f}%\n"
        f"  4b +Sent:     +{full_4b:.2f}%\n"
        f"  4c +Regime:   +{full_4c:.2f}%\n"
        f"  Buy & Hold:   +{full_bh:.2f}%"
    )
    ax.text(1.02, 0.97, textstr, transform=ax.transAxes,
            fontsize=9, verticalalignment="top", horizontalalignment="left",
            family="monospace",
            bbox=dict(boxstyle="round,pad=0.5", facecolor="white",
                      edgecolor="gray", alpha=0.9))

    plt.tight_layout(rect=[0, 0, 0.80, 1])  # 右側留 20% 給文字框
    out = OUTPUT_DIR / "returns_comparison.png"
    plt.savefig(out, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"✅ Saved: {out}")


# ============================================================
# 圖 2：報酬 vs 回撤的權衡（拿掉「Ideal direction」箭頭）
# ============================================================
def plot_return_vs_drawdown():
    strategies = ["4a Baseline", "4b +Sentiment", "4c +Regime"]
    avg_returns = [114.48, 76.83, 53.07]
    avg_drawdowns = [34.26, 34.26, 23.53]
    colors = [COLOR_4A, COLOR_4B, COLOR_4C]

    fig, ax = plt.subplots(figsize=(9, 7))

    for i, (name, ret, dd, color) in enumerate(
        zip(strategies, avg_returns, avg_drawdowns, colors)
    ):
        ax.scatter(dd, ret, s=400, color=color, edgecolor="black",
                   linewidth=1.5, zorder=3, label=name)
        ax.annotate(
            f"  {name}\n  Return: +{ret:.1f}%\n  Drawdown: -{dd:.1f}%",
            xy=(dd, ret),
            xytext=(dd + 0.5, ret + 3),
            fontsize=10, fontweight="bold",
        )

    ax.set_xlabel("Average Max Drawdown (%)", fontsize=12)
    ax.set_ylabel("Average 4-Year Return (%)", fontsize=12)
    ax.set_title(
        "Return vs Drawdown Trade-off\n"
        "4c reduces drawdown by 10.74pp but sacrifices 61pp of return",
        fontsize=13, fontweight="bold", pad=15,
    )
    ax.set_xlim(15, 40)
    ax.set_ylim(30, 140)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    out = OUTPUT_DIR / "return_vs_drawdown.png"
    plt.savefig(out, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"✅ Saved: {out}")


# ============================================================
# 圖 3：TSLA 熊市案例 — 用真實 Backtrader 跑
# ============================================================
def plot_tsla_bear_case_real():
    """
    用 Backtrader 真正跑一次 TSLA 的 4a 策略，抓出每日資產變化。
    """
    try:
        import backtrader as bt
        from pipeline.db import get_connection, load_prices
        from engine.strategies.breakout import BreakoutStrategy
    except ImportError as e:
        print(f"⚠️  Import failed: {e}")
        print("   Skipping TSLA case chart.")
        return

    # 1. 拿 TSLA 價格
    conn = get_connection()
    df = load_prices(conn, "TSLA")
    conn.close()

    if df.empty:
        print("⚠️  No TSLA price data — skipping")
        return

    # 只取 2022-01-01 之後
    df = df[df.index >= "2022-01-01"].copy()
    if df.empty:
        print("⚠️  No TSLA data after 2022 — skipping")
        return

    print(f"  Loaded {len(df)} days of TSLA data ({df.index[0].date()} ~ {df.index[-1].date()})")

    # 2. 寫一個自訂 observer 記錄每日 equity
    # 最簡單的做法：用 bt.analyzers.Analyzer 收集
    class EquityRecorder(bt.Analyzer):
        """記錄每一天的 portfolio value"""
        def start(self):
            self.equity = []
            self.dates = []

        def next(self):
            self.equity.append(self.strategy.broker.getvalue())
            self.dates.append(self.strategy.data.datetime.date(0))

    # 3. 跑 4a baseline backtest
    cerebro = bt.Cerebro()
    cerebro.broker.setcash(100000)
    cerebro.broker.setcommission(commission=0.001)

    # 只餵 OHLCV（不需要 sentiment feed，因為 4a baseline 不用）
    data = bt.feeds.PandasData(dataname=df[["open", "high", "low", "close", "volume"]])
    cerebro.adddata(data, name="TSLA")

    cerebro.addstrategy(
        BreakoutStrategy,
        entry_period=20,
        exit_period=10,
        stop_loss_pct=0.08,
        trailing_pct=0.15,
    )
    cerebro.addanalyzer(EquityRecorder, _name="equity")

    print("  Running 4a baseline backtest on TSLA...")
    results = cerebro.run()
    recorder = results[0].analyzers.equity

    baseline_dates = recorder.dates
    baseline_equity = recorder.equity
    final_value = baseline_equity[-1]
    final_return_pct = (final_value / 100000 - 1) * 100

    print(f"  4a final: ${final_value:,.0f} ({final_return_pct:+.2f}%)")

    # 4. 計算 Buy & Hold 資產曲線
    initial_capital = 100000.0
    bh_shares = initial_capital / df["close"].iloc[0]
    bh_equity = bh_shares * df["close"]
    bh_final_pct = (bh_equity.iloc[-1] / initial_capital - 1) * 100
    print(f"  B&H final: ${bh_equity.iloc[-1]:,.0f} ({bh_final_pct:+.2f}%)")

    # 5. 畫圖
    fig, ax = plt.subplots(figsize=(12, 6))

    # B&H — 用整個 df 的日期
    ax.plot(df.index, bh_equity, label=f"Buy & Hold (ended {bh_final_pct:+.2f}%)",
            color=COLOR_BH, linewidth=2, alpha=0.85)

    # 4a baseline — 用 backtrader 記錄的日期
    ax.plot(baseline_dates, baseline_equity,
            label=f"4a Baseline (ended {final_return_pct:+.2f}%)",
            color=COLOR_4A, linewidth=2.5)

    # 初始資金線
    ax.axhline(initial_capital, color="black", linestyle="--",
               linewidth=0.8, alpha=0.5, label="Initial capital ($100k)")

    # 標註 2022 熊市低點
    bear_low_idx = df["close"].idxmin()
    ax.axvline(bear_low_idx, color="red", linestyle=":", linewidth=1, alpha=0.5)
    y_top = ax.get_ylim()[1]
    ax.text(bear_low_idx, y_top * 0.96,
            " 2022 bear market low",
            fontsize=9, color="red", alpha=0.7, va="top")

    ax.set_xlabel("Date", fontsize=12)
    ax.set_ylabel("Portfolio Value ($)", fontsize=12)
    ax.set_title(
        f"TSLA Case Study: Cross-Bear-Market Comparison\n"
        f"Buy & Hold loses {abs(bh_final_pct):.2f}% over 4 years, "
        f"while 4a baseline gains {final_return_pct:.2f}%",
        fontsize=13, fontweight="bold", pad=15,
    )
    ax.legend(loc="upper left", fontsize=10)
    ax.grid(True, alpha=0.3)
    ax.yaxis.set_major_formatter(
        plt.FuncFormatter(lambda x, _: f"${x/1000:.0f}k")
    )

    plt.tight_layout()
    out = OUTPUT_DIR / "tsla_bear_market_case.png"
    plt.savefig(out, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"✅ Saved: {out}")


# ============================================================
# Main
# ============================================================
if __name__ == "__main__":
    print("🎨 Generating portfolio images...\n")

    print("[1/3] Returns comparison...")
    plot_returns_comparison()
    print()

    print("[2/3] Return vs Drawdown...")
    plot_return_vs_drawdown()
    print()

    print("[3/3] TSLA bear market case (running real Backtrader)...")
    plot_tsla_bear_case_real()
    print()

    print(f"✅ All images saved to: {OUTPUT_DIR}")
    print("\nTo embed in README, add:")
    print("  ![Returns Comparison](docs/images/returns_comparison.png)")
    print("  ![Return vs Drawdown](docs/images/return_vs_drawdown.png)")
    print("  ![TSLA Case Study](docs/images/tsla_bear_market_case.png)")