# Portfolio Construction and Performance Evaluation
## A Comparative Study of Traditional and Modern Approaches

This repository contains the full quantitative pipeline for the research project
"A Comparative Study of Traditional and Modern Approaches to Portfolio Construction
and Performance Evaluation", submitted as a PGDM Finance Specialisation project at
S.P. Mandali's Welingkar Institute of Management Development & Research, Mumbai.

The project applies Markowitz Mean-Variance Optimization to a universe of nine
large-cap Indian equities over the period January 2019 to March 2026, comparing
an equal-weighted traditional portfolio against two optimized portfolios: Maximum
Sharpe Ratio and Minimum Variance.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Repository Structure](#repository-structure)
3. [Asset Universe](#asset-universe)
4. [Pipeline Architecture](#pipeline-architecture)
5. [Notebook Reference](#notebook-reference)
   - [0 - Data Aggregator](#0--data-aggregator)
   - [1 - Returns Generator](#1--returns-generator)
   - [2 - Portfolio Construction](#2--portfolio-construction)
   - [3 - Efficient Frontier](#3--efficient-frontier)
   - [4 - Performance Metrics](#4--performance-metrics)
   - [5 - Visualisation](#5--visualisation)
   - [6 - Risk-Adjusted Metrics vs Nifty 50](#6--risk-adjusted-metrics-vs-nifty-50)
   - [7 - Portfolio Weights](#7--portfolio-weights)
6. [Variables Reference](#variables-reference)
   - [Global Constants](#global-constants)
   - [Per-Asset Variables](#per-asset-variables)
   - [Matrix Variables](#matrix-variables)
   - [Portfolio Construction Variables](#portfolio-construction-variables)
   - [Portfolio-Level Output Variables](#portfolio-level-output-variables)
   - [CAPM Variables](#capm-variables)
   - [Monte Carlo Variables](#monte-carlo-variables)
7. [Mathematical Foundations](#mathematical-foundations)
8. [Key Results](#key-results)
9. [Limitations](#limitations)
10. [Dependencies](#dependencies)
11. [Reproducing the Analysis](#reproducing-the-analysis)

---

## Project Overview

The central question this codebase answers is whether systematic mean-variance
optimization produces meaningfully better risk-adjusted investment outcomes than
naive equal-weight diversification, when both strategies are applied to the same
asset universe under the same conditions.

Three portfolios are constructed and evaluated:

- **Equal Weight** — each of the 9 assets receives an identical 11.11% allocation.
  This is the traditional passive baseline. No statistical inputs are considered.

- **Maximum Sharpe Ratio** — weights are determined by numerical optimization,
  maximizing return per unit of risk (the Sharpe ratio). This represents the
  modern active approach.

- **Minimum Variance** — weights are determined by minimizing total portfolio
  volatility regardless of return. This represents the most risk-averse position
  on the efficient frontier.

All three portfolios are evaluated using the same set of risk-adjusted performance
metrics: Sharpe ratio, Treynor ratio, Jensen's Alpha, Sortino ratio, maximum
drawdown, and Calmar ratio.

---

## Repository Structure

```
project-root/
│
├── data/                          Raw monthly price CSVs (one per ticker)
│   ├── BRTI Historical Data.csv
│   ├── EICH Historical Data.csv
│   ├── HDBK Historical Data.csv
│   ├── HLL Historical Data.csv
│   ├── LART Historical Data.csv
│   ├── RELI Historical Data.csv
│   ├── SUN Historical Data.csv
│   ├── TISC Historical Data.csv
│   ├── TITN Historical Data.csv
│   └── Nifty 50 Historical Data.csv
│
├── analysis/                      Intermediate and final outputs (auto-generated)
│   ├── india_equity_prices.csv
│   ├── india_equity_returns.csv
│   ├── india_equity_log_returns.csv
│   ├── india_covariance_matrix.csv
│   ├── india_correlation_matrix.csv
│   ├── asset_summary_statistics.csv
│   ├── portfolio_weights.csv
│   ├── portfolio_summary.csv
│   ├── portfolio_simulations.csv
│   ├── efficient_frontier.csv
│   ├── portfolio_metrics.csv
│   ├── portfolio_construction_percent.csv
│   └── risk_adjusted_metrics.csv
│
├── charts/                        All chart outputs (auto-generated)
│
├── utils.py                       Shared constants and helper functions
│
├── 0_data_aggregator.ipynb
├── 1_returns_generator.ipynb
├── 2_portfolio_construction.ipynb
├── 3_efficient_frontier.ipynb
├── 4_performance_metrics.ipynb
├── 5_viz.ipynb
├── 6_risk_adjusted_metrics.ipynb
└── 7_portfolio_weights.ipynb
```

The `analysis/` and `charts/` directories are created automatically when the
notebooks are run. Do not manually edit files in `analysis/` — they are
overwritten on each run.

---

## Asset Universe

Nine large-cap Indian equities were selected to ensure sectoral diversification,
varying volatility profiles, and continuous data availability across the full
sample period.

| Study Ticker | NSE Symbol    | Company                          | Sector                    |
|--------------|---------------|----------------------------------|---------------------------|
| BRTI         | BHARTIARTL    | Bharti Airtel Ltd.               | Telecom                   |
| EICH         | EICHERMOT     | Eicher Motors Ltd.               | Automobile                |
| HDBK         | HDFCBANK      | HDFC Bank Ltd.                   | Banking                   |
| HLL          | HINDUNILVR    | Hindustan Unilever Ltd.          | FMCG                      |
| LART         | LT            | Larsen & Toubro Ltd.             | Infrastructure/Engineering|
| RELI         | RELIANCE      | Reliance Industries Ltd.         | Energy/Conglomerate        |
| SUN          | SUNPHARMA     | Sun Pharmaceutical Industries    | Pharmaceuticals           |
| TISC         | TATASTEEL     | Tata Steel Ltd.                  | Metals                    |
| TITN         | TITAN         | Titan Company Ltd.               | Consumer Discretionary    |

Ticker symbols follow the naming convention used by investing.com, which is the
data source. These differ from official NSE symbols in some cases. This is
deliberate to preserve reproducibility against the original downloaded datasets.

**Sample period:** January 2019 to March 2026 (86 monthly price observations,
yielding 85 return observations after differencing).

The period spans three distinct market phases: pre-pandemic stability (2019),
the COVID-19 market crash and recovery (2020-2021), and the post-pandemic
growth phase (2022-2026).

---

## Pipeline Architecture

The notebooks form a strict sequential pipeline. Each notebook reads from
`analysis/` and writes back to `analysis/`. They must be run in numerical order.

```
data/ (raw CSVs)
    |
    v
[0_data_aggregator]
    |
    v  india_equity_prices.csv
    |
[1_returns_generator]
    |
    v  india_equity_returns.csv
    v  india_covariance_matrix.csv
    v  india_correlation_matrix.csv
    v  asset_summary_statistics.csv
    |
[2_portfolio_construction]
    |
    v  portfolio_weights.csv
    v  portfolio_summary.csv
    |
[3_efficient_frontier]       [4_performance_metrics]
    |                               |
    v  portfolio_simulations.csv    v  portfolio_metrics.csv
    v  efficient_frontier.csv       |
    |                               |
    +---------------+---------------+
                    |
              [5_viz]  [6_risk_adjusted_metrics]  [7_portfolio_weights]
                    |
                    v  charts/
```

Notebooks 5, 6, and 7 are all terminal — they produce final outputs and do not
feed into further notebooks.

---

## Notebook Reference

### 0 — Data Aggregator

**Input:** Individual CSV files in `data/`, one per ticker.  
**Output:** `analysis/india_equity_prices.csv`

Reads each stock's historical price file, extracts the ticker name from the
filename, parses and cleans the `Date` and `Price` columns, and merges all
tickers into a single wide-format matrix indexed by date.

Data cleaning steps applied:
- Column names are stripped of whitespace
- Dates are parsed with `dayfirst=True` to handle the DD/MM/YYYY format from
  investing.com
- Price strings containing commas (e.g. `1,265.54`) are cleaned before casting
  to float
- Files containing "nifty" in the filename are excluded from this notebook and
  handled separately in notebook 6
- An outer join is used during merging so no date history is silently dropped
- Isolated gaps of up to 2 consecutive missing months are forward-filled
- Any rows still containing NaN after forward-filling are dropped

The resulting price matrix contains 86 monthly observations across 9 tickers
with no missing values.

---

### 1 — Returns Generator

**Input:** `analysis/india_equity_prices.csv`  
**Output:** `india_equity_returns.csv`, `india_equity_log_returns.csv`,
`india_covariance_matrix.csv`, `india_correlation_matrix.csv`,
`asset_summary_statistics.csv`

Computes all statistical inputs required for portfolio optimization.

**Simple returns** are computed as:

```
R_t = (P_t - P_{t-1}) / P_{t-1}
```

These are used in all downstream analysis. Simple returns are preferred over
log returns for portfolio optimization because portfolio return is a linear
weighted sum of individual asset simple returns, which simplifies the
optimization math.

**Log returns** are computed as:

```
r_t = ln(P_t / P_{t-1})
```

These are saved for reference and can be used for normality testing, but are
not used in optimization.

**The covariance matrix** is a 9x9 symmetric matrix where each entry `[i, j]`
represents how assets `i` and `j` move together. The diagonal entries are each
asset's own variance. This matrix is the primary risk input to the optimizer.

**The correlation matrix** is the standardized version of the covariance matrix,
where each entry is bounded between -1 and +1. It is used for interpretation
and visualization but the raw covariance matrix is used in optimization.

Summary statistics computed per asset include mean monthly return, monthly
standard deviation, compounded annual return, annualized volatility, individual
Sharpe ratio, skewness, excess kurtosis, and the minimum and maximum monthly
return observed.

---

### 2 — Portfolio Construction

**Input:** `analysis/india_equity_returns.csv`  
**Output:** `analysis/portfolio_weights.csv`, `analysis/portfolio_summary.csv`

This is the core optimization notebook. It constructs all three portfolios.

**Equal-weight portfolio:**
Weight vector is simply `w_i = 1/9` for all 9 assets. No optimization is
performed.

**Maximum Sharpe portfolio:**
Uses `scipy.optimize.minimize` with the SLSQP (Sequential Least Squares
Programming) method. SLSQP is a gradient-based constrained optimization
algorithm suitable for smooth, nonlinear objective functions with equality
and inequality constraints.

The objective function minimized is the negative Sharpe ratio:

```
minimize: -(w · mu - RF_monthly) / sqrt(w^T · cov · w)
```

Subject to:
- `sum(w) = 1` (weights fully invested)
- `w_i >= 0` for all i (no short selling)
- `w_i <= 1` for all i (no leverage per asset)

To mitigate the risk of converging to a local rather than global optimum,
the optimizer is run 50 times from random starting points drawn from a
Dirichlet distribution. The run with the highest Sharpe ratio is kept.

After optimization, tiny negative weights arising from numerical floating
point noise are clipped to zero and the weights are renormalized to sum to 1.

**Minimum Variance portfolio:**
Same optimizer and constraints, but the objective function is portfolio
variance rather than negative Sharpe:

```
minimize: w^T · cov · w
```

This finds the leftmost point on the efficient frontier — the portfolio with
the absolute lowest achievable volatility given the asset universe.

---

### 3 — Efficient Frontier

**Input:** `analysis/india_equity_returns.csv`  
**Output:** `analysis/portfolio_simulations.csv`, `analysis/efficient_frontier.csv`

Produces two complementary representations of the opportunity set.

**Monte Carlo simulation:**
20,000 random portfolios are generated by drawing weight vectors from a
Dirichlet distribution. For each portfolio, return, volatility, and Sharpe
ratio are recorded. This creates the characteristic scatter cloud seen in
efficient frontier charts.

**Exact frontier:**
The true efficient frontier is traced by solving 80 separate optimization
problems, each finding the minimum-volatility portfolio achievable at a
specific target return level. Target returns are evenly spaced between the
lowest and highest individual asset mean returns. The result is a smooth
curve representing the set of Pareto-optimal portfolios.

The Maximum Sharpe portfolio from the Monte Carlo simulation (0.317) differs
slightly from the optimizer result in notebook 2 (0.330) because random
sampling of 20,000 portfolios does not guarantee hitting the exact optimum.
The notebook 2 figure is the authoritative one.

---

### 4 — Performance Metrics

**Input:** `analysis/india_equity_returns.csv`, `analysis/portfolio_weights.csv`  
**Output:** `analysis/portfolio_metrics.csv`

Computes the full set of risk and performance metrics for all three portfolios
against the synthetic market benchmark.

The **synthetic market** is constructed as the equal-weighted average of the
nine asset monthly returns at each point in time:

```
R_market_t = (1/9) * sum(R_i_t)  for i in [BRTI, EICH, ..., TITN]
```

This proxy was chosen because using the Nifty 50 as a benchmark would
introduce a structural mismatch — the portfolio universe contains only 9
stocks, not 50, and the weights differ substantially. The synthetic benchmark
ensures that all CAPM-based metrics are computed within a self-consistent
framework. The limitation this creates (circularity) is acknowledged in the
paper.

Metrics computed: monthly return, annual return, monthly volatility, annual
volatility, monthly Sharpe ratio, annual Sharpe ratio, Sortino ratio, maximum
drawdown, Calmar ratio, beta, Jensen's Alpha, and Treynor ratio.

---

### 5 — Visualisation

**Input:** All files in `analysis/`  
**Output:** All charts in `charts/`

Generates all charts used in the paper: the asset risk-return scatter plot,
average monthly returns bar chart, return distribution histogram, normalized
price performance, covariance and correlation heatmaps, portfolio weight
allocation bar chart, efficient frontier with capital market line, 3D
risk-return-Sharpe scatter plot, and the cumulative returns comparison chart.

No new calculations are performed in this notebook.

---

### 6 — Risk-Adjusted Metrics vs Nifty 50

**Input:** `analysis/india_equity_returns.csv`, `analysis/portfolio_weights.csv`,
`data/Nifty 50 Historical Data.csv`  
**Output:** `analysis/risk_adjusted_metrics.csv`

Recomputes CAPM metrics (Beta, Jensen's Alpha, Treynor ratio) using the actual
Nifty 50 index as the market benchmark instead of the synthetic proxy.

The Nifty data is cleaned using the same price-parsing logic as notebook 0,
and aligned to the portfolio return series using an inner join on dates. Only
dates present in both series are used, preventing NaN contamination.

Note: Due to the sparse overlap between the Nifty CSV and the portfolio date
range, only 7 observations are available in the current dataset. This makes
the Nifty-benchmarked metrics unreliable for inference, which is why the paper
uses the synthetic benchmark. This notebook is provided for completeness and
as a template for future work using a richer Nifty dataset.

---

### 7 — Portfolio Weights

**Input:** `analysis/portfolio_weights.csv`  
**Output:** `analysis/portfolio_construction_percent.csv`, chart in `charts/`

A presentation notebook. Loads the raw weight vectors, converts them to
percentage form rounded to 2 decimal places, verifies that column totals
equal 100%, and generates the portfolio weight allocation bar chart. No new
calculations are performed.

---

## Variables Reference

### Global Constants

Defined in `utils.py` and imported by all notebooks.

| Variable | Value | Description |
|---|---|---|
| `RF_ANNUAL` | 0.065 | Risk-free rate, 6.5% per annum, proxied by the 10-year Indian Government Security yield |
| `RF_MONTHLY` | 0.065 / 12 = 0.005417 | Monthly equivalent of the risk-free rate, used in all monthly Sharpe and CAPM calculations |
| `PERIODS_PER_YEAR` | 12 | Scaling factor for annualization; reflects monthly data frequency |
| `DATA_DIR` | `"data/"` | Path to raw input CSVs |
| `ANALYSIS_DIR` | `"analysis/"` | Path to intermediate and final analytical outputs |
| `CHARTS_DIR` | `"charts/"` | Path to chart outputs |

---

### Per-Asset Variables

Computed in notebook 1. One value per asset.

| Variable | Formula | Description |
|---|---|---|
| `Mean_Monthly` | `mean(R_t)` | Average simple monthly return over the sample period |
| `Std_Monthly` | `std(R_t)` | Standard deviation of monthly returns; measures individual asset volatility |
| `Mean_Annual` | `(1 + Mean_Monthly)^12 - 1` | Compounded annual return; accounts for reinvestment |
| `Std_Annual` | `Std_Monthly × sqrt(12)` | Annualized volatility; scales monthly standard deviation |
| `Sharpe_Annual` | `(Mean_Annual - RF_ANNUAL) / Std_Annual` | Individual asset risk-adjusted return relative to the risk-free rate |
| `Skewness` | — | Degree of asymmetry in the return distribution; negative skew indicates a longer left tail |
| `Kurtosis` | — | Excess kurtosis; positive values indicate fat tails and higher probability of extreme returns than a normal distribution |
| `Min_Monthly` | — | Worst single-month return observed; often coincides with March 2020 |
| `Max_Monthly` | — | Best single-month return observed |

---

### Matrix Variables

Computed in notebook 1. Used as inputs to the optimizer in notebook 2.

| Variable | Dimensions | Description |
|---|---|---|
| `returns` | 85 rows × 9 columns | Simple monthly return for each asset at each time point. The primary dataset for all downstream analysis |
| `log_returns` | 85 × 9 | Natural log returns. Saved for reference; not used in optimization |
| `cov_matrix` | 9 × 9 | Covariance matrix. Entry `[i, j]` measures how assets i and j co-move. Diagonal entries are individual asset variances. This is the risk input to the optimizer |
| `corr_matrix` | 9 × 9 | Correlation matrix. Standardized form of the covariance matrix, bounded between -1 and +1. Used for interpretation and heatmap visualization |
| `mu` | 9 × 1 vector | Vector of mean returns. Shorthand reference used inside the optimizer for `mean_returns` |

---

### Portfolio Construction Variables

Used in notebook 2 during optimization.

| Variable | Description |
|---|---|
| `w` | Weight vector of length 9. Each entry is the fraction of the portfolio allocated to the corresponding asset. Must sum to 1; all entries must be >= 0 |
| `w_equal` | Equal-weight vector: `[1/9, 1/9, 1/9, 1/9, 1/9, 1/9, 1/9, 1/9, 1/9]` |
| `w_opt` | Optimal weight vector produced by the Maximum Sharpe optimizer |
| `w_minvar` | Optimal weight vector produced by the Minimum Variance optimizer |
| `portfolio_return(w, mu)` | `w · mu` — dot product of weights and mean returns. Gives the expected monthly return of the portfolio |
| `portfolio_volatility(w, cov)` | `sqrt(w^T × cov × w)` — square root of the quadratic form. Gives the monthly standard deviation of the portfolio |
| `neg_sharpe(w, mu, cov, RF)` | `-(w · mu - RF) / sqrt(w^T × cov × w)` — the objective function passed to the optimizer. Minimizing this is equivalent to maximizing the Sharpe ratio |
| `constraints` | List of optimizer constraints: (1) weights sum to 1, (2) for Min Variance, a target return equality constraint is added per frontier point |
| `bounds` | Tuple of `(0.0, 1.0)` pairs, one per asset, enforcing the long-only constraint |

---

### Portfolio-Level Output Variables

Computed in notebooks 2 and 4. One value per portfolio.

| Variable | Formula | Description |
|---|---|---|
| `Monthly_Return` | `w · mu` | Expected monthly portfolio return |
| `Annual_Return` | `(1 + Monthly_Return)^12 - 1` | Compounded annual return |
| `Monthly_Vol` | `sqrt(w^T · cov · w)` | Monthly portfolio standard deviation |
| `Annual_Vol` | `Monthly_Vol × sqrt(12)` | Annualized portfolio volatility |
| `Monthly_Sharpe` | `(Monthly_Return - RF_monthly) / Monthly_Vol` | Excess return per unit of total risk, monthly |
| `Annual_Sharpe` | `Monthly_Sharpe × sqrt(12)` | Annualized Sharpe ratio |
| `Sortino_Monthly` | `(Monthly_Return - RF_monthly) / downside_std` | Like Sharpe but the denominator uses only the standard deviation of negative returns, not total volatility |
| `Max_Drawdown` | `max((peak - trough) / peak)` | Largest percentage decline from a portfolio peak to a subsequent trough over the sample period |
| `Calmar` | `Annual_Return / abs(Max_Drawdown)` | Annual return per unit of maximum drawdown; measures return relative to worst-case loss |

---

### CAPM Variables

Computed in notebooks 4 and 6.

| Variable | Formula | Description |
|---|---|---|
| `market` | `returns.mean(axis=1)` | Synthetic market benchmark. At each month, the simple average of all 9 assets' returns. Used in notebook 4 |
| `Beta` | `Cov(R_portfolio, R_market) / Var(R_market)` | Measures how sensitive the portfolio is to market movements. A beta of 1.2 means the portfolio moves 1.2% for every 1% market move |
| `Jensen_Alpha` | `R_portfolio - [RF + Beta × (R_market - RF)]` | The excess return the portfolio earns above the return predicted by CAPM. Positive alpha indicates outperformance relative to the risk taken |
| `Treynor` | `(R_portfolio - RF) / Beta` | Excess return per unit of systematic risk. Unlike the Sharpe ratio, it uses beta rather than total volatility in the denominator, so it rewards diversified portfolios that eliminate unsystematic risk |
| `Beta_Nifty` | Same formula, using Nifty 50 returns as market | Computed in notebook 6 only. Beta relative to the actual index rather than the synthetic proxy |

---

### Monte Carlo Variables

Used in notebook 3.

| Variable | Description |
|---|---|
| `N_SIMS` | 20,000 — the number of random portfolios simulated to approximate the feasible set |
| `w` (random) | At each simulation step, a random weight vector drawn from a Dirichlet distribution. By construction, all weights are positive and sum to 1 |
| `sim` | DataFrame with 20,000 rows. Each row stores the monthly return, monthly volatility, monthly Sharpe, annual return, annual volatility, and annual Sharpe of one random portfolio |
| `target_returns` | Array of 80 evenly spaced return values between the minimum and maximum individual asset mean returns. Used to trace the exact efficient frontier |
| `frontier_df` | DataFrame of up to 80 rows, one per target return level, recording the minimum achievable volatility at that return. Together these points trace the efficient frontier curve |

---

## Mathematical Foundations

**Portfolio Return:**
```
E(R_p) = sum(w_i × E(R_i))  =  w · mu
```

**Portfolio Variance:**
```
sigma_p^2 = sum_i sum_j (w_i × w_j × Cov(R_i, R_j))  =  w^T · cov · w
```

**Sharpe Ratio:**
```
S_p = (E(R_p) - R_f) / sigma_p
```

**Beta:**
```
Beta_p = Cov(R_p, R_m) / Var(R_m)
```

**Jensen's Alpha:**
```
alpha_p = R_p - [R_f + Beta_p × (R_m - R_f)]
```

**Treynor Ratio:**
```
T_p = (R_p - R_f) / Beta_p
```

**Annualization:**
```
Annual_Return = (1 + Monthly_Return)^12 - 1
Annual_Vol    = Monthly_Vol × sqrt(12)
Annual_Sharpe = Monthly_Sharpe × sqrt(12)
```

---

## Key Results

| Portfolio | Monthly Return | Annual Return | Annual Sharpe | Jensen Alpha | Treynor |
|---|---|---|---|---|---|
| Equal Weight | 1.66% | 21.81% | 0.793 | 0.00% | 1.12% |
| Max Sharpe | 2.25% | 30.60% | 1.143 | 0.71% | 1.91% |
| Min Variance | 1.23% | 15.85% | 0.597 | -0.08% | 1.00% |

Cumulative returns over the full sample period (2019 to early 2026):

- Max Sharpe portfolio: approximately 500%
- Equal Weight portfolio: approximately 270%
- Min Variance portfolio: approximately 170%

The Max Sharpe portfolio achieves the highest cumulative return and the best
risk-adjusted metrics across all measures. The Minimum Variance portfolio
delivers the lowest volatility as intended, at the cost of lower returns.

---

## Limitations

**Synthetic benchmark circularity.** The proxy market portfolio is constructed
from the same nine assets used to build the portfolios being evaluated. Any
portfolio drawn from this universe will naturally correlate highly with the
benchmark, which inflates beta estimates and makes Jensen's Alpha less
interpretable. This was a deliberate design choice given the restricted asset
universe, and is discussed in the paper.

**No transaction costs.** The analysis assumes frictionless trading with no
brokerage, impact costs, or taxes. Real-world implementation would reduce
realized returns, particularly for the optimized portfolio which requires
periodic rebalancing.

**Static weights.** Portfolio weights are computed once from the full sample
and held fixed. In practice, a rolling or dynamic optimization would be used,
which would also expose the model to estimation error accumulation over time.

**Estimation error sensitivity.** Mean-variance optimization is known to be
sensitive to small errors in expected return inputs. The optimized weights
(e.g., 56% in a single asset) reflect this concentration risk, which would be
mitigated in practice through weight caps or regularization.

**Short sample for Nifty benchmark.** The Nifty 50 data aligned to only 7
observations in notebook 6, making those metrics statistically unreliable.
Future work should use a complete monthly Nifty series aligned to the full
2019-2026 range.

**Equal-weight as passive proxy.** Real passive strategies are typically
market-capitalization weighted, not equal-weighted. The equal-weight
assumption simplifies the research design but does not fully represent
passive investment in practice.

---

## Dependencies

```
python >= 3.10
pandas
numpy
scipy
matplotlib
seaborn
pathlib (standard library)
jupyter
```

Install all dependencies with:

```bash
pip install pandas numpy scipy matplotlib seaborn jupyter
```

---

## Reproducing the Analysis

1. Clone the repository and navigate to the project root.

2. Place the raw monthly price CSV files in `data/`. Each file should be named
   `TICKER Historical Data.csv` (e.g. `BRTI Historical Data.csv`) and must
   contain at minimum a `Date` column and a `Price` column. The Nifty 50 file
   should be named `Nifty 50 Historical Data.csv`.

3. Confirm that `utils.py` is present in the project root with the correct
   constants (`RF_ANNUAL`, `PERIODS_PER_YEAR`, directory paths, and helper
   functions).

4. Run the notebooks in order:

```bash
jupyter nbconvert --to notebook --execute 0_data_aggregator.ipynb
jupyter nbconvert --to notebook --execute 1_returns_generator.ipynb
jupyter nbconvert --to notebook --execute 2_portfolio_construction.ipynb
jupyter nbconvert --to notebook --execute 3_efficient_frontier.ipynb
jupyter nbconvert --to notebook --execute 4_performance_metrics.ipynb
jupyter nbconvert --to notebook --execute 5_viz.ipynb
jupyter nbconvert --to notebook --execute 6_risk_adjusted_metrics.ipynb
jupyter nbconvert --to notebook --execute 7_portfolio_weights.ipynb
```

Or open and run each notebook interactively in Jupyter Lab or Jupyter Notebook.

5. All outputs will appear in `analysis/` and all charts in `charts/`.

---

## Data Source

All price data was sourced from [investing.com](https://www.investing.com).
Data is publicly available and no proprietary or confidential data was used.
The full source code and data pipeline are open source and available at:
https://github.com/aam-007/portfolio-data-analysis
