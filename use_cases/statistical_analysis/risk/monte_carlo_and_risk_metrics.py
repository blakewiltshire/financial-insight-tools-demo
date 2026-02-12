# -------------------------------------------------------------------------------------------------
#  ---- pylint global exceptions ----
# Add any global disables if required (e.g., unused-import)
# -------------------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------------
# Docstring
# -------------------------------------------------------------------------------------------------
"""
This module contains functions for performing Monte Carlo simulations and calculating various
risk-adjusted performance metrics. The functions in this module are used to simulate future price
movements, evaluate risk-adjusted returns, and assess the probability of achieving specific
profit targets.

Functions in this module include:
- `monte_carlo_simulations`: Performs Monte Carlo simulations to forecast future asset prices based
  on historical data. The function simulates price movements using a random walk and visualizes the
  results using a line chart.
- `risk_adjusted_returns`: Calculates the Sharpe Ratio, which measures the risk-adjusted
return of an asset using the specified column of data.
- `sortino_ratio`: Calculates the Sortino Ratio, a variation of the Sharpe Ratio that uses downside
  deviation as a measure of risk, focusing on negative volatility.
- `calculate_probability_of_dpt`: Calculates the probability of hitting a
Desired Profit Target (DPT) based on historical data, filtered by direction ('Up' or 'Down')
and the selected timeline column.

These functions provide insights into the potential future performance and risk of an asset,
enabling investors to assess the likelihood of achieving specific financial goals.

Example usage:
    from monte_carlo_and_risk_metrics import monte_carlo_simulations, risk_adjusted_returns

    monte_carlo_simulations(df, 'column_name')
    risk_adjusted_returns(df, 'column_name')
"""

# -------------------------------------------------------------------------------------------------
# Third-party Libraries
# -------------------------------------------------------------------------------------------------
from fractions import Fraction
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# -------------------------------------------------------------------------------------------------
# Function: monte_carlo_simulations
# Purpose: Simulate future asset price paths based on historical volatility to model outcome
# uncertainty under a random walk framework.
# Use Case: Statistical Analysis / Risk and Uncertainty (Market & Volatility module)
# -------------------------------------------------------------------------------------------------
# pylint: disable=R0914
def monte_carlo_simulations(processed_df, column):
    """
    Perform Monte Carlo simulations to forecast future asset prices based on historical data.

    This function simulates future price movements using a random walk, with volatility
    taken from the asset's historical returns. It runs a specified number of simulations
    and visualizes the results using a line chart.

    Parameters:
        processed_df (DataFrame): The processed DataFrame containing asset
        data (including 'close').
        column (str): The name of the column containing the data to base
        the simulation on (e.g., 'Interday').

    Returns:
        None: Displays a chart and simulation results.
    """

    # Ensure the column is 'Interday' and filter based on the timeline
    if column != 'Interday':
        st.warning("Monte Carlo Simulations can only be applied to the 'Interday' timeline.")
        return  # Exit the function if the timeline is not 'Interday'

    # Slider for number of simulations (default is 100, range from 50 to 500)
    num_simulations = st.sidebar.slider("Number of Monte Carlo Simulations", min_value=50,
                                        max_value=500, value=100, step=50)

    # Set parameters for the Monte Carlo simulation
    trading_days = 252  # Number of trading days (252 trading days in a year)

    # Use the 'close' column for the actual price data
    initial_price = processed_df['close'].iloc[-1]  # Last actual closing price
    daily_vol = processed_df[column].std()  # Volatility from the percentage changes

    # Prepare for storing the simulations results (using a list to collect all simulations)
    all_simulations = []

    # Run Monte Carlo simulations
    for _ in range(num_simulations):  # Ignoring the unused 'simulation_index'
        price_list = [initial_price]
        for _ in range(trading_days):  # Ignoring the unused 'day_index'
            # Simulate next day's price
            price = price_list[-1] * (1 + np.random.normal(0, daily_vol))
            price_list.append(price)

        # Instead of assigning directly to df, append each simulation to the list
        all_simulations.append(price_list)

    # Convert the list of simulations into a DataFrame once, after all simulations are complete
    df_simulations = pd.DataFrame(all_simulations).transpose()

    # Create Plotly chart for visualization
    fig = go.Figure()
    for _ in range(num_simulations):  # Ignoring the unused 'i'
        fig.add_trace(go.Scatter(x=np.arange(trading_days + 1), y=df_simulations[_], mode='lines',
                                opacity=0.2, line={'width': 1}))  # Using dict literal

    # Layout settings for the plot
    fig.update_layout(
        title="Monte Carlo Simulation of Future Prices",
        xaxis_title="Days",
        yaxis_title="Price",
        showlegend=False
    )

    # Display the plot in Streamlit
    st.plotly_chart(fig)

    # Calculate the key statistics
    mean_price = df_simulations.iloc[-1].mean()
    std_dev_price = df_simulations.iloc[-1].std()
    percentile_90 = np.percentile(df_simulations.iloc[-1], 90)
    percentile_10 = np.percentile(df_simulations.iloc[-1], 10)

    # Monte Carlo Simulation Results
    st.write("**Monte Carlo Simulation Results**")

    # Metrics display with enhanced descriptions
    st.write(f"**Mean Final Price**: {mean_price:.2f}")
    st.write(":gray[*(The average expected price based on the simulation. This represents \
    the central tendency of the possible outcomes.)*]")
    st.write(f"**Standard Deviation of Final Prices**: {std_dev_price:.2f}")
    st.write(":gray[*(Indicates the variability or spread of the simulated end prices. \
    A higher value suggests more uncertainty.)*]")

    st.write(f"**90th Percentile of Final Prices**: {percentile_90:.2f}")
    st.write(":gray[*(The 90th percentile represents the price below which 90% of the \
    simulations fall. This gives an idea of the best-case scenario.)*]")
    st.write(f"**10th Percentile of Final Prices**: {percentile_10:.2f}")
    st.write(":gray[*(The 10th percentile represents the price below which 10% of the \
    simulations fall. This gives an idea of the worst-case scenario.)*]")

    # Add a comparison between the last price and the mean final price to show if
    # there's an upward or downward bias.
    current_price = processed_df['close'].iloc[-1]
    price_diff = mean_price - current_price
    st.write(f"**Current Price**: {current_price:.2f}")
    st.write(f"**Difference from Mean Final Price**: {price_diff:.2f} "
             f"({'Up' if price_diff > 0 else 'Down'} from current price)")

# -------------------------------------------------------------------------------------------------
# Function: risk_adjusted_returns
# Purpose: Evaluate return per unit of total risk using the Sharpe Ratio for portfolio or trade review.
# Use Case: Statistical Analysis / Risk and Uncertainty (Market & Volatility module)
# -------------------------------------------------------------------------------------------------
def risk_adjusted_returns(processed_df, column):
    """
    Calculate the Sharpe Ratio to evaluate the risk-adjusted return for Interday data.

    Parameters:
    - processed_df (pd.DataFrame): The DataFrame containing the asset's returns.
    - column (str): The column name containing the return data.

    Returns:
    - dict: A dictionary containing sharpe_ratio, mean_return, and std_dev for snapshot export.
    """

    # Ensure the column is 'Interday' and filter based on the timeline
    if column != 'Interday':
        st.warning("Sharpe Ratio can only be applied to the 'Interday' timeline.")
        return

    # Slider for Risk-Free Rate
    risk_free_rate = st.sidebar.slider("Sharpe Ratio Risk-Free Rate (%)", min_value=0.0,
        max_value=10.0, value=0.0, step=0.1)

    returns = processed_df[column]

    # Compute metrics
    mean_return = returns.mean()
    std_dev = returns.std()

    if std_dev == 0:
        st.error("Standard deviation is zero — Sharpe Ratio is undefined.")
        return

    sharpe_ratio = (mean_return - (risk_free_rate / 100)) / std_dev  # Convert risk-free rate to decimal

    # Display outputs
    st.write(f"**Sharpe Ratio**: {sharpe_ratio:.2f}")
    st.write(":gray[*(The Sharpe Ratio measures the return per unit of total risk. "
             "The risk-free rate represents the baseline return for comparison.)*]")

    st.write(f"**Mean Daily Return**: {mean_return:.4f}")
    st.write(f"**Standard Deviation (Risk)**: {std_dev:.4f}")

    if sharpe_ratio > 1:
        st.success("The Sharpe Ratio is positive, indicating good risk-adjusted performance.")
    else:
        st.warning("The Sharpe Ratio is low or negative, indicating poor risk-adjusted performance.")

    # ✅ Return JSON snapshot block
    return {
        "sharpe_ratio": round(sharpe_ratio, 4),
        "mean_daily_return": round(mean_return, 6),
        "standard_deviation": round(std_dev, 6),
        "risk_free_rate_input_pct": round(risk_free_rate, 2)
    }

# -------------------------------------------------------------------------------------------------
# Function: sortino_ratio
# Purpose: Evaluate return per unit of downside risk using the Sortino Ratio for a more loss-sensitive
# assessment of risk-adjusted returns.
# Use Case: Statistical Analysis / Risk and Uncertainty (Market & Volatility module)
# -------------------------------------------------------------------------------------------------
def sortino_ratio(processed_df, column):
    """
    Calculate the Sortino Ratio, which is a variation of the Sharpe Ratio that
    uses downside deviation.

    Parameters:
    - processed_df (pd.DataFrame): The DataFrame containing the asset's returns.
    - column (str): The column name containing the return data.

    Returns:
    - dict: A dictionary containing sortino_ratio, mean_return, downside_deviation,
      and the target return used, for JSON snapshot export.
    """
    # Ensure the column is 'Interday' and filter based on the timeline
    if column != 'Interday':
        st.warning("Sortino Ratio can only be applied to the 'Interday' timeline.")
        return

    # Slider for Target Return (customized for Sortino Ratio)
    target_return = st.sidebar.slider(
        "Sortino Ratio Target Return (%)",
        min_value=-50.0, max_value=50.0, value=0.0, step=1.0
    )

    # Use the percentage change directly
    returns = processed_df[column]

    # Calculate mean return
    mean_return = returns.mean()

    # Calculate downside deviation
    downside_returns = returns[returns < (target_return / 100)]  # Convert to decimal
    downside_deviation = downside_returns.std()

    # Calculate Sortino Ratio
    if downside_deviation != 0:
        calculated_sortino_ratio = (mean_return - (target_return / 100)) / downside_deviation
    else:
        calculated_sortino_ratio = np.nan

    # Display the Sortino Ratio
    st.write(f"**Sortino Ratio**: {calculated_sortino_ratio:.2f}")
    st.write(":gray[*(The Sortino Ratio measures the return per unit of downside risk. "
             "It only considers negative volatility, which is useful for investors "
             "concerned about losses.)*]")

    st.write(f"**Mean Daily Return**: {mean_return:.4f}")
    st.write(f"**Downside Deviation (Risk)**: {downside_deviation:.4f}")

    if calculated_sortino_ratio > 1:
        st.success("The Sortino Ratio is positive, indicating good risk-adjusted "
                   "performance based on downside risk.")
    else:
        st.warning("The Sortino Ratio is low or negative, indicating poor risk-adjusted "
                   "performance based on downside risk.")

    # ✅ Return JSON snapshot block
    return {
        "sortino_ratio": round(calculated_sortino_ratio, 4) if not np.isnan(calculated_sortino_ratio) else None,
        "mean_daily_return": round(mean_return, 6),
        "downside_deviation": round(downside_deviation, 6),
        "target_return_input_pct": round(target_return, 2)
    }

# -------------------------------------------------------------------------------------------------
# Function: calculate_probability_of_dpt_advanced
# Purpose: Calculate empirical probabilities of achieving specific profit targets (DPT) based on past
# directional moves to aid probabilistic expectation setting.
# Use Case: Statistical Analysis / Risk and Uncertainty (Market & Volatility module)
# -------------------------------------------------------------------------------------------------
# pylint: disable=too-many-locals
def calculate_probability_of_dpt_advanced(
    processed_df,
    column,
    direction,
    desired_profit_target,
    filtered_df=None,
    return_json=False
):
    """
    Calculate the probability of hitting the Desired Profit Target (DPT) based on direction
    and timeline column. Optionally return a structured dictionary for JSON export.

    Parameters:
        processed_df (DataFrame): Full dataset.
        column (str): Target return column ('Interday', etc.).
        direction (str): 'Up' or 'Down'.
        desired_profit_target (float): DPT % value.
        filtered_df (DataFrame, optional): Date-filtered subset.
        return_json (bool): If True, return dictionary instead of tuple.

    Returns:
        tuple or dict: If return_json=False, returns:
            (target_decimal, occurrences, count, probability, rounded_probability,
             probability_fraction, fraction_approx, approximate_readable)
        Else returns a structured dictionary for JSON output.
    """
    # Convert DPT to decimal
    target_decimal = desired_profit_target / 100

    # Use filtered or full data
    data_to_use = filtered_df if filtered_df is not None else processed_df

    # Directional filtering
    if direction == 'Up':
        dtp_filtered_data = data_to_use[data_to_use[column] >= target_decimal]
    elif direction == 'Down':
        dtp_filtered_data = data_to_use[data_to_use[column] <= -target_decimal]
    else:
        raise ValueError("Direction must be 'Up' or 'Down'.")

    occurrences = int(len(dtp_filtered_data))
    count = int(data_to_use[column].count())

    # Probability calculations
    probability = (occurrences / count) * 100 if count > 0 else 0
    rounded_probability = round(probability)
    probability_fraction = Fraction(occurrences, count) if count > 0 else Fraction(0, 1)
    fraction_approx = probability_fraction.limit_denominator(100)
    approximate_readable = round(1 / (occurrences / count)) if occurrences > 0 else 0

    # ✅ Return JSON snapshot block
    if return_json:
        return {
            "selected_dpt_pct": round(desired_profit_target, 2),
            "direction": direction,
            "timeline": column,
            "estimated_hit_ratio": f"1 in {approximate_readable}" if approximate_readable > 0 else "N/A",
            "occurrences": int(occurrences),
            "total_observations": int(count)
        }

    # Default full tuple return
    return (
        target_decimal, occurrences, count, probability, rounded_probability,
        probability_fraction, fraction_approx, approximate_readable
    )

# -------------------------------------------------------------------------------------------------
# Risk & Uncertainty Function Mapping
# -------------------------------------------------------------------------------------------------
options_risk_and_uncertainty_map = {
    'Monte Carlo Simulations': monte_carlo_simulations,
    'Risk-Adjusted Returns (Sharpe Ratio)': risk_adjusted_returns,
    'Downside Risk Measure (Sortino Ratio)': sortino_ratio,
    'Probability of Hitting DPT': calculate_probability_of_dpt_advanced
    # map other options to their corresponding functions here...
}
