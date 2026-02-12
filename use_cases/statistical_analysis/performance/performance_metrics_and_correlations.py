# -------------------------------------------------------------------------------------------------
#  ---- pylint global exceptions ----
# Add any global disables if required (e.g., unused-import)
# -------------------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------------
# Docstring
# -------------------------------------------------------------------------------------------------
"""
This module contains functions for calculating and visualising key performance metrics and
correlations in financial data. These metrics are essential for evaluating the performance and
risk of assets, as well as understanding the relationships between different market variables.

Key functionalities include:
- annualised_return: Calculates the annualised return of an asset based on its historical data.
- max_drawdown: Computes the maximum drawdown, representing the largest peak-to-trough decline
  in the asset's value.
- volatility_adjusted_return: Measures the return per unit of risk (volatility) for the asset.
- roi: Calculates the return on investment (ROI), which measures the profitability of an asset.
- volume_vs_atr_correlation: Computes the correlation between trading volume and
ATR (Average True Range), providing insights into market volatility.
- pearsons_or_spearmans_correlation: Computes Pearson's or Spearman's correlation between an
asset and other market assets or indices, allowing users to understand asset relationships.
- generate_correlation_heatmap: Generates a heatmap to visualize the correlation between
a base asset and other selected assets.

The module also provides functions to handle correlations between user-uploaded assets and offers
visual and textual feedback to users, ensuring they can interpret and utilize these metrics
effectively.

Example usage:
    from performance_metrics_and_correlations import annualised_return, max_drawdown

    annualised_return(df, 'Interday')
    max_drawdown(df, 'Interday')
"""

# -------------------------------------------------------------------------------------------------
# Third-party Libraries
# -------------------------------------------------------------------------------------------------
import streamlit as st
import pandas as pd
import altair as alt
from scipy.stats import pearsonr, spearmanr

# -------------------------------------------------------------------------------------------------
# Function: check_timeline_for_performance
# Purpose: Validates that the selected timeline is 'Interday' before performing calculations.
# Use Case: Statistical Analysis / Performance Metrics & Correlations (Market & Volatility module)
# -------------------------------------------------------------------------------------------------
def check_timeline_for_performance(filtered_df, column, metric_name):
    """
    Check if the specified column is 'Interday' before performing a performance metric calculation.

    This function ensures that the column matches the 'Interday' timeline before proceeding.
    If the column does not match, it displays a warning and returns None, indicating that the
    metric cannot be calculated for the given column. If the column is 'Interday', it returns
    the filtered dataframe for further processing.

    Parameters:
    filtered_df (pandas.DataFrame): The dataframe containing the data to be checked.
    column (str): The name of the column representing the timeline (e.g., 'Interday').
    metric_name (str): The name of the metric being applied, used to display a warning message.

    Returns:
    pandas.DataFrame or None: The filtered dataframe if the column is 'Interday', or None if
    the column is not 'Interday'.
    """
    if column != 'Interday':
        st.warning(f"{metric_name} can only be applied to the 'Interday' timeline.")
        return None
    return filtered_df  # Return the dataframe if column is 'Interday'

# -------------------------------------------------------------------------------------------------
# Function: annualised_return
# Purpose: Quantifies the compounded annual growth rate of an asset over a specified period,
# accounting for the effects of time and compounding.
# Use Case: Statistical Analysis / Performance Metrics & Correlations (Market & Volatility module)
# -------------------------------------------------------------------------------------------------
def annualised_return(filtered_df, timeline):
    """
    Calculate the Annualised Return based on the filtered data and assigned timeline.
    """
    filtered_df = check_timeline_for_performance(filtered_df, timeline, "Annualised Return")
    if filtered_df is None:
        return None

    start_price = filtered_df['close'].iloc[0]
    end_price = filtered_df['close'].iloc[-1]
    years = (filtered_df['date'].iloc[-1] - filtered_df['date'].iloc[0]).days / 365.25

    return_rate = (end_price / start_price) ** (1 / years) - 1
    annualised_return_value = return_rate * 100  # Return as percentage

    # Display the result with Markdown in the same function
    st.subheader(f"**Annualised Return**: {annualised_return_value:.2f}%")
    st.markdown("""
    The **Annualised Return** represents the geometric average annual return of an
    asset over a period of time.
    It takes into account compounding and is useful for understanding the long-term
    performance of an investment.
    """)
    return annualised_return_value

# -------------------------------------------------------------------------------------------------
# Function: max_drawdown
# Purpose: Identifies the largest historical decline from peak to trough in asset value,
# serving as a proxy for worst-case loss and risk sensitivity.
# Use Case: Statistical Analysis / Performance Metrics & Correlations (Market & Volatility module)
# -------------------------------------------------------------------------------------------------
def max_drawdown(filtered_df, timeline):
    """
    Calculate the Maximum Drawdown based on the filtered data and assigned timeline.
    """
    filtered_df = check_timeline_for_performance(filtered_df, timeline, "Maximum Drawdown")
    if filtered_df is None:
        return None

    peak = filtered_df['close'].max()
    trough = filtered_df['close'].min()
    drawdown = (trough - peak) / peak

    # Display the Max Drawdown with Markdown
    st.subheader(f"**Maximum Drawdown**: {drawdown * 100:.2f}%")
    st.markdown("""
    The **Maximum Drawdown** represents the largest peak-to-trough decline in the value of
    an asset during the selected period. It gives investors an idea of the risk or potential
    loss they could have experienced.
    """)

    return drawdown * 100  # Return as percentage

# -------------------------------------------------------------------------------------------------
# Function: volatility_adjusted_return
# Purpose: Measures return efficiency by evaluating how much return is generated per unit of
# risk (volatility), providing a basic benchmark of return consistency.
# Use Case: Statistical Analysis / Performance Metrics & Correlations (Market & Volatility module)
# -------------------------------------------------------------------------------------------------
def volatility_adjusted_return(filtered_df, timeline):
    """
    Calculate Volatility-Adjusted Return based on filtered data.
    """
    filtered_df = check_timeline_for_performance(filtered_df,
    timeline, "Volatility-Adjusted Return")
    if filtered_df is None:
        return None

    # Calculate the average return (mean) and standard deviation (volatility)
    avg_return = filtered_df['close'].pct_change().mean()  # Average daily return
    volatility = filtered_df['close'].pct_change().std()  # Standard deviation of returns

    # Calculate the Volatility-Adjusted Return
    var_return = (avg_return / volatility) * 100  # Return as percentage

    # Display the Volatility-Adjusted Return with Markdown
    st.subheader(f"**Volatility-Adjusted Return**: {var_return:.2f}%")
    st.markdown("""
    The **Volatility-Adjusted Return** measures the return per unit of risk (volatility).
    It provides insight into how much return is achieved per unit of risk taken, with higher
    values indicating a better risk-adjusted return.
    """)

    return var_return  # Return as percentage

# -------------------------------------------------------------------------------------------------
# Function: roi
# Purpose: Calculates the net gain or loss on an investment relative to its initial cost,
# offering a direct, time-agnostic measure of profitability.
# Use Case: Statistical Analysis / Performance Metrics & Correlations (Market & Volatility module)
# -------------------------------------------------------------------------------------------------
def roi(filtered_df, timeline):
    """
    Calculate the Return on Investment (ROI) based on the filtered data and assigned timeline.
    This applies only for Interday data.
    """
    filtered_df = check_timeline_for_performance(filtered_df, timeline,
    "Return on Investment (ROI)")
    if filtered_df is None:
        return None

    # Use the 'close' column for prices (Interday data)
    start_price = filtered_df['close'].iloc[0]
    end_price = filtered_df['close'].iloc[-1]

    # Calculate ROI: (End Price - Start Price) / Start Price
    return_rate = (end_price - start_price) / start_price
    roi_percentage = return_rate * 100  # Return as percentage

    # Display the ROI value
    st.subheader(f"**Return on Investment (ROI)**: {roi_percentage:.2f}%")
    st.markdown("""
    The **Return on Investment (ROI)** measures the percentage gain or loss from an investment
    relative to its initial cost. It provides a simple way to assess the profitability
    of an investment.
    """)

    return roi_percentage  # Return ROI as percentage

# -------------------------------------------------------------------------------------------------
# Function: volume_vs_atr_correlation
# Purpose: Evaluates the relationship between trading volume and market volatility (ATR),
# helping assess how liquidity and price movement intensity are linked.
# Use Case: Statistical Analysis / Performance Metrics & Correlations (Market & Volatility module)
# -------------------------------------------------------------------------------------------------
def volume_vs_atr_correlation(processed_df, column):
    """
    Calculates the correlation between trading volume and ATR (Average True Range),
    and provides a message based on the correlation value.
    """
    if column != 'Interday':
        st.info("Volume vs ATR Correlation can only be applied to the 'Interday' timeline.")
        return None

    if 'volume' not in processed_df.columns or processed_df['volume'].isna().all() or \
       (processed_df['volume'] == 0).all():
        st.info("The selected dataset does not have completed 'volume' data, "
                "so Volume vs ATR Correlation is unavailable.")
        return None

    correlation = processed_df['volume'].corr(processed_df['ATR'])

    st.info(f"**Volume vs ATR Correlation**: {correlation:.2f}")

    if correlation > 0.7:
        st.markdown(f"**Strong Positive Correlation**: A correlation of {correlation:.2f} \
        suggests that as trading volume increases, volatility (ATR) tends to increase as well.")
    elif correlation > 0.3:
        st.markdown(f"**Moderate Positive Correlation**: A correlation of {correlation:.2f} \
        indicates a moderate relationship between volume and volatility.")
    elif correlation > -0.3:
        st.markdown(f"**Neutral/No Correlation**: A correlation of {correlation:.2f} \
        indicates no significant relationship between volume and ATR.")
    elif correlation > -0.7:
        st.markdown(f"**Weak Negative Correlation**: A correlation of {correlation:.2f} \
        indicates that as volume increases, volatility decreases slightly.")
    else:
        st.markdown(f"**Strong Negative Correlation**: A correlation of {correlation:.2f} \
        suggests that higher volume is associated with lower volatility.")

    return correlation


# -------------------------------------------------------------------------------------------------
# Function: pearsons_or_spearmans_correlation
# Purpose: Compute statistical correlations between asset returns and broader market benchmarks.
# Use Case: Statistical Analysis / Performance Metrics & Correlations (Market & Volatility module)
# -------------------------------------------------------------------------------------------------
# pylint: disable=W0613
def pearsons_or_spearmans_correlation(correlation_data_df, asset_df,
asset_column, method='pearson'):
    """
    Calculate the Pearson’s or Spearman’s correlation between the selected asset
    and other market assets (e.g., indices, equities, etc.).
    """
    try:
        asset_column_name = asset_column

        # Check if the asset column exists in correlation_df
        if asset_column_name not in correlation_data_df.columns:
            raise ValueError(f"Column '{asset_column_name}' not found in correlation_data_df. \
            Ensure that the asset column exists.")

        # Loop over each other asset column in correlation_df (those with '_return' in their name)
        for index_column in [col for col in correlation_data_df.columns if '_return' in col]:
            # Filter out rows where market index column has NaN or zero values
            valid_data = correlation_data_df[
                (correlation_data_df[asset_column_name].notna()) &
                (correlation_data_df[index_column].notna())
            ]
            valid_data = valid_data[
                (valid_data[asset_column_name] != 0) &
                (valid_data[index_column] != 0)
            ]

            # If there are not enough valid data points for correlation, skip the calculation
            if len(valid_data) < 2:
                st.write(f"Not enough valid data to compute correlation between {asset_column} "
                         f"and {index_column}")
                continue

            # Perform Pearson or Spearman correlation on the valid data
            if method == 'pearson':
                correlation, p_value = pearsonr(valid_data[asset_column_name],
                valid_data[index_column])
            elif method == 'spearman':
                correlation, p_value = spearmanr(valid_data[asset_column_name],
                valid_data[index_column])
            else:
                raise ValueError("Invalid method. Choose either 'pearson' or 'spearman'.")

            # Display results for each index
            st.write(f"**Correlation between {asset_column} and {index_column}**: "
                    f"{correlation:.2f}")
            st.write(f"P-value: {p_value:.4f}")

            # Message based on correlation strength
            explanation = get_correlation_explanation(correlation, asset_column, index_column)
            st.write(explanation)

    except ValueError as error:
        st.write(f"ValueError: {error}")

# -------------------------------------------------------------------------------------------------
# Function: pearsons_or_spearmans_correlation_user
# Purpose: Enable correlation analysis between user-uploaded asset return series.
# Use Case: Statistical Analysis / Performance Metrics & Correlations (Market & Volatility module)
# -------------------------------------------------------------------------------------------------
# pylint: disable=W0613
def pearsons_or_spearmans_correlation_user(correlation_df_user, asset_df,
asset_column, method='pearson'):
    """
    Calculate the Pearson’s or Spearman’s correlation between the selected user-uploaded assets.
    """
    try:
        asset_column_name = asset_column  # No _return added here, it's just the column name

        # Ensure the column exists in the cleaned user data
        if asset_column_name not in correlation_df_user.columns:
            raise ValueError(f"Column '{asset_column_name}' not found in correlation_df_user. \
            Ensure that the asset column exists.")

        # Loop over each other asset column in correlation_df (those with '_return' in their name)
        for index_column in [col for col in correlation_df_user.columns if '_return' in col]:
            # Filter out rows where market index column has NaN or zero values
            valid_data = correlation_df_user[
                (correlation_df_user[asset_column_name].notna()) &
                (correlation_df_user[index_column].notna())
            ]
            valid_data = valid_data[
                (valid_data[asset_column_name] != 0) &
                (valid_data[index_column] != 0)
            ]

            # If there are not enough valid data points for correlation, skip the calculation
            if len(valid_data) < 2:
                st.write(f"Not enough valid data to compute correlation between {asset_column} "
                         f"and {index_column}")
                continue

            # Perform Pearson or Spearman correlation on the valid data
            if method == 'pearson':
                correlation, p_value = pearsonr(valid_data[asset_column_name],
                valid_data[index_column])
            elif method == 'spearman':
                correlation, p_value = spearmanr(valid_data[asset_column_name],
                valid_data[index_column])
            else:
                raise ValueError("Invalid method. Choose either 'pearson' or 'spearman'.")

            # Display the correlation results
            st.write(f"**Correlation between {asset_column} and {index_column}**: "
                    f"{correlation:.2f}")
            st.write(f"P-value: {p_value:.4f}")

            explanation = get_correlation_explanation(correlation, asset_column_name, index_column)
            st.write(explanation)

    except ValueError as error:
        st.write(f"ValueError: {error}")

# -------------------------------------------------------------------------------------------------
# Function: get_correlation_explanation
# Purpose: Provide contextual interpretation of correlation values for asset relationships.
# Use Case: Statistical Analysis / Performance Metrics & Correlations (Market & Volatility module)
# -------------------------------------------------------------------------------------------------
# pylint: disable=R0911
def get_correlation_explanation(correlation, asset_column, index_column):
    """
    Provide an explanation based on the correlation between the asset and market index.

    Args:
        correlation (float): The correlation value between the asset and the market index.
        asset_column (str): The name of the asset column.
        index_column (str): The name of the market index column.

    Returns:
        str: An explanation of the correlation strength between the asset and market index.
    """
    if correlation == 1:
        return f"Perfect positive correlation: As the market index increases, {asset_column} \
        increases proportionally."

    if correlation == -1:
        return f"Perfect negative correlation: As the market index increases, {asset_column} \
        decreases proportionally."

    if correlation == 0:
        return f"No correlation: {asset_column} and the market index move independently."

    if 0 < correlation < 0.3:
        return f"Weak positive correlation: {asset_column} and the market index have a slight \
        tendency to move in the same direction."

    if 0.3 < correlation < 0.7:
        return f"Moderate positive correlation: {asset_column} and the market index generally \
        move in the same direction."

    if 0.7 < correlation < 1:
        return f"Strong positive correlation: {asset_column} and the market index have a strong \
        tendency to move together."

    if -0.3 < correlation < 0:
        return f"Weak negative correlation: {asset_column} and the market index tend to move in \
        opposite directions, but weakly."

    if -0.7 < correlation < -0.3:
        return f"Moderate negative correlation: {asset_column} and the market index generally \
        move in opposite directions."

    return f"Strong negative correlation: {asset_column} and the market index have a strong \
    tendency to move in opposite directions."

# -------------------------------------------------------------------------------------------------
# Function: generate_correlation_heatmap
# Purpose: Visually summarise correlation strengths between base asset and peer group.
# Use Case: Statistical Analysis / Performance Metrics & Correlations (Market & Volatility module)
# -------------------------------------------------------------------------------------------------
def generate_correlation_heatmap(correlation_df, asset_column):
    """
    Generate a Correlation Matrix Heatmap for visualizing the correlations between the base asset
    and other selected assets (Market Indices, SPDR Sectors, Countries, User Uploads).

    Parameters:
    correlation_df (pd.DataFrame): The DataFrame containing the correlation data.
    asset_column (str): The column name of the base asset (e.g., 'SPY' or 'Tesla').

    Returns:
    alt.Chart: The Altair chart object for the heatmap.
    """
    try:
        # Select the base asset and other relevant return columns
        relevant_columns = [asset_column] + [
            col for col in correlation_df.columns if '_return' in col
        ]

        # Subset the dataframe to include only the relevant columns (base asset and return columns)
        correlation_subset = correlation_df[relevant_columns]

        # Calculate the correlation matrix between the base asset and the other columns
        corr_matrix = correlation_subset.corr()

        # Melt the correlation matrix to long format for Altair
        corr_matrix_melted = corr_matrix.reset_index().melt(id_vars=['index'],
        var_name='Asset', value_name='Correlation')

        # Filter for rows where the 'index' is the base asset column
        corr_matrix_melted = corr_matrix_melted[corr_matrix_melted['index'] == asset_column]

        # Exclude the base asset from the 'Asset' column
        corr_matrix_melted = corr_matrix_melted[corr_matrix_melted['Asset'] != asset_column]

        # Sort by Correlation value (from high to low)
        corr_matrix_melted = corr_matrix_melted.sort_values(by='Correlation', ascending=False)

        # Create the heatmap using Altair, adjusting the size, color, and axis labels
        heatmap = alt.Chart(corr_matrix_melted).mark_rect().encode(
            x=alt.X('Asset:N', title='Correlated Asset', axis=alt.Axis(labelAngle=90)),
            y=alt.Y('index:N', title='Base Asset', axis=alt.Axis(labelAngle=0)),
            color=alt.Color('Correlation:Q', scale=alt.Scale(scheme='blues'), title='Correlation'),
            tooltip=[
                'Asset:N',
                alt.Tooltip('Correlation:Q', format='.2%', title='Correlation') # 2% decimal places
            ]
        ).properties(width=800, height=400)  # Adjusted chart size for better readability

        return heatmap

    except KeyError as key_error:
        st.write(f"Column error: {key_error}. Please check the column names in the dataframe.")
        return None
    except ValueError as value_error:
        st.write(f"Data error: {value_error}. Ensure the data is in the correct format.")
        return None
    except TypeError as type_error:
        st.write(f"Type error: {type_error}. Check the data types in the dataframe.")
        return None

# -------------------------------------------------------------------------------------------------
# Function: volatility_assets
# Purpose: Generate a structured comparison of volatility metrics across selected asset groupings.
# Use Case: Statistical Analysis / Performance Metrics & Correlations (Market & Volatility module)
# -------------------------------------------------------------------------------------------------
# pylint: disable=R0914
# pylint: disable=C0103
def volatility_assets(volatility_data_df, filtered_df, DATA_TITLE):
    """
    This function generates the volatility table for the selected base asset
    and the relevant asset groups.
    It handles various asset types (Equities, Commodities, Currencies, etc.) dynamically.
    """

    try:
        # Create an empty list to store the data for the table
        volatility_data = []

        # Loop through all columns that match '_ATR%' and '_STDdev%' in the merged data
        for column in volatility_data_df.columns:
            # Check if the column is for ATR or STDdev
            if '_ATR%' in column or '_STDdev%' in column:
                # Extract the financial asset name from the column
                financial_asset = column.replace('_ATR%', '').replace('_STDdev%', '')

                # Initialize the values for ATR, STDdev, and Rating
                sector_atr = None
                sector_stdev = None
                sector_rating = None

                # If the column is for ATR, extract the value
                if '_ATR%' in column:
                    # Extract the last valid ATR for this financial asset
                    valid_atr = volatility_data_df[column].dropna()
                    if not valid_atr.empty:
                        sector_atr = valid_atr.iloc[-1]  # Get the last valid value

                # Find the corresponding STDdev column
                sector_stdev_column = column.replace('_ATR%', '_STDdev%')
                if sector_stdev_column in volatility_data_df.columns:
                    # Extract the last valid STDdev for this financial asset
                    valid_stdev = volatility_data_df[sector_stdev_column].dropna()
                    if not valid_stdev.empty:
                        sector_stdev = valid_stdev.iloc[-1]

                # Find the volatility rating for this financial asset
                rating_column = f'{financial_asset}_rating'
                if rating_column in volatility_data_df.columns:
                    # Extract the last valid rating for this financial asset
                    valid_rating = volatility_data_df[rating_column].dropna()
                    if not valid_rating.empty:
                        sector_rating = valid_rating.iloc[-1]

                # Check if the ATR, STDdev, and Rating values are valid before adding them
                if pd.notna(sector_atr) and pd.notna(sector_stdev) and pd.notna(sector_rating):
                    # Add the data to the list for this financial asset
                    volatility_data.append([financial_asset, f"{sector_atr:.2f}",
                    f"{sector_stdev:.2f}", sector_rating])

        # Include the base asset data (e.g., dynamically pulled from DATA_TITLE)
        valid_base_asset_atr = volatility_data_df[f'{DATA_TITLE}_ATR%'].dropna()
        valid_base_asset_stdev = volatility_data_df[f'{DATA_TITLE}_STDdev%'].dropna()
        valid_base_asset_rating = volatility_data_df[f'{DATA_TITLE}_rating'].dropna()

        # Ensure base asset data is valid before appending to the table
        if (not valid_base_asset_atr.empty and
            not valid_base_asset_stdev.empty and
            not valid_base_asset_rating.empty):

            # Convert the list into a DataFrame for display
            volatility_df = pd.DataFrame(volatility_data, columns=['Asset', 'ATR', 'STDdev',
            'Volatility Rating'])

            # Display the resulting volatility comparison table
            st.dataframe(volatility_df)

    # pylint: disable=W0718
    except Exception:  # Catch duplicate column creation errors
        st.error(f"We cannot generate the volatility table. This may be due to the base \
        asset {DATA_TITLE} having membership with the chosen asset grouping. Please try another \
        base asset or select a different asset grouping and members \
        (e.g., ETF's Sectors and Technology).")

# -------------------------------------------------------------------------------------------------
# Function: volatility_assets_user
# Purpose: Generate volatility comparison tables from user-uploaded financial datasets.
# Use Case: Statistical Analysis / Performance Metrics & Correlations (Market & Volatility module)
# -------------------------------------------------------------------------------------------------
# pylint: disable=R0914
# pylint: disable=C0103
def volatility_assets_user(volatility_user_df, filtered_df, DATA_TITLE):
    """
    This function generates the volatility table for the selected base asset
    and the relevant asset groups.
    It handles various asset types (Equities, Commodities, Currencies, etc.) dynamically.
    """

    try:
        # Create an empty list to store the data for the table
        volatility_user = []

        # Loop through all columns that match '_ATR%' and '_STDdev%' in the merged data
        for column in volatility_user_df.columns:
            # Check if the column is for ATR or STDdev
            if '_ATR%' in column or '_STDdev%' in column:
                # Extract the financial asset name from the column
                financial_asset = column.replace('_ATR%', '').replace('_STDdev%', '')

                # Initialize the values for ATR, STDdev, and Rating
                sector_atr = None
                sector_stdev = None
                sector_rating = None

                # If the column is for ATR, extract the value
                if '_ATR%' in column:
                    # Extract the last valid ATR for this financial asset
                    valid_atr = volatility_user_df[column].dropna()
                    if not valid_atr.empty:
                        sector_atr = valid_atr.iloc[-1]  # Get the last valid value

                # Find the corresponding STDdev column
                sector_stdev_column = column.replace('_ATR%', '_STDdev%')
                if sector_stdev_column in volatility_user_df.columns:
                    # Extract the last valid STDdev for this financial asset
                    valid_stdev = volatility_user_df[sector_stdev_column].dropna()
                    if not valid_stdev.empty:
                        sector_stdev = valid_stdev.iloc[-1]

                # Find the volatility rating for this financial asset
                rating_column = f'{financial_asset}_rating'
                if rating_column in volatility_user_df.columns:
                    # Extract the last valid rating for this financial asset
                    valid_rating = volatility_user_df[rating_column].dropna()
                    if not valid_rating.empty:
                        sector_rating = valid_rating.iloc[-1]

                # Check if the ATR, STDdev, and Rating values are valid before adding them
                if pd.notna(sector_atr) and pd.notna(sector_stdev) and pd.notna(sector_rating):
                    # Add the data to the list for this financial asset
                    volatility_user.append([financial_asset, f"{sector_atr:.2f}",
                    f"{sector_stdev:.2f}", sector_rating])

        # Include the base asset data (e.g., dynamically pulled from DATA_TITLE)
        valid_base_asset_atr = volatility_user_df[f'{DATA_TITLE}_ATR%'].dropna()
        valid_base_asset_stdev = volatility_user_df[f'{DATA_TITLE}_STDdev%'].dropna()
        valid_base_asset_rating = volatility_user_df[f'{DATA_TITLE}_rating'].dropna()

        # Ensure base asset data is valid before appending to the table
        if (not valid_base_asset_atr.empty and
            not valid_base_asset_stdev.empty and
            not valid_base_asset_rating.empty):

            # Convert the list into a DataFrame for display
            volatility_user_df = pd.DataFrame(volatility_user, columns=['Asset', 'ATR', 'STDdev',
            'Volatility Rating'])

            # Display the resulting volatility comparison table
            st.dataframe(volatility_user_df)

    # pylint: disable=W0718
    except Exception:  # Catch duplicate column creation errors
        st.error(f"We cannot generate the volatility table. This may be due to the base \
        asset {DATA_TITLE} having membership with the chosen asset grouping. Please try another \
        base asset or select a different asset grouping and members \
        (e.g., ETF's Sectors and Technology).")

# -------------------------------------------------------------------------------------------------
# Performance and Correlation Function Mapping
# -------------------------------------------------------------------------------------------------
options_performance_and_correlation_map = {
    'Annualised Return': annualised_return,
    'Maximum Drawdown': max_drawdown,
    'Volatility-Adjusted Return': volatility_adjusted_return,
    'Return on Investment (ROI)': roi,
    'Volume vs ATR Correlation': volume_vs_atr_correlation,

    # map other options to their corresponding functions here...
}
