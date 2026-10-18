# Messi vs. Ronaldo: The Race to 1,000 Official Goals

Statistical modeling and predictive analytics project in Python designed to estimate the trajectory and target date for **Lionel Messi** and **Cristiano Ronaldo** to reach **1,000 official career goals**.

Rather than treating all historical matches equally, this project applies **exponential time-decay functions**, **league quality adjustments**, and **hierarchical Bayesian inference** to reflect age-related decline, current match rhythm, and competitive environment shifts.

---

## Methodology & Architecture

- **Poisson & Gamma Arrival Process**: Goal-scoring is modeled as a Poisson count process, converting the remaining goal counts into time-to-event estimations via Gamma distribution sampling.
- **Backtested Exponential Time-Decay**: Calibrated via historical backtesting (optimal half-life $H = 0.75$ years) to ensure recent performance heavily informs future rates while preserving structural historical baselines.
- **League Quality Adjustments**: Coefficients derived from competitive power rankings normalize goals scored across top European leagues, international competitions, MLS, and the Saudi Pro League.
- **Hierarchical Bayesian Model (PyMC)**: Implements a Negative Binomial regression with NUTS sampling to incorporate age slope parameters ($\beta$) and dynamically modulate prior variance based on temporal weights.
- **Interactive Dashboard**: Developed using Streamlit and Plotly with custom HTML/CSS KPI metrics, interactive parameter tuning, and probability density curves.

---

## Key Results

- **Efficiency Context**: At the primary model cut-off, Cristiano Ronaldo holds 977 goals across 1,332 matches (0.73 goals/match)[cite: 11, 12], whereas Lionel Messi holds 930 goals across 1,168 matches (0.79 goals/match)[cite: 11, 12].
- **Projected Target Dates (Bayesian Model)**:
  - **Cristiano Ronaldo**: Estimated ~April 2027 (80% CI: Feb 2027 – Jul 2027)[cite: 13]
  - **Lionel Messi**: Estimated ~June 2028 (80% CI: Feb 2028 – Dec 2028)[cite: 13]
- **Contract Scenario Sensitivity**: Pure statistical projection gives Ronaldo the lead due to his absolute goal buffer. However, scenario analysis shows that if Ronaldo retires at the end of his Al-Nassr contract (June 2027), Messi's probability of reaching 1,000 goals first rises to 77%.

---

## Tech Stack

- **Language**: Python 3.13
- **Bayesian Inference**: PyMC, ArviZ
- **Data Manipulation**: Pandas, NumPy
- **Data Visualization**: Plotly, Streamlit
- **Environment**: Visual Studio Code, Jupyter Notebooks
