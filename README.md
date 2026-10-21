### 👉 [Open the interactive framework](https://laurencefilby.github.io/value-capture-gap/)

# The Value Capture Gap

A framework for the gap between the **value people create** and the **pay they capture**, anchored in US data.

## The core idea

At any point in a career, pay sits inside a band:

- **Ceiling**: the marginal value you produce for the organisation
- **Floor**: your best realistic alternative (reservation wage)

Where pay settles between the two depends on:

1. How visible your contribution is
2. Market structure and switching costs
3. How hard your value is to attribute
4. Negotiation and behavioural factors (anchoring, status quo bias)

Above your pay sits **uncaptured value**, which the firm keeps. Below it sits your **retention margin**, the premium that stops you leaving.

## What the page shows

**Real data**

| Evidence | Figure | Source |
|---|---|---|
| Productivity vs typical worker pay | Productivity +93.7%, pay +32.7% (1979 to 2026 Q2) | EPI |
| Labour share of business output | 65.5% (1947) to 52.8% (Q2 2026), a record low | BLS |
| Innovators' share of the value they create | About 2.2% | Nordhaus, NBER |
| Job switchers vs stayers, wage growth | 4.7% vs 3.4% (Sep 2026); switchers peaked at 8.4% (Aug 2022) | Atlanta Fed |
| Concentration of pay | Workers on $1M+ (0.13%) earned 5.3% of all US wages in 2022 | SSA |

**Interactive model**

- A career band for five earnings tiers (median to top 0.01%), each anchored to its real 2022 wage percentile
- Three strategy toggles that move the band live
- A personal calculator: enter your pay, best alternative and value created to see your capture share

The career band is an illustrative model, not a measurement. Its ceiling and floor ratios are framework assumptions.

## The three strategies

**I. Raise the floor** (expand the opportunity set): skills the market prices, higher-value sectors, credible outside options.

**II. Raise the ceiling** (create more value): innovation, scope, decision rights. The catch: without attribution, the firm keeps the extra and the gap widens.

**III. Move within the band** (capture more): quantify output, negotiate from data, equity and profit share.

## Repository

| Path | What it is |
|---|---|
| `index.html` | The interactive page (served by GitHub Pages) |
| `model/value_capture_model.py` | Python version of the career band model; exports `data/band_model.csv` |
| `data/evidence.json` | All real data points used, with sources |
| `archive/value_capture_percentiles_final.html` | The original v1 Plotly chart |

Run the model:

```bash
python model/value_capture_model.py          # writes data/band_model.csv
python model/value_capture_model.py --plot   # plus a matplotlib chart
```

## Author

**Laurence Filby**
Quantitative Strategies | Behavioural Economics | Post-Quantum Systems

## Licence

© 2025–2026 Laurence Filby. All rights reserved. Academic citation permitted with attribution. Commercial use or reproduction requires written permission.

Research collaboration and licensing: laurence@sevenbricks.co.uk
