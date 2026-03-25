"""
utils.py — shared constants and functions for the India equity portfolio project.
All notebooks import from here to guarantee consistent parameters.
"""

import numpy as np
import pandas as pd

# ── Time-period constants ────────────────────────────────────────────────────
PERIODS_PER_YEAR = 12          # monthly data → 12 periods per year
RF_ANNUAL        = 0.065       # 6.5 % p.a. — approximate Indian 91-day T-bill yield
RF_MONTHLY       = RF_ANNUAL / PERIODS_PER_YEAR   # risk-free rate per period

# ── Paths ────────────────────────────────────────────────────────────────────
DATA_DIR     = "../data"
ANALYSIS_DIR = "../analysis"
CHARTS_DIR   = "../charts"

# ── Matplotlib style ─────────────────────────────────────────────────────────
import matplotlib.pyplot as plt
import matplotlib as mpl

def apply_style():
    plt.style.use("seaborn-v0_8-whitegrid")
    mpl.rcParams.update({
        "figure.dpi"       : 150,
        "font.family"      : "serif",
        "axes.titleweight" : "bold",
        "axes.titlesize"   : 13,
        "axes.labelsize"   : 11,
        "legend.fontsize"  : 9,
        "xtick.labelsize"  : 9,
        "ytick.labelsize"  : 9,
    })

# ── Return / risk helpers ─────────────────────────────────────────────────────

def annualise_return(r_monthly: float) -> float:
    """Compound a mean monthly return to an annualised figure."""
    return (1 + r_monthly) ** PERIODS_PER_YEAR - 1

def annualise_vol(vol_monthly: float) -> float:
    """Scale monthly volatility to annual using √12."""
    return vol_monthly * np.sqrt(PERIODS_PER_YEAR)

def portfolio_return(weights: np.ndarray, mean_returns: np.ndarray) -> float:
    """Expected monthly portfolio return."""
    return float(np.dot(weights, mean_returns))

def portfolio_volatility(weights: np.ndarray, cov_matrix: np.ndarray) -> float:
    """Monthly portfolio volatility (std dev)."""
    return float(np.sqrt(weights @ cov_matrix @ weights))

def sharpe_ratio(weights: np.ndarray,
                 mean_returns: np.ndarray,
                 cov_matrix: np.ndarray,
                 rf: float = RF_MONTHLY) -> float:
    """
    Monthly Sharpe ratio using the correct monthly rf.
    To annualise multiply by √12.
    """
    r = portfolio_return(weights, mean_returns)
    v = portfolio_volatility(weights, cov_matrix)
    if v == 0:
        return 0.0
    return (r - rf) / v

def neg_sharpe(weights: np.ndarray,
               mean_returns: np.ndarray,
               cov_matrix: np.ndarray,
               rf: float = RF_MONTHLY) -> float:
    """Objective for scipy.optimize.minimize (minimise → maximise Sharpe)."""
    return -sharpe_ratio(weights, mean_returns, cov_matrix, rf)

def beta(port_returns: pd.Series, market_returns: pd.Series) -> float:
    """OLS beta of portfolio against market."""
    cov = np.cov(port_returns, market_returns, ddof=1)[0, 1]
    var = np.var(market_returns, ddof=1)
    return cov / var if var != 0 else np.nan

def jensen_alpha(port_returns: pd.Series,
                 market_returns: pd.Series,
                 b: float,
                 rf: float = RF_MONTHLY) -> float:
    """Jensen's alpha (monthly)."""
    return port_returns.mean() - (rf + b * (market_returns.mean() - rf))

def treynor_ratio(port_returns: pd.Series,
                  b: float,
                  rf: float = RF_MONTHLY) -> float:
    """Treynor ratio (monthly)."""
    return (port_returns.mean() - rf) / b if b != 0 else np.nan

def sortino_ratio(port_returns: pd.Series,
                  rf: float = RF_MONTHLY) -> float:
    """Sortino ratio using downside deviation."""
    excess  = port_returns - rf
    downside = excess[excess < 0]
    dd_std  = np.sqrt((downside ** 2).mean()) if len(downside) > 0 else np.nan
    return excess.mean() / dd_std if dd_std else np.nan

def max_drawdown(port_returns: pd.Series) -> float:
    """Maximum drawdown from cumulative wealth series."""
    wealth = (1 + port_returns).cumprod()
    peak   = wealth.cummax()
    dd     = (wealth - peak) / peak
    return float(dd.min())

def calmar_ratio(port_returns: pd.Series) -> float:
    """Calmar ratio: annualised return / |max drawdown|."""
    ann_ret = annualise_return(port_returns.mean())
    mdd     = abs(max_drawdown(port_returns))
    return ann_ret / mdd if mdd != 0 else np.nan
