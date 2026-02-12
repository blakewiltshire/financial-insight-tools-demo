# -------------------------------------------------------------------------------------------------
#  ---- pylint global exceptions ----
# Add any global disables if required (e.g., unused-import)
# -------------------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------------
# Docstring
# -------------------------------------------------------------------------------------------------
"""
visualisations.py

This module contains various functions for generating and displaying visualizations
related to financial data. It includes charts for price movement, returns, volatility,
and other metrics based on data processed for different timeframes (e.g., Interday, Weekly).

Functions include:
- Line charts
- Candlestick charts
- Area charts
- Temporal returns
- Risk-return scatter plots
- User-uploaded data visualizations

This module utilises Streamlit for displaying the charts and Plotly/Altair for chart generation.

Import required libraries:
- pandas
- plotly.express
- altair
- streamlit

Module designed to support the analysis and visualization of asset returns and their relationships
with volatility and other financial metrics.

"""
# -------------------------------------------------------------------------------------------------
# Third-party Libraries
# -------------------------------------------------------------------------------------------------
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px

# -------------------------------------------------------------------------------------------------
# Mapping of timelines to column names
# -------------------------------------------------------------------------------------------------
column_map = {
    'Intraday': 'Intraday',
    'Overnight': 'Overnight',
    'Interday': 'Interday',
    'Daily H-L': 'Daily H-L'
}

# -------------------------------------------------------------------------------------------------
# Return column name
# -------------------------------------------------------------------------------------------------
def get_column(timeline, time_period='weekly'):
    """
    Returns the appropriate column name ('close') based on the timeline.

    Parameters:
    timeline (str): The timeline type ('Interday' expected).
    time_period (str, optional): The period for return calculation (default is 'weekly').

    Returns:
    str: 'close' if timeline is 'Interday', else None.
    """
    # Apply info message if the timeline isn't 'Interday'
    if timeline != 'Interday':
        st.warning(f"{time_period.capitalize()} Return Chart can only be applied to \
        the 'Interday' timeline.")
        return None  # Return None to prevent any charting if not 'Interday'

    # Return 'close' for Interday timeline
    return 'close'

# --- Chart Configuration - Returns ---
def chart_returns(return_df, time_period='weekly', timeline='Interday', filtered_df=None):
    """Generate a chart for the selected return period (weekly, monthly, etc.)
    with timeline check."""

    # Check if the timeline is 'Interday' before proceeding
    column = get_column(timeline, time_period)  # Get the correct column based on timeline
    if column is None:
        return None  # Exit if the timeline isn't 'Interday'

    # Apply filtering if 'filtered_df' is provided (e.g., from Range etc)
    if filtered_df is not None:
        return_df = filtered_df  # Use the filtered dataframe

    # Ensure the column name used is dynamic
    if time_period == 'weekly':
        return_col = 'weekly_return'
    elif time_period == 'monthly':
        return_col = 'monthly_return'
    elif time_period == 'quarterly':
        return_col = 'quarterly_return'
    elif time_period == 'halfyearly':
        return_col = 'six_month_return'
    elif time_period == 'yearly':
        return_col = 'yearly_return'
    else:
        raise ValueError(f"Unsupported time period: {time_period}")

    # Create a bar chart for return periods
    chart = px.bar(
        return_df, x="date",
        y=return_col,
        title=f'{time_period.capitalize()} Return Chart'
    )

    # Customise layout
    chart.update_layout(
        xaxis_title="Date",
        yaxis_title=f"{time_period.capitalize()} Return (%)",
        template="plotly_dark"
    )

    return chart

# --- Scatterplot Chart - ATR - DPT ---
# pylint: disable=W0613
def scatterplot_dpt_vs_volatility(processed_df, direction, desired_profit_target,
period='1d', temporal_filter=None):
    """Generate a scatter plot showing the relationship between ATR and DPT achievement."""
    # Dynamically generate ATR column name based on the selected period
    atr_column = f'{period}_atr'
    dpt_column = 'DPT_achieved'

    # Ensure that both ATR and DPT_achieved columns exist
    if atr_column not in processed_df.columns or dpt_column not in processed_df.columns:
        raise ValueError(
            f"Required columns '{atr_column}' or '{dpt_column}' are missing from the data."
        )

    # Filter data based on direction (up or down)
    if direction == "Up":
        filtered_df = processed_df[processed_df['Interday'] > 0]
    elif direction == "Down":
        filtered_df = processed_df[processed_df['Interday'] < 0]
    else:
        filtered_df = processed_df

    # Apply temporal filtering if specified (only for Temporal Patterns)
    if temporal_filter:
        filtered_df = filtered_df[filtered_df['period'] == temporal_filter]

    # Filter the data for ATR > 0% (optional)
    filtered_df = filtered_df[filtered_df[atr_column] > 0]

    # Make DPT Achieved more readable (e.g., as percentages)
    filtered_df[dpt_column] = filtered_df[dpt_column].apply(lambda x: round(x * 100, 2))

    # Create scatter plot using Plotly
    fig = px.scatter(filtered_df,
                     x=atr_column,
                     y=dpt_column,
                     title=f'Volatility vs DPT Achievement (Period: {period})',
                     labels={atr_column: 'ATR (%)', dpt_column: 'DPT Achieved (%)'},
                     hover_data=['date', atr_column, dpt_column])

    return fig

# --- Line Chart - Returns ---
def line(processed_df, timeline):
    """
    Visualises price movement using a line chart for the 'Interday' timeline.

    Parameters:
    processed_df (pd.DataFrame): The DataFrame containing the asset data.
    timeline (str): The timeline type ('Interday' expected).

    Returns:
    None: Displays the line chart if valid, otherwise does nothing.
    """

    # Check if timeline is 'Interday'
    if timeline != 'Interday':
        st.warning("Price Movement & Trend Visualisation (Line Chart) can only be applied \
        to the 'Interday' timeline.")
        return  # Exit the function if the timeline is not 'Interday'

    column = get_column(timeline)  # This will always return 'close'
    st.write('**Price Movement Visualisation**')
    st.write('You have selected: Line Chart')

    line_base = alt.Chart(processed_df).encode(
        alt.X('date:T',
              axis=alt.Axis(
                  format='%m/%d/%y',
                  labelAngle=-45,
                  title='Date'
              )
        )
    )

    # Plot the 'close' value on the y-axis for the selected timeline
    line_chart = line_base.mark_line().encode(
        alt.Y(f'{column}:Q', title='Close Price')  # Dynamically use 'close' column
    )

    st.altair_chart(line_chart, theme="streamlit", width='stretch')

# --- Candlestick Chart - Returns ---
def candlestick(processed_df, timeline, use_filtered_data=False):
    """
    Visualises price movement with a candlestick chart for the 'Interday' timeline.

    Parameters:
    processed_df (pd.DataFrame): The DataFrame containing the asset data.
    timeline (str): The timeline type ('Interday' expected).
    use_filtered_data (bool, optional): Whether to use filtered data (default is False).

    Returns:
    None: Displays the candlestick chart if valid, otherwise does nothing.
    """

    # Check if timeline is 'Interday'
    if timeline != 'Interday':
        st.warning("Price Movement & Trend Visualisation (Candlestick Chart) can only be \
        applied to the 'Interday' timeline.")
        return  # Exit the function if the timeline is not 'Interday' (no return value needed)

    column = get_column(timeline)  # This will always return 'close'
    st.write('**Price Movement Visualisation**')
    st.write('You have selected: Candlestick Chart')

    # Get the current date and calculate the date 3 months ago
    current_date = pd.to_datetime(processed_df['date'].iloc[-1])
    three_months_ago = current_date - pd.DateOffset(months=3)

    # Use filtered data if required, otherwise use the full dataset
    if use_filtered_data:
        filtered_df = processed_df[processed_df['date'] >= three_months_ago]
        st.write('Showing last 3 months of price data.')
    else:
        filtered_df = processed_df
        st.write('Showing full dataset of price data.')

    # Define the open/close color logic for candlestick chart
    open_close_color = alt.condition("datum.open <= datum.close",
                                     alt.value("#06982d"),
                                     alt.value("#ae1325"))

    # Base chart for candlestick
    base = alt.Chart(filtered_df).encode(
        alt.X('date:T',
              axis=alt.Axis(
                  format='%m/%d',
                  labelAngle=-45,
                  title='Date'
              )
        ),
        color=open_close_color
    )

    rule = base.mark_rule().encode(
        alt.Y(
            'low:Q',
            title='Price',
            scale=alt.Scale(zero=False),
        ),
        alt.Y2(f'{column}:Q')  # Plot the 'close' column for price movement
    )

    # Renaming bar to candlestick_bar to avoid conflict with 'bar'
    candlestick_bar = base.mark_bar().encode(
        alt.Y('open:Q'),
        alt.Y2(f'{column}:Q')
    )

    candlestick_chart = rule + candlestick_bar

    st.altair_chart(candlestick_chart, theme=None, width='stretch')

# --- Area Chart - Returns ---
def area(processed_df, timeline):
    """
    Visualises trend using an area chart for the 'Interday' timeline.

    Parameters:
    processed_df (pd.DataFrame): The DataFrame containing the asset data.
    timeline (str): The timeline type ('Interday' expected).

    Returns:
    None: Displays the area chart if valid, otherwise does nothing.
    """
    # Check if timeline is 'Interday'
    if timeline != 'Interday':
        st.warning("Price Movement & Trend Visualisation (Area Chart) can only be applied \
        to the 'Interday' timeline.")
        return  # Exit the function if the timeline is not 'Interday' (no return value needed)

    column = get_column(timeline)  # This will always return 'close'
    st.write('**Trend Visualisation**')
    st.write('You have selected: Area Chart')

    area_base = alt.Chart(processed_df).encode(
        alt.X('date:T',
              axis=alt.Axis(
                  format='%m/%d/%y',
                  labelAngle=-45,
                  title='Date'
              )
        )
    )

    # Plot the 'close' value on the y-axis for the selected timeline
    area_chart = area_base.mark_area().encode(
        alt.Y(f'{column}:Q', title='Close Price')  # Dynamically use 'close' column
    )

    st.altair_chart(area_chart, theme="streamlit", width='stretch')

# --- Bar Chart - Returns ---
def range_returns(processed_df, timeline, filtered_df=None):
    """
    Generate a bar chart for returns based on filtered data (Range, and Event-Based Analysis).
    """
    st.write('Returns')
    st.write('You have selected: Bar Charts')

    # Check if the timeline is 'Interday'
    if timeline != 'Interday':
        st.info("Returns can only be applied to the 'Interday' timeline.")
        return  # Exit the function if the timeline is not 'Interday'

    # Use the filtered dataframe if provided
    return_df = filtered_df if filtered_df is not None else processed_df

    # Compute the percentage change for the 'close' price
    return_df['return'] = return_df['close'].pct_change() * 100

    # Create a bar chart for returns over time
    chart = px.bar(
        return_df, x="date", y="return",
        title=f'Returns Chart ({timeline})',
        labels={"return": "Percentage Change (%)", "date": "Date"}
    )

    # Customise layout for better visualisation
    chart.update_layout(
        xaxis_title="Date",
        yaxis_title="Return (%)",
        template="plotly_dark"
    )

    st.plotly_chart(chart, theme="streamlit", width='stretch')

# --- Bar Chart - Temporal Patterns ---
def temporal_returns(filtered_df, timeline, selected_pattern):
    """
    Calculates and Visualises temporal returns based on the selected pattern
    ('Week', 'Month', etc.).

    Parameters:
    filtered_df (pd.DataFrame): The DataFrame containing the asset data.
    timeline (str): The timeline type ('Interday' expected).
    selected_pattern (str): The selected temporal pattern for returns calculation
    ('Week', 'Month', etc.).

    Returns:
    None: Displays a bar chart of average returns by the selected pattern.
    """

    # Check if the timeline is 'Interday'
    if timeline != 'Interday':
        st.info("Temporal Returns can only be applied to the 'Interday' timeline.")
        return  # Exit the function if the timeline is not 'Interday'

    # Make sure filtered_df is a valid DataFrame
    if filtered_df is None or filtered_df.empty:
        st.warning("No valid data available.")
        return  # Exit if no valid data

    return_df = filtered_df.copy()

    # Calculate percentage change (returns) based on 'close' price
    return_df['return'] = return_df['close'].pct_change() * 100

    # Handle Temporal Pattern: Weekly, Monthly, etc.
    if selected_pattern == "Week":
        return_df['week'] = return_df['date'].dt.isocalendar().week  # Add week number
        return_df = return_df[return_df['week'] != 53]  # Remove Week 53 from data
        grouped_df = return_df.groupby('week', observed=False).agg(
        {'return': 'mean'}).reset_index()
        grouped_df['period'] = grouped_df['week'].astype(str)  # Create period column

    elif selected_pattern == "Month":
        return_df['month'] = return_df['date'].dt.month  # Add month
        grouped_df = return_df.groupby('month', observed=False).agg(
        {'return': 'mean'}).reset_index()
        grouped_df['period'] = return_df['month'].apply(lambda x: pd.to_datetime(x,
        format='%m').strftime('%B'))

    elif selected_pattern == "Weekday":
        weekday_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday",
        "Saturday", "Sunday"]
        return_df['weekday'] = return_df['date'].dt.day_name()  # Add weekday
        return_df['weekday'] = pd.Categorical(return_df['weekday'],
        categories=weekday_order, ordered=True)
        grouped_df = return_df.groupby('weekday', observed=False).agg(
        {'return': 'mean'}).reset_index()
        grouped_df['period'] = grouped_df['weekday']

    elif selected_pattern == "Season":
        season_order = ['Winter', 'Spring', 'Summer', 'Autumn'] # Add season
        return_df['season'] = return_df['date'].apply(
            lambda x: 'Winter' if x.month in [12, 1, 2] else
                  'Spring' if x.month in [3, 4, 5] else
                  'Summer' if x.month in [6, 7, 8] else 'Autumn'
          )

        return_df['season'] = pd.Categorical(return_df['season'],
        categories=season_order, ordered=True)
        grouped_df = return_df.groupby('season', observed=False).agg(
        {'return': 'mean'}).reset_index()
        grouped_df['period'] = grouped_df['season']

    elif selected_pattern == "Business Quarter":
        return_df['quarter'] = return_df['date'].dt.to_period('Q')  # Add quarter
        grouped_df = return_df.groupby('quarter', observed=False).agg(
        {'return': 'mean'}).reset_index()
        grouped_df['period'] = grouped_df['quarter'].astype(str)

    else:
        st.warning("Unsupported Temporal Pattern")
        return  # Exit if unsupported temporal pattern

    # Format the returns as percentages (round to 2 decimal places)
    grouped_df['return'] = grouped_df['return'].round(2)

    # Create a bar chart for returns over the temporal periods
    chart = px.bar(
        grouped_df, x="period", y="return",
        title=f'Average Returns by {selected_pattern}',
        labels={"return": "Average Return (%)", "period": selected_pattern}
    )

    # Customise the hover template to display percentage values with % sign
    chart.update_traces(hovertemplate='%{y}%')  # Display values as percentages on hover

    # Customise layout for better visualisation
    chart.update_layout(
        xaxis_title=selected_pattern,
        yaxis_title="Average Return (%)",
        template="plotly_dark"
    )

    st.plotly_chart(chart, theme="streamlit", width='stretch')

# --- Bar Chart - User Upload Returns ---
def user_returns(correlation_user_returns_df, asset_column):
    """
    Visualise the User Uploaded returns.
    """
    try:
        # Ensure the asset_column (e.g., 'SPY_return') exists in the dataframe
        if asset_column not in correlation_user_returns_df.columns:
            raise ValueError(f"Column '{asset_column}' not found in \
            correlation_indices_returns_df. Ensure that the asset column exists.")

        # Get the list of return columns (including Tesla's return and other market returns)
        return_columns = [col for col in correlation_user_returns_df.columns if '_return' in col]

        # Convert 0 returns to None (NaN) for proper averaging
        correlation_user_returns_df[
        asset_column] = correlation_user_returns_df[asset_column].where(
        correlation_user_returns_df[asset_column] != 0, None)

        # Aggregate the data (average returns for each market index)
        agg_returns = correlation_user_returns_df[return_columns].mean().reset_index()
        agg_returns.columns = ['Market', 'Average Return (%)']

        # Format returns for display (rounded to 2 decimal places for clarity)
        def format_return(value):
            # Display as percentage with 2 decimal places
            return f'{value * 100:.2f}%'  # Show as percentage

        agg_returns['Average Return (%)'] = agg_returns['Average Return (%)'].apply(format_return)

        # Create a bar chart for average returns
        chart = px.bar(
            agg_returns, x="Market", y="Average Return (%)",
            title=f'User Uploads Average Returns ({asset_column})',
            labels={"Market": "User Uploads Index", "Average Return (%)": "Average Return (%)"}
        )

        st.plotly_chart(chart, theme="streamlit", width='stretch')

    # pylint: disable=W0718
    except Exception as error:  # Catching broad exception for error handling
        st.write(f"Error performing the visualisation: {error}")

# --- Bar Chart - Preloaded Returns ---
def returns_visualisation(correlation_returns_df, asset_column, clean_asset_name):
    """
    Visualise the returns for the selected asset.
    """
    try:
        # Ensure the asset_column (e.g., 'SPY_return') exists in the dataframe
        if asset_column not in correlation_returns_df.columns:
            raise ValueError(f"Column '{asset_column}' not found in correlation_returns_df. \
            Ensure that the asset column exists.")

        # Get the list of return columns (including the base asset and other returns)
        return_columns = [col for col in correlation_returns_df.columns if '_return' in col]

        # Convert 0 returns to None (NaN) for proper averaging
        correlation_returns_df[asset_column] = correlation_returns_df[asset_column].where(
        correlation_returns_df[asset_column] != 0, None)

        # Aggregate the data (average returns for each asset, excluding None values)
        agg_returns = correlation_returns_df[return_columns].mean().reset_index()
        agg_returns.columns = ['Asset', 'Average Return (%)']

        # Format returns for display (rounded to 2 decimal places for clarity)
        def format_return(value):
            return f'{value * 100:.2f}%'

        agg_returns['Average Return (%)'] = agg_returns['Average Return (%)'].apply(format_return)

        # Create a bar chart for average returns
        chart = px.bar(
            agg_returns, x="Asset", y="Average Return (%)",
            title=f'Average Returns Analysis ({clean_asset_name})',  # Use clean_asset_name here
            labels={"Asset": "Asset", "Average Return (%)": "Average Return (%)"}
        )

        # Show the plot
        st.plotly_chart(chart, theme="streamlit", width='stretch')

    # pylint: disable=W0718
    except Exception:  # Catch duplicate column creation errors
        st.error(f"We cannot generate the returns table. This may be due to the base \
        asset {clean_asset_name} having membership with the chosen asset grouping. \
        Please try another base asset or select a different asset grouping and members \
        (e.g., ETF's Sectors and Technology).")

# ---  Line Chart - Cumulative Returns ---
def cumulative_returns(processed_df, timeline, filtered_df=None):
    """
    Calculate and display cumulative returns for the base asset.
    """
    st.write('Cumulative Returns')
    st.write('You have selected: Cumulative Returns Chart')

    # Check if the timeline is 'Interday'
    if timeline != 'Interday':
        st.info("Cumulative Returns can only be applied to the 'Interday' timeline.")
        return  # Exit if unsupported temporal pattern

    # Use the filtered dataframe if provided
    return_df = filtered_df if filtered_df is not None else processed_df

    # Ensure the 'return' column exists
    if 'return' not in return_df.columns:
        return_df['return'] = return_df['close'].pct_change() * 100  # Calculate percentage change

    # Compute the cumulative returns
    return_df['cumulative_return'] = (1 + return_df['return'] / 100).cumprod() - 1

    # Create a line chart for cumulative returns
    chart = px.line(
        return_df, x="date", y="cumulative_return",
        title=f'Cumulative Returns Chart ({timeline})',
        labels={"cumulative_return": "Cumulative Return (%)", "date": "Date"}
    )

    # Customise layout for better visualisation
    chart.update_layout(
        xaxis_title="Date",
        yaxis_title="Cumulative Return (%)",
        template="plotly_dark"
    )

    st.plotly_chart(chart, theme="streamlit", width='stretch')

# ---  Line - Rolling Returns ---
def rolling_returns(processed_df, timeline, filtered_df=None):
    """
    Generate a rolling return chart based on filtered data (Range, and Event-Based Analysis).
    """
    st.write('Rolling Returns')
    st.write('You have selected: Line Chart')

    # Check if the timeline is 'Interday'
    if timeline != 'Interday':
        st.info("Rolling Returns can only be applied to the 'Interday' timeline.")
        return  # Exit if unsupported temporal pattern

    # Use the filtered dataframe if provided
    return_df = filtered_df if filtered_df is not None else processed_df

    # Add a slider for the user to define the rolling window (default 5 days)
    rolling_window = st.sidebar.slider('Select Rolling Window (Days)',
    min_value=1, max_value=30, value=5, step=1)

    # Compute the rolling returns for the 'close' price
    return_df['rolling_return'] = return_df['close'].pct_change().rolling(
    window=rolling_window).sum() * 100

    # Create line chart for rolling returns over time
    chart = px.line(
        return_df, x="date", y="rolling_return",
        title=f'Rolling Returns ({timeline}) - {rolling_window} Days',
        labels={"rolling_return": "Rolling Return (%)", "date": "Date"}
    )

    # Customise layout for better visualisation
    chart.update_layout(
        xaxis_title="Date",
        yaxis_title="Rolling Return (%)",
        template="plotly_dark"
    )

    st.plotly_chart(chart, theme="streamlit", width='stretch')

# --- Scatterplot - Risk Return ---
def risk_return_scatter_plot(processed_df, timeline, filtered_df):
    """
    Generate a Risk-Return scatter plot, where returns are plotted against risk (volatility).

    Parameters:
    processed_df (pd.DataFrame): The DataFrame containing the data to plot.
    timeline (str): The timeline selected (e.g., Interday).

    Returns:
    None: Displays the scatter plot in Streamlit.
    """
    st.write(f"Risk-Return Scatter Plot for {timeline}")

    # Ensure the timeline is 'Interday' before proceeding
    if timeline != 'Interday':
        st.info("Risk-Return Scatter Plot can only be applied to the 'Interday' timeline.")
        return  # Exit if unsupported temporal pattern

    # Use the filtered dataframe if provided
    scatter_df = filtered_df if filtered_df is not None else processed_df

    # Drop rows where 'return' or 'Volatility' are missing (NaN)
    scatter_df = filtered_df[['date', 'return', 'volatility']].dropna()

    # Create scatter plot
    fig = px.scatter(
        scatter_df,
        x="volatility",  # Risk (Volatility)
        y="return",  # Return (percentage change)
        title=f'Risk-Return Analysis ({timeline})',
        labels={"volatility": "Risk (Volatility) (%)", "return": "Return (%)"},
        hover_data=['date']
    )

    # Customise layout for better readability
    fig.update_layout(
        xaxis_title="Risk (Volatility) (%)",  # Label for volatility axis
        yaxis_title="Return (%)",  # Label for return axis
        template="plotly_dark",
        height=400
    )

    st.plotly_chart(fig, width='stretch')

# -------------------------------------------------------------------------------------------------
# Visualisations Function Mapping
# -------------------------------------------------------------------------------------------------
options_data_visualisations_map = {
    'Price Movement - Line': line,
    'Price Movement - Candlestick': candlestick,
    'Trend Visualisation - Area': area,
    'Range and Events Returns': range_returns,
    'DPT vs Volatility': scatterplot_dpt_vs_volatility,
    'Temporal Returns': temporal_returns,
    'User Uploads Returns': user_returns,
    'Cumulative Returns': cumulative_returns,
    'Rolling Returns': rolling_returns,
    'Risk-Return': risk_return_scatter_plot
    # map other options to their corresponding functions here...
}
