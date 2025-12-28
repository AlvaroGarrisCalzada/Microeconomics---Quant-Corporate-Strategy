# IE Customer Analytics Complete Journey Analysis

A comprehensive data-driven marketing strategy project analyzing 2,500 households and ~2.6M transactions from the Dunnhumby Complete Journey dataset to optimize resource allocation, bundling, pricing, coupon targeting, and retention.

## Quick Navigation

### View Analysis Results (HTML Exports)
**For submission/review, start here:**
- Open `index.html` in your browser for an interactive navigation dashboard
- All notebooks are pre-exported as HTML files in the root directory:
  - `0_project_overview.html` - Project introduction and methodology
  - `1_customer_value_map.html` - RFM segmentation and clustering
  - `2_bundle_analysis.html` - Market basket analysis
  - `3_price_elasticity.html` - Price sensitivity and promotional lift
  - `4_coupon_propensity.html` - Coupon targeting optimization
  - `5_time_to_churn.html` - Survival analysis and retention
  - `6_strategic_conclusions.html` - Integrated strategy playbook

### Run Notebooks Locally
The repo is ready to run with a lightweight virtual environment. These steps assume a recent Python 3 (3.10+).

## Quick start
- From the repo root:
  - `python -m venv .venv`
  - Activate  
    - macOS/Linux: `source .venv/bin/activate`  
    - Windows (PowerShell): `.venv\Scripts\Activate.ps1`
  - `python -m pip install --upgrade pip`
  - `pip install -r requirements.txt`
  - (Optional, keeps Jupyter tidy) `python -m ipykernel install --user --name ie-ca --display-name "ie-ca"`
- Launch notebooks from the repo root:
  - `jupyter lab` (or `jupyter notebook` if you prefer the classic UI)
  - Pick the `ie-ca` kernel (or the active `.venv` kernel) when opening notebooks.

## Running notebooks end-to-end
- Keep `innitial_datasets/` beside `code/` so the relative paths used in notebooks keep working.
- You can auto-run a notebook from the command line, e.g.:
  - `jupyter nbconvert --to notebook --execute --inplace code/a_customer_value_map/customer_value_map.ipynb`
  - Repeat for others as needed.

## What’s installed
- Analytics stack: `pandas`, `numpy`, `matplotlib`, `seaborn`, `scikit-learn`, `statsmodels`, `scipy`, `lifelines`, `mlxtend`, `CHAID`
- File I/O: `pyarrow` (parquet), `openpyxl` (Excel)
- Notebook tooling: `jupyterlab`, `notebook`, `ipykernel`

## Project Structure

```
ie_ca/
├── index.html                          # Interactive navigation dashboard
├── 0_project_overview.html             # Exported: Project introduction
├── 1_customer_value_map.html           # Exported: Customer segmentation
├── 2_bundle_analysis.html              # Exported: Product bundles
├── 3_price_elasticity.html             # Exported: Pricing strategy
├── 4_coupon_propensity.html            # Exported: Coupon targeting
├── 5_time_to_churn.html                # Exported: Retention analysis
├── 6_strategic_conclusions.html        # Exported: Integrated strategy
├── HTML_EXPORTS_README.md              # Documentation for HTML exports
├── code/
│   ├── 0_project_introduction/
│   ├── a_customer_value_map/
│   ├── b_bundle_analysis/
│   ├── c_price_elasticity+promotions/
│   ├── d_coupon_redemption_propensity/
│   ├── e_time_to_churn/
│   └── f_strategic_conclusions/
├── innitial_datasets/                  # Raw Dunnhumby data
└── requirements.txt                    # Python dependencies
```

## Key Findings

- **Revenue Concentration:** 392 Premium Loyalists (16% of households) drive 47% of revenue
- **Bundle Opportunity:** High-support bundles deliver 15-30% volume lifts without margin erosion
- **Pricing Power:** Inelastic categories (elasticity -0.5 to -0.9) tolerate 3-5% price increases
- **Coupon Efficiency:** Top 30% by propensity score deliver 2× lift and capture 68% of redemptions
- **Retention Driver:** Only trips and spend extend survival; tactics must boost these behaviors

## Troubleshooting
- If Jupyter cannot find the kernel, re-run `python -m ipykernel install --user --name ie-ca --display-name "ie-ca"` and restart Jupyter.
- If packages seem outdated, re-run `pip install -r requirements.txt`.

## Submission Package

All HTML files are self-contained with full execution results, visualizations, and recommendations. Total package size: ~3.5 MB.
