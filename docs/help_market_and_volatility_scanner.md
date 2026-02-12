### Welcome to Event-Based Financial Analysis!

  This section allows you to filter and analyse financial data based on **specific events** and **temporal patterns**.
  You can gain insights on how the market behaves **before**, **during**, and **after** major events, enabling you to make more informed decisions.

  #### **Selecting the Right Event**
  Choose events from **macroeconomic indicators**, **earnings reports**, **geopolitical events**, etc., and use **time-based** filters to narrow down the analysis.
  Examples of event groupings:
  - **Economic Growth and Stability** (e.g., GDP Reports, Business Cycles)
  - **Labour Market Dynamics** (e.g., Unemployment Rates, Non-farm Payrolls)
  - **Market Trends & Financial Health** (e.g., Earnings Reports, Financial Statements)

  #### **Timeframes for Event Analysis**
  - **Pre-event Analysis**: Analyses market behaviour **before** an event.
  - **Post-event Analysis**: Analyses the market’s **reaction** after the event.
  - **Custom Timeframe**: Choose a custom window for your analysis.

  #### **Temporal Patterns:**
  Popular time filters you can apply:
  - **Weekday** (e.g., Monday to Friday)
  - **Month** (e.g., January to December)
  - **Season** (e.g., Spring, Winter)
  - **Business Quarter** (e.g., Q1, Q2)
  - **Week (1-52/53)**: Weekly performance trends

  These filters help you identify **patterns** and **cyclic behaviours** in market performance. Combine them with features like **frequency distribution** and **volatility analysis** to uncover valuable insights.

  #### **Features & Analysis**
  After selecting the time and event filters, you can explore:
  - **Frequency Distribution**: See how often certain behaviours occur over time.
  - **Price Movement & Trend Visualisation**: Explore price changes using charts like line, candlestick, and area charts.
  - **Returns Analysis**: View the return rates for selected periods.
  - **Volatility vs DPT Achievement**: Analyse how volatility affects the achievement of your desired profit targets.

  **Tip**: Always check if your time filters match your analysis focus—whether you're interested in daily returns, weekly trends, or seasonal effects.

  ### What are Monte Carlo Simulations?

  Monte Carlo simulations are used to predict the possible future prices of an asset by running many simulations based on a random process. Each simulation represents a possible price path based on the volatility of the asset.

  - **Mean Final Price**: This is the average final price after running all the simulations. It represents the central tendency of possible outcomes.
  - **Standard Deviation**: Measures how much the final prices deviate from the mean price, indicating uncertainty.
  - **10th and 90th Percentiles**: These percentiles represent the worst and best-case scenarios for the future price, based on the simulations.

  This method is widely used in financial modelling to help estimate the risk and potential return of investments under uncertainty. It can be particularly useful for **risk management**, where you assess various possible outcomes and make more robust investment decisions.

  ### What are Risk-Adjusted Returns?

  Risk-adjusted returns help investors understand the profitability of an asset relative to the risk involved in investing in it. Here are two common metrics used:

  #### **Sharpe Ratio**
  The **Sharpe Ratio** measures the excess return (or risk premium) of an asset relative to its volatility. It compares the asset's return to a "risk-free rate" (e.g., Treasury bonds).
  - **Formula**: (Asset Return - Risk-Free Rate) / Standard Deviation of Asset Return
  - A **higher Sharpe Ratio** implies a better risk-adjusted return.
  - **Tip**: If you don't have a specific risk-free rate in mind, a typical value is **0%** or the average yield on government bonds.

  #### **Sortino Ratio**
  The **Sortino Ratio** focuses only on the downside risk (negative volatility). It is especially useful for risk-averse investors who are more concerned with avoiding losses than with overall volatility.
  - **Formula**: (Asset Return - Target Return) / Downside Deviation
  - A **higher Sortino Ratio** indicates better performance per unit of downside risk.
  - **Tip**: A **target return** is a specific return you're aiming to achieve. By default, this is usually **0%**, but you can adjust it to reflect your goals.

  These metrics are used by investors to evaluate the quality of an asset or portfolio's risk-adjusted performance.

  ### What is **Volume vs ATR Correlation**?

  **Volume vs ATR Correlation** measures the relationship between trading volume and volatility (as measured by the Average True Range). A higher correlation suggests that as trading volume increases, the asset’s price volatility also increases, and vice versa.

  - **Positive Correlation**: As volume increases, volatility increases. This could indicate that higher market participation or market-moving events are driving larger price fluctuations.
  - **Negative Correlation**: As volume increases, volatility decreases. This may suggest more stability in the market during periods of high trading activity.
  - **No Correlation**: No clear relationship between volume and volatility. Other factors may be influencing price movements.

  #### **Correlation Ranges**:
  - **Strong Positive Correlation**: A correlation of **0.7 to 1.0** suggests that higher volume corresponds with higher volatility.
  - **Moderate Positive Correlation**: A correlation of **0.3 to 0.7** indicates a moderate relationship.
  - **No Correlation**: A correlation of **0.0 to 0.3** means there is little to no relationship between volume and volatility.
  - **Weak Negative Correlation**: A correlation of **-0.3 to 0.0** suggests that higher volume corresponds with lower volatility.
  - **Strong Negative Correlation**: A correlation of **-1.0 to -0.7** suggests a strong inverse relationship, where higher volume leads to lower volatility.

  **Tip**: The Volume vs ATR Correlation can help you assess how market sentiment (via volume) affects price movement. It can be especially useful when combined with other volatility or price trend indicators.

  ### Pearson’s/Spearman’s Correlation with Market Indices

  **Correlation** is a statistical measure that describes the relationship between two variables. In financial analysis, it’s used to assess how two assets (or an asset and a market index) move in relation to each other. Here, we are looking at the correlation between the selected asset (e.g., **Tesla**) and several market indices (e.g., **S&P 500**, **Nasdaq**, etc.).

  - **Pearson's correlation** measures the linear relationship between two variables.
  - **Spearman's rank correlation** measures how well the relationship between two variables can be described using a monotonic function (not necessarily linear).

  #### **Interpreting Correlation Values:**
  - **r = 1**: Perfect positive correlation — As the market index increases, the asset increases proportionally.
  - **r = -1**: Perfect negative correlation — As the market index increases, the asset decreases proportionally.
  - **r = 0**: No correlation — The asset and the market index move independently of each other.
  - **0 < r < 0.3**: Weak positive correlation — The asset and market index have a slight tendency to move in the same direction.
  - **0.3 < r < 0.7**: Moderate positive correlation — The asset and market index generally move in the same direction.
  - **0.7 < r < 1**: Strong positive correlation — The asset and market index have a strong tendency to move together.
  - **-0.3 < r < 0**: Weak negative correlation — The asset and market index tend to move in opposite directions, but weakly.
  - **-0.7 < r < -0.3**: Moderate negative correlation — The asset and market index generally move in opposite directions.
  - **-1 < r < -0.7**: Strong negative correlation — The asset and market index have a strong tendency to move in opposite directions.

  #### **P-Value:**
  The **P-value** helps you assess the significance of the correlation. A low P-value (typically < 0.05) indicates that the correlation is statistically significant, meaning it is unlikely to have occurred by chance.

  - **P-value < 0.05**: Strong evidence that the correlation is significant.
  - **P-value ≥ 0.05**: Weak evidence against the null hypothesis (no correlation).

  **Tip**: A strong correlation does not imply causality. Just because two variables are correlated, it doesn’t mean one is causing the other to move. Correlation merely shows a relationship between the variables.

  ### Volatility Ratio

  ### What is the Volatility Ratio?

  The **Volatility Ratio** helps assess the price fluctuations relative to a specific period. It calculates the difference between the **high** and **low** prices over a given period, then divides this range by the **low price**.

  This ratio helps identify periods of high volatility and is a key indicator for understanding market instability. The Volatility Ratio is particularly useful as it provides insights into how much the market is moving within the chosen timeframe.

  #### **Interpretation of the Volatility Ratio:**
  - A **high ratio** indicates high market volatility, which could represent a trading opportunity.
  - A **low ratio** suggests stability in the market, which may signal less risk.

  ## **What is Event-Based Analysis?**
  This section allows you to filter and analyse financial data based on **specific events** and **temporal patterns**...

  ## **Selecting the Right Event**
  Choose events from **macroeconomic indicators**, **earnings reports**, etc...

  ## **Monte Carlo Simulations**
  Monte Carlo simulations are used to predict the possible future prices of an asset by running many simulations based on a random process. Each simulation represents a possible price path based on the volatility of the asset.

  - **Mean Final Price**: This is the average final price after running all the simulations. It represents the central tendency of possible outcomes.
  - **Standard Deviation**: Measures how much the final prices deviate from the mean price, indicating uncertainty.
  - **10th and 90th Percentiles**: These percentiles represent the worst and best-case scenarios for the future price, based on the simulations.

  This method is widely used in financial modelling to help estimate the risk and potential return of investments under uncertainty.

  ## **Risk Adjusted Returns**
  Risk-adjusted returns help investors understand the profitability of an asset relative to the risk involved in investing in it. Here are two common metrics used

  ## **Volume vs ATR Correlation**
  **Volume vs ATR Correlation** measures the relationship between trading volume and volatility (as measured by the Average True Range). A higher correlation suggests that as trading volume increases, the asset’s price volatility also increases, and vice versa.

  - **Positive Correlation**: As volume increases, volatility increases. This could indicate that higher market participation or market-moving events are driving larger price fluctuations.
  - **Negative Correlation**: As volume increases, volatility decreases. This may suggest more stability in the market during periods of high trading activity.
  - **No Correlation**: No clear relationship between volume and volatility. Other factors may be influencing price movements.
