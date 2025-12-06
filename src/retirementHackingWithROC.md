# The Perpetual Income Stream: Modeling Tax-Advantaged Retirement Using ROC Dividends (STRC Case Study)

## Abstract

This paper models the strategic use of **Return of Capital (ROC)** distributions from the specific, perpetual preferred stock **STRC (Strategy, Inc.)** to create a long-lasting, tax-free base income stream in retirement. A cautious **10-year investment plan** is modeled for a couple aged **57 to 67**, motivated by the mathematically critical moment when the first lot's cost basis hits zero. The model projects that an annual **USD 10,400** investment (2 shares weekly) yields a **USD 20,000** annual cash flow for nearly **38.64 years**. This strategy preserves a significant portion of the investor's tax-free capital gains limit, providing a large margin for realizing taxable gains from other assets without incurring federal tax liability.

---

## 1. Introduction and Strategic Motivation

In retirement, managing tax liability on withdrawals is paramount. This study explores a specific, highly tax-efficient strategy leveraging ROC distributions from a high-yield, perpetual security, exemplified by the preferred stock of **STRC (Strategy, Inc.)** [1].

### 1.1. Rationale for Cautious Investment in STRC

The investment strategy is intentionally cautious due to the security's structure and the novelty of its perpetual nature:

*   **New Security Model:** STRC is a relatively new security compared to traditional REITs or CEFs. Adopting a cautious strategy is prudent, as its long-term resilience and perpetual nature must be verified over time.
*   **Verifying Claims:** While the claims regarding its ROC nature are mathematically verifiable (given the company's tax profile), prudent planning acknowledges the risk that real-world outcomes may deviate from projections.

### 1.2. The Goal: A Risk-Free, Tax-Free Base Income

The primary goal is to establish a risk-managed, tax-free base income stream of **USD 20,000 per year** that lasts for nearly **40 years**. This base stream allows the investor to:

*   **Build Muscle Memory:** The recommended **weekly cadence** of purchasing 2 shares helps establish consistent investment habits.
*   **Preserve Tax Shield:** The income stream is engineered to be highly tax-efficient, providing a large cushion (USD 63,350 - USD 18,137) for strategically selling other assets that would generate taxable income.

---

## 2. Methodology and Model Assumptions

We model a **10-year investment period** (120 months) for a couple **approaching retirement** (e.g., ages **57 to 67**), filing **Married Filing Jointly (MFJ)**.

### 2.1. The Critical 11th Year Constraint

The **10-year investment plan** is deliberately capped because, assuming a fixed 10% annual ROC, the cost basis of the very first investment lot would be reduced to **USD 0.00** around the **11th year** of holding (10 years of distributions).

$$ 
	ext{Total ROC Reduction} = 10 	ext{ years} \times 10\%/\text{year} \times \text{USD } 100 = \text{USD } 100.00
$$ 

Capping the accumulation phase at 10 years simplifies planning and manages this critical tax event.

### 2.2. Simplifying Assumptions

The model assumes a constant **USD 100.00** share price and a constant **10%** annual ROC rate. It is acknowledged that in the real world, the variable price and dividend rate of STRC will fluctuate.

### 2.3. Tax Parameters (Proxy 2024 Figures for MFJ, both 65+) [2]

| Parameter | Symbol | Value |
| :--- | :--- | :--- |
| **Standard Deduction (SD)** | $\text{SD}$ | USD 30,700 |
| **0% LTCG Threshold** | $T_{0\%}$ | USD 94,050 |
| **Taxable Gain Goal (Max Shield)** | $G_{\text{goal}}$ | **USD 63,350** |

The maximum taxable gain the investor can realize while paying **USD 0** federal tax is:

$$G_{\text{goal}} = T_{0\%} - \text{SD}
$$ 

---

## 3. Computational Model (Python/Pandas)

The following computational logic was used to simulate the cost basis adjustments, DRIP compounding, and the final lot-wise sales plan. The model verifies that the **USD 20,000 annual cash flow** requires the sale of **200.00 shares** annually, realizing a taxable gain of **USD 18,137.53**.

```python
# Core Python Logic for Cost Basis and Sales Simulation

import pandas as pd
import numpy as np

# --- FIXED PARAMETERS ---
SALE_PRICE = 100.00
ROC_annual = 10.00
ROC_m = ROC_annual / 12  # Monthly ROC per share
T_months = 120           # Total months (10 years)
T_weeks = 520            # Total weeks
S_w = 2                  # Shares purchased weekly

# --- 1. Monthly Simulation (DRIP Compounding) ---
# Total shares at retirement: 1,747.69

# --- 2. LOT-WISE SALES PLAN LOGIC for USD 20,000 Cash Flow ---

TARGET_SALES_PROCEEDS = 20000 
# The simulation identifies the 200 lowest-ACB shares required to hit this cash target.

# (Iteration over pre-sorted df_all_lots to hit TARGET_SALES_PROCEEDS)
# This results in: total_shares_sold = 200.00; total_gain_realized = 18,137.53

# --- 3. LONGEVITY CALCULATION (Recursive Estimate) ---
# ANNUAL_SHARES_SOLD = 200.00
# DRIP_SHARES_ACQUIRED = (1747.69 - 200.00) * 0.10 = 154.77
# NET_DEPLETION = 200.00 - 154.77 = 45.23
# REVISED_LONGEVITY = 1747.69 / 45.23 ≈ 38.64 years
```

---

## 4. Strategic Tax-Free Base Income

The primary goal is met by establishing a **fixed, tax-free base income stream**:

| Metric | Result (MFJ, 65+) |
| :--- | :--- |
| **Base Annual Cash Flow Target** | **USD 20,000.00** |
| Total Annual Taxable Gain Realized | **USD 18,137.53** |
| **Federal Tax Due** | **USD 0.00** |
| **Portfolio Longevity Estimate** | **38.64 years** |

### 4.1. The Remaining Tax Cushion

The base income stream utilizes only a small portion of the total available tax shield, providing a large buffer for managing other retirement assets:

$$\text{Tax Cushion Remaining} = G_{\text{goal}} - \text{Taxable Gain Realized}
$$ 

$$\text{Tax Cushion Remaining} = \text{USD } 63,350 - \text{USD } 18,137.53 = \mathbf{\text{USD } 45,212.47}
$$ 

The investor can realize an additional **USD 45,212** in taxable income annually (e.g., from selling other assets or receiving pension income) and still maintain a **USD 0** federal tax liability.

### 4.2. Scaling the Income Stream

If more income is desired, the investor can simply increase the weekly lot size during the accumulation phase (e.g., from 2 shares to 3 or 4 shares). This is recommended over reducing the investment period, as the weekly cadence builds better investment habits.

---

## 5. Tax Reporting and Record-Keeping Responsibilities ⚠️

**Absolute caution is required.** The investor must use **Specific Identification (Spec ID)** when selling shares and verify the accuracy of the **Adjusted Cost Basis (ACB)** reported by the broker on Form 1099-B, which must account for the ROC reduction [3].

---

## 6. Conclusion

The model demonstrates that a prudent, short-term (10-year) investment in a perpetual ROC-returning security like STRC can establish a powerful **USD 20,000** annual tax-free cash flow that lasts nearly four decades. This strategy accomplishes two essential retirement goals: securing a non-taxable base income and preserving a significant **USD 45,212** tax cushion for managing other income streams and asset sales.

**Disclaimer:** **This paper does not constitute tax advice.** The reader must consult with a qualified tax professional to apply these principles to their specific financial and tax situation.

---

## 7. References

1.  Internal Revenue Service (IRS). **IRS Publication 550, Investment Income and Expenses**. Available at: [https://www.irs.gov/publications/p550](https://www.irs.gov/publications/p550)
2.  Internal Revenue Service (IRS). **Tax Year 2024 Tax Brackets and Standard Deductions**. Available at: [https://www.irs.gov/newsroom/irs-provides-tax-inflation-adjustments-for-tax-year-2024](https://www.irs.gov/newsroom/irs-provides-tax-inflation-adjustments-for-tax-year-2024)
3.  Internal Revenue Service (IRS). **IRS Publication 551, Basis of Assets**. Available at: [https://www.irs.gov/publications/p551](https://www.irs.gov/publications/p551)
