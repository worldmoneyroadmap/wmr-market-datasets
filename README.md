# World Money Roadmap market datasets

Free CSV datasets published by [World Money Roadmap](https://worldmoneyroadmap.com/en/), a market data site
covering U.S. and Korean markets. Released under [CC BY 4.0](LICENSE).

This GitHub repository is a mirror of the Hugging Face dataset
[worldmoneyroadmap/wmr-market-datasets](https://huggingface.co/datasets/worldmoneyroadmap/wmr-market-datasets).
Both carry the same six files. The original files are regenerated at every site build and listed on the site's
[data library page](https://worldmoneyroadmap.com/en/data/#datasets).

<!-- BEGIN:stamp -->
**Last refreshed: 2026-11-28 (UTC).** Row counts below match the files in `data/`.
<!-- END:stamp -->

## Files

All files are in [`data/`](data/). Column descriptions and units for every file are also in
[`data/datasets.json`](data/datasets.json).

<!-- BEGIN:files -->
| File | What it contains | Rows | As of | Size | Source |
|---|---|---:|---|---:|---|
| [`fed-rate-history.csv`](data/fed-rate-history.csv) | Each date the FOMC changed the federal funds target rate (or range), the size of the change and the new level. Holds are not listed, as in the official table. | 42 | 2026-11-21 | 1.4 KB | [Federal Reserve Board — Open Market Operations table](https://www.federalreserve.gov/monetarypolicy/openmarket.htm) |
| [`market-dates.csv`](data/market-dates.csv) | U.S. and Korean market holidays and early closes, FOMC decision days, U.S. CPI and jobs-report release dates, U.S. monthly options and KOSPI 200 futures and options expirations, and SPDR ETF (SPY, DIA, MDY) ex-dividend dates in one table. Status = official, expected, tentative or calculated (rule-based). | 150 | 2026-11-20 | 30.0 KB | NYSE holiday and early-close notice (ICE investor relations), Federal Reserve FOMC calendar, U.S. Bureau of Labor Statistics release schedules, Cboe options calendar, State Street SPDR distribution schedule, Korea Astronomy and Space Science Institute calendar of official public holidays (Korean holidays not yet announced by the Korea Exchange are expected), and a Korean broker guide to the KOSPI 200 expiration rule (second Thursday) (source URL on every row) |
| [`trading-days.csv`](data/trading-days.csv) | Trading days per month after removing weekends and market holidays (WMR calculation). U.S. early-close days count as trading days. Korean figures are expected until the Korea Exchange announces its holidays. | 39 | 2026-11-20 | 1.3 KB | WMR calculation from the NYSE holiday calendar (Dec 23, 2025) and Korea Exchange holidays / official public holidays |
| [`us-financials-sec.csv`](data/us-financials-sec.csv) | 10-Q and 10-K XBRL values filed with the SEC by the U.S. companies covered by WMR stock pages (fiscal-year basis). Fourth-quarter values are the annual total minus the first three quarters (q4_derived = 1; EPS not derived). Page tables round these values to billions or millions. | 6,034 | 2026-11-25 | 683.5 KB | [U.S. Securities and Exchange Commission (SEC) EDGAR XBRL companyfacts](https://www.sec.gov/edgar/sec-api-documentation) |
| [`ai-lab-nav.csv`](data/ai-lab-nav.csv) | Daily value and cumulative return since start of the paper accounts run only by AI. Hypothetical, not real trades, and not investment advice. Daily benchmark index values (third-party prices) are not included. | 97 | 2026-11-27 | 4.9 KB | WMR calculation (AI experiment execution engine) |
| [`ai-lab-metrics.csv`](data/ai-lab-metrics.csv) | For each paper account: cumulative return, the benchmark's cumulative return over the same period and the gap, maximum drawdown, volatility, Sharpe, Sortino and information ratios, beta, trade count and costs, as calculated by WMR. With a short history the verdict is too_early. Not investment advice. | 6 | 2026-11-27 | 1.2 KB | WMR calculation (AI experiment performance metrics) |
<!-- END:files -->

## Sources and attribution

Only data that may be republished is included: figures World Money Roadmap calculates itself, U.S. government
works, and dates taken from official public notices. Third-party market prices are not included.

| File | Source | Terms of the source |
|---|---|---|
| `fed-rate-history.csv` | Board of Governors of the Federal Reserve System, [Open Market Operations](https://www.federalreserve.gov/monetarypolicy/openmarket.htm) table | Public domain ([Federal Reserve Board website policies](https://www.federalreserve.gov/disclaimer.htm)) |
| `market-dates.csv` | Public notices: NYSE Group holiday and early-close announcement (ICE investor relations), Federal Reserve FOMC calendar, U.S. Bureau of Labor Statistics release schedules (CPI, Employment Situation), Cboe options calendar, State Street Global Advisors SPDR distribution schedule, Korea Astronomy and Space Science Institute calendar of official public holidays (Korean holidays not yet announced by the Korea Exchange are marked `expected`), and a Korean broker's guide to the KOSPI 200 expiration rule (second Thursday). The `source_url` column names the source of every row. | Calendar dates are facts compiled by World Money Roadmap from public notices; no text or tables are copied. BLS and Federal Reserve material is public domain. |
| `trading-days.csv` | Calculated by World Money Roadmap from the NYSE holiday calendar and Korean market holidays (same sources as `market-dates.csv`) | CC BY 4.0 (World Money Roadmap) |
| `us-financials-sec.csv` | U.S. Securities and Exchange Commission, [EDGAR XBRL companyfacts API](https://www.sec.gov/edgar/sec-api-documentation) (10-Q and 10-K filings) | U.S. government work, public domain ([SEC](https://www.sec.gov/about/webmaster-frequently-asked-questions)) |
| `ai-lab-nav.csv` | Calculated by World Money Roadmap: paper (hypothetical) accounts in the site's [AI investing experiment](https://worldmoneyroadmap.com/en/ai-lab/) | CC BY 4.0 (World Money Roadmap) |
| `ai-lab-metrics.csv` | Calculated by World Money Roadmap from the same paper accounts | CC BY 4.0 (World Money Roadmap) |

Suggested source lines when you reuse a file:

- `fed-rate-history.csv`: "Source: Federal Reserve Board; compiled by World Money Roadmap"
- `us-financials-sec.csv`: "Source: U.S. SEC EDGAR; compiled by World Money Roadmap"
- `market-dates.csv`: "Source: official exchange and agency calendars (see source_url); compiled by World Money Roadmap"
- other files: "Data: World Money Roadmap (worldmoneyroadmap.com), CC BY 4.0"

Third-party names (NYSE, ICE, Korea Exchange, Cboe, SPDR, State Street) are trademarks of their owners and are used
only to identify the source. See [NOTICE](NOTICE) for the full attribution list.

### What is not included, and why

- Daily prices from Yahoo Finance, Naver, Nasdaq.com and similar sites: their terms do not allow redistribution.
- Korea Exchange (KRX) data services and the public-data-portal price feed: licensed for non-commercial use only.
- FRED series marked as copyrighted, FINRA data, and private index data (for example S&P, Dow Jones, Nikkei).
- DART (Korea) filings datasets, Bank of Korea rate history and the site's sentiment and analog datasets:
  left out here until their redistribution terms are confirmed. Some of them are on the site's data page.
- No personal holdings of any person. The AI-lab files describe paper accounts only, with no real money.

## Update frequency

A [GitHub Actions workflow](.github/workflows/weekly-update.yml) runs every Saturday at 01:17 UTC and can also be
started by hand. It downloads the public files from `https://worldmoneyroadmap.com/data/csv/en/`, checks them with
[`scripts/update.py`](scripts/update.py), and commits only when something changed. It uses no secrets or personal
tokens.

The checks: the header must match `datasets.json`, the row count must match the metadata, every row must have the
right number of fields, the AI-lab files may contain only the known paper-account codes, no file may exceed 50 MB, no Korean text may appear in the English edition, no reference to
an excluded source may appear, and no file may lose more than 30% of its rows in one update. If any check fails,
nothing is written and the workflow fails.

How often the underlying data changes depends on the file (see the schema below). The site's own copies may be
newer than this mirror by up to a week.

## Format

- UTF-8 CSV with a byte-order mark (BOM), CRLF line endings, every field quoted, first line is the header.
  Files are byte-for-byte copies of the site files.
- Units are in the column names (for example `change_bp`, `target_low_pct`, `revenue_usd`, `nav_usd`).
- Dates are ISO 8601 (`YYYY-MM-DD`).
- `us-financials-sec.csv`: values are on a fiscal-year basis; Q4 is the annual total minus Q1 to Q3 (`q4_derived` = 1).
- `trading-days.csv`: U.S. early-close days count as trading days. Korean figures stay `expected` until the
  Korea Exchange announces its holidays.
- `market-dates.csv`: `status` is `official`, `expected`, `tentative` or `calculated` (rule-based).
- `ai-lab-*`: paper accounts, not real trades. No benchmark price series is included; only the benchmark's return
  over the same period appears in the metrics file.

## Schema

<!-- BEGIN:schema -->
### `fed-rate-history.csv`

U.S. Federal Reserve target rate change history. Updated: when the Fed changes rates (after checking the official table).

| Column | Description |
|---|---|
| `date_fed_table` | Date as printed in the Fed table (YYYY-MM-DD; often the day after the announcement) |
| `change_bp` | Change in basis points (1 bp = 0.01 percentage point), as printed |
| `target_low_pct` | Lower bound of target range (% per year; blank before Dec 16, 2008, when a single target was used) |
| `target_high_pct` | Upper bound of target range, or the single target (% per year) |

### `market-dates.csv`

Market dates — holidays, early closes, FOMC, CPI, jobs report, options expiration, ex-dividend dates. Updated: when official schedules are published or changed.

| Column | Description |
|---|---|
| `date` | Date (YYYY-MM-DD, local date of that market) |
| `time_et` | New York time (HH:MM, when applicable) |
| `market` | Market (US or KR) |
| `event_type` | Event type code |
| `event` | Description |
| `reference_period` | Reference month for CPI and jobs data (YYYY-MM) |
| `status` | official, expected, tentative or calculated (rule-based) |
| `note` | Note |
| `source_url` | Source URL |

### `trading-days.csv`

Trading days per month — U.S. (NYSE and Nasdaq) and Korea (KOSPI and KOSDAQ). Updated: when the holiday source changes.

| Column | Description |
|---|---|
| `year` | Year |
| `month` | Month (01–12; all = full-year total) |
| `us_trading_days` | U.S. trading days (days) |
| `us_early_close_days` | Of which U.S. early-close days (days) |
| `kr_trading_days` | Korea trading days (days; blank when the holiday list for that year is incomplete) |
| `kr_status` | Status of the Korean figure (official or expected) |

### `us-financials-sec.csv`

U.S. company quarterly and annual financials (SEC XBRL) — revenue, operating income, net income, diluted EPS. Updated: when new 10-Q or 10-K filings appear (automated).

| Column | Description |
|---|---|
| `ticker` | Ticker |
| `sec_registrant` | SEC registrant name |
| `sec_cik` | SEC CIK |
| `period_type` | Q = quarter, FY = fiscal year |
| `fiscal_year` | Fiscal year |
| `fiscal_quarter` | Fiscal quarter (1–4; blank for annual) |
| `period_end` | Period end date |
| `revenue_usd` | Revenue (US$) |
| `operating_income_usd` | Operating income (US$; blank if not reported) |
| `net_income_usd` | Net income (US$) |
| `eps_diluted_usd` | Diluted EPS (US$ per share) |
| `q4_derived` | 1 = fourth quarter derived from the annual total |

### `ai-lab-nav.csv`

AI investing experiment — daily paper-account value and cumulative return. Updated: after each market close.

| Column | Description |
|---|---|
| `date` | Date (YYYY-MM-DD) |
| `account` | Account code |
| `account_name` | Account name |
| `nav_usd` | Account value (US$, started at $100,000) |
| `cum_return_pct` | Cumulative return since start (%, two decimals as on the page) |

### `ai-lab-metrics.csv`

AI investing experiment — account metrics (vs. benchmark, risk, costs). Updated: after each market close.

| Column | Description |
|---|---|
| `account` | Account code |
| `account_name` | Account name |
| `start_date` | Start date |
| `as_of` | As-of date |
| `trading_days` | Trading days run (days) |
| `cum_return_pct` | Cumulative return (%) |
| `benchmark` | Benchmark code (spx = S&P 500, btc = Bitcoin, mix = ACWI and AGG blend) |
| `benchmark_cum_return_pct` | Benchmark cumulative return over the same period (%) |
| `excess_return_pp` | Difference vs. benchmark (percentage points) |
| `max_drawdown_pct` | Maximum drawdown (%) |
| `volatility_ann_pct` | Annualized volatility (%) |
| `sharpe_ratio` | Sharpe ratio (risk-free rate 0%) |
| `sortino_ratio` | Sortino ratio |
| `information_ratio` | Information ratio |
| `beta` | Beta vs. benchmark |
| `trades` | Number of trades |
| `closed_trades` | Closed trades |
| `win_rate_pct` | Share of closed trades with a gain (%) |
| `costs_pct_of_start` | Cumulative trading costs (% of starting value) |
| `verdict` | Verdict code (e.g. too_early) |
<!-- END:schema -->

## How the data is made

The files are generated automatically by the site's build from its own data files. The site's text is written by AI
(Anthropic's Claude) and published automatically; numbers are checked against source data by software before
publishing, and later changes are listed in a public [corrections log](https://worldmoneyroadmap.com/en/corrections/).
See the site's [AI use policy](https://worldmoneyroadmap.com/en/ai-policy/).

## Limitations

- Information only. Not investment advice.
- Dates marked `expected` or `tentative` can change; check the official source before relying on them.
- SEC values are as filed; companies can restate them later.

## License

The datasets are released under the [Creative Commons Attribution 4.0 International License](LICENSE)
(CC BY 4.0; site terms: [worldmoneyroadmap.com/en/content-use/#datasets](https://worldmoneyroadmap.com/en/content-use/#datasets)).
Public-domain figures inside the files stay public domain; the license covers the compilation.
The scripts in this repository are released under the same license.

## How to cite

Short credit line:

> Data: World Money Roadmap (worldmoneyroadmap.com), CC BY 4.0

BibTeX:

```bibtex
@misc{wmr_market_datasets,
  author       = {{World Money Roadmap}},
  title        = {World Money Roadmap market datasets},
  year         = {2026},
  publisher    = {GitHub},
  howpublished = {\url{https://github.com/worldmoneyroadmap/wmr-market-datasets}},
  note         = {Also on Hugging Face: https://huggingface.co/datasets/worldmoneyroadmap/wmr-market-datasets. CC BY 4.0}
}
```

Machine-readable citation: [CITATION.cff](CITATION.cff) (GitHub shows it under "Cite this repository").

## Links

- Website: https://worldmoneyroadmap.com
- Data library page: https://worldmoneyroadmap.com/en/data/
- Hugging Face dataset: https://huggingface.co/datasets/worldmoneyroadmap/wmr-market-datasets
