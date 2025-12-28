# HTML Exports - Complete Journey Analysis

This folder contains the complete analytical journey as HTML exports for easy viewing and submission.

## Navigation Sequence

Please review the notebooks in the following order:

### 0. Project Introduction
**File:** `0_project_overview.html`
- Executive overview and business context
- Data foundation: Dunnhumby Complete Journey dataset
- Project structure and methodology overview
- Cross-module integration framework

### 1. Customer Value Map
**File:** `1_customer_value_map.html`
- RFM segmentation analysis
- K-means clustering (4 clusters identified)
- Premium Loyalists: 392 households generating 47% of revenue
- Growth Regulars, Reactivation Pool, and Lost/Churned segments
- Actionable recommendations by cluster

### 2. Bundle Analysis
**File:** `2_bundle_analysis.html`
- Market basket analysis using Apriori algorithm
- Top product bundles: Breakfast Kit, Deli Lunch, Pasta Night, Snack Pairings
- Association rules with confidence, lift, and support metrics
- Network visualization of category relationships
- Cross-promotional recommendations

### 3. Price Elasticity & Promotions
**File:** `3_price_elasticity.html`
- Log-log regression models for top categories and manufacturers
- Price elasticity estimates (most categories -0.5 to -0.9: inelastic)
- Display lift: 20-30% volume increase
- Mailer lift: 10-20% volume increase
- Pricing strategy: stabilize/increase prices on inelastic anchors

### 4. Coupon Redemption Propensity
**File:** `4_coupon_propensity.html`
- Logistic regression model (AUC ~0.75)
- Top 30% of households by score capture 68% of redemptions
- 2× lift over random targeting
- TypeA campaigns convert 2× better than TypeB/C
- Dual-objective optimization: redemption rate vs. incremental revenue

### 5. Time to Churn
**File:** `5_time_to_churn.html`
- Kaplan-Meier survival curves
- Cox proportional hazards model
- Key insight: coupons/campaigns only work when they trigger incremental trips/spend
- Log trips (HR ~0.57) and log spend (HR ~0.67) are the only protective factors
- Real-time churn monitoring framework (green/yellow/red zones)

### 6. Strategic Conclusions
**File:** `6_strategic_conclusions.html`
- Integration of all five modules into cohesive strategy
- Four strategic pillars:
  1. Segment-first resource allocation
  2. Bundle-driven merchandising over discounting
  3. Precision coupon targeting
  4. Behavior-first retention
- 90-day action plan with specific tactics
- Resource allocation blueprint ($100K quarterly budget example)
- Success metrics and continuous improvement loop

## Key Findings Summary

- **Revenue Concentration:** 392 Premium Loyalists (16% of households) drive 47% of revenue
- **Bundle Opportunity:** High-support bundles deliver 15-30% lifts without margin erosion
- **Pricing Power:** Inelastic categories (elasticity -0.5 to -0.9) tolerate 3-5% price increases
- **Coupon Efficiency:** Top 30% by propensity score deliver 2× lift and 68% of redemptions
- **Retention Driver:** Only trips and spend extend survival; tactics must boost these behaviors

## Technical Details

- **Data:** Dunnhumby Complete Journey dataset (2017-2018)
- **Scope:** 2,500 households, ~2.6M transactions, 711 days
- **Methods:** RFM + K-means, Apriori, log-log OLS, logistic regression, Kaplan-Meier + Cox PH
- **Tools:** Python 3.13, pandas, scikit-learn, statsmodels, lifelines, mlxtend

## Submission Package

All HTML files are self-contained and can be viewed in any modern web browser. They include:
- Full code execution results
- Visualizations and charts
- Data tables and statistical outputs
- Narrative explanations and business recommendations

Total package size: ~3.5 MB
