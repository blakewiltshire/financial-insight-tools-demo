# -------------------------------------------------------------------------------------------------
#  ---- pylint global exceptions ----
# Add any global disables if required (e.g., unused-import)
# -------------------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------------
# Docstring
# -------------------------------------------------------------------------------------------------
"""
This module contains functions for performing various descriptive statistical analyses
on a DataFrame containing financial data. These functions calculate and visualize key statistics
such as measures of central tendency, dispersion, shape, and basic statistics. Additionally,
it includes functionality for creating histograms, boxplots, and frequency distributions,
with the option to exclude outliers based on the Interquartile Range (IQR).

Functions in this module include:
- `centre_of_the_data_set`: Calculates and displays the mean and median values for a
specified column.
- `measures_of_dispersion`: Calculates and displays measures such as variance, range,
standard deviation, and standard deviation bands for a specified column.
- `measures_of_shape`: Calculates and displays the kurtosis and skewness of a specified column.
- `basic_statistics`: Displays basic statistics such as minimum, maximum, sum, and count for a
specified column.
- `create_histogram`: Generates and displays a histogram for a specified column, with an option
to exclude outliers.
- `calculate_frequencies`: Computes a frequency distribution for a specified column, with
optional outlier removal.
- `calculate_summary`: Summarizes returns by calculating frequencies of positive, negative,
and zero returns, along with average return percentages.
- `create_boxplot`: Creates a boxplot to visualize the distribution of data for a specified column.
- `frequency_distribution`: Displays the frequency distribution for a specified column,
including histograms, boxplots, frequency tables, and summaries.

The functions support hiding outliers, based on IQR filtering, for more accurate data analysis.

Example usage:
    from descriptive_statistics import centre_of_the_data_set, measures_of_dispersion

    centre_of_the_data_set(df, 'column_name')
    measures_of_dispersion(df, 'column_name')
"""

# -------------------------------------------------------------------------------------------------
# Third-party Libraries
# -------------------------------------------------------------------------------------------------
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

# -------------------------------------------------------------------------------------------------
# Function: centre_of_the_data_set
# Purpose: Calculate and display the central tendency (mean, median) of returns for a
# selected column.
# Use Case: Statistical Analysis / Descriptive Statistics (Market & Volatility module)
# -------------------------------------------------------------------------------------------------
def centre_of_the_data_set(processed_df, column):
    """
    Calculate and display measures of central tendency for a specified column.

    This function calculates the mean and median values for the specified column in the provided
    dataframe (`processed_df`) and displays them as percentages.

    Parameters:
    processed_df (pandas.DataFrame): The dataframe containing the data to analyze.
    column (str): The column name for which the central tendency measures are calculated.

    Returns:
    None: Displays the mean and median as percentages.
    """
    st.write('**Measure of Central Tendency**')

    # Calculate Mean and format as percentage
    mean_value = processed_df[column].mean() * 100
    st.write('Mean')
    st.info(f'{mean_value:.2f}%')  # Display mean with two decimal places as percentage

    # Calculate Median and format as percentage
    median_value = processed_df[column].median() * 100
    st.write('Median')
    st.info(f'{median_value:.2f}%')

    # Optional: calculate Mode if needed
    mode_value = processed_df[column].mode().iloc[0] * 100
    st.write('Mode')
    st.info(f'{mode_value:.2f}%')

    # ✅ Return the results for JSON snapshot
    return {
        "mean_pct": round(mean_value, 2),
        "median_pct": round(median_value, 2),
        "mode_pct": round(mode_value, 2)
    }

# -------------------------------------------------------------------------------------------------
# Function: measures_of_dispersion
# Purpose: Display return dispersion using variance, range, and standard deviation with
# band breakdowns.
# Use Case: Statistical Analysis / Descriptive Statistics (Market & Volatility module)
# -------------------------------------------------------------------------------------------------
def measures_of_dispersion(processed_df, column):
    """
    Calculate and display various measures of dispersion for the specified column.

    This function calculates and displays the following measures of dispersion for the specified
    column in the dataframe (`processed_df`):
    - Standard variance
    - Range (maximum - minimum)
    - Standard deviation
    - Standard deviation bands and actual counts within those bands

    Each measure is displayed as a percentage, with the bands and counts shown in a formatted table.

    Parameters:
    processed_df (pandas.DataFrame): The dataframe containing the data to analyze.
    column (str): The column name for which the measures of dispersion are calculated.

    Returns:
    None: Displays the calculated measures and the standard deviation bands as a table.
    """
    st.write('**Measures of Dispersion**')

    # Calculate Standard Variance and format as percentage
    var = processed_df[column].var() * 100  # Multiply by 100 to convert to percentage
    st.write('Standard Variance')
    st.info(f'{var:.2f}%')  # Display var with two decimal places as percentage

    # Calculate Range (Max - Min) and format as percentage
    range_value = (processed_df[column].max() - processed_df[column].min()) * 100
    st.info(f'{range_value:.2f}%')  # Display range with two decimal places as percentage

    # Calculate Standard Deviation and format as percentage
    std = processed_df[column].std() * 100  # Multiply by 100 to convert to percentage
    st.write('Standard Deviation')
    st.info(f'{std:.2f}%')  # Display std with two decimal places as percentage

    # Create a copy of the processed_df dataframe
    bands_returns = processed_df.copy()
    bands_returns = bands_returns[column]

    # Calculate standard deviation bands and actual counts
    bands = [1, 2, 3]
    upper_bands = [(bands_returns.mean() + (i * bands_returns.std())) for i in bands]
    lower_bands = [(bands_returns.mean() - (i * bands_returns.std())) for i in bands]
    ubacs = [(bands_returns.mean() + ub) for ub in upper_bands]
    lbacs = [(bands_returns.mean() + lb) for lb in lower_bands]
    counts = [sum((bands_returns <= ub) & (bands_returns >= lb)) for ub, lb in zip(ubacs, lbacs)]

    # Define the dictionary for the DataFrame
    data_1 = {
        'Band': bands,
        'Upper Band': upper_bands,
        'Lower Band': lower_bands,
        'Actual Count': counts,
        'Actual Count %': [c / bands_returns.count() for c in counts],
        'Normal Count': [p * bands_returns.count() for p in [0.682, 0.9540, 0.9980]],
        'Normal %': ["68.20%", "95.40%", "99.80%"]
    }

    # Create a pandas DataFrame from the dictionary
    std_dev = pd.DataFrame(data_1)

    # Set the index to be the Band column
    std_dev.set_index('Band', inplace=True)

    # Format the data using f-strings
    std_dev['Upper Band'] = [f"{x:.2%}" for x in std_dev['Upper Band']]
    std_dev['Lower Band'] = [f"{x:.2%}" for x in std_dev['Lower Band']]
    std_dev['Actual Count'] = [f"{x:.0f}" for x in std_dev['Actual Count']]
    std_dev['Actual Count %'] = [f"{x:.2%}" for x in std_dev['Actual Count %']]
    std_dev['Normal Count'] = [f"{x:.0f}" for x in std_dev['Normal Count']]

    # Print the DataFrame
    st.write('Standard Deviation Bands\n')
    st.write(std_dev)

    # ✅ Return JSON snapshot block
    return {
        "Standard Variance %": round(var, 2),
        "Range %": round(range_value, 2),
        "Standard Deviation %": round(std, 2),
        "Standard Deviation Bands": std_dev.to_dict(orient="index")
    }

# -------------------------------------------------------------------------------------------------
# Function: measures_of_shape
# Purpose: Assess skewness and kurtosis to understand asymmetry and tail risk of returns.
# Use Case: Statistical Analysis / Descriptive Statistics (Market & Volatility module)
# -------------------------------------------------------------------------------------------------
def measures_of_shape(processed_df, column):
    """
    Calculate and display the kurtosis and skewness of the specified column.

    This function calculates and displays two measures of the shape of the distribution for the
    specified column in the dataframe (`processed_df`):
    - Kurtosis, which measures the tailedness of the distribution.
    - Skewness, which measures the asymmetry of the distribution.

    Parameters:
    processed_df (pandas.DataFrame): The dataframe containing the data to analyze.
    column (str): The column name for which the measures of shape are calculated.

    Returns:
    None: Displays the calculated kurtosis and skewness values.
    """
    st.write('**Measures of Shape**')

    # Define kurt_value and skew_value for snapshot return
    kurt_value = processed_df[column].kurt()
    st.write('Kurt')
    st.info(f"{kurt_value:.4f}")

    skew_value = processed_df[column].skew()
    st.write('Skew')
    st.info(f"{skew_value:.4f}")

    # ✅ Return JSON snapshot block
    return {
        "Kurtosis": round(kurt_value, 4),
        "Skewness": round(skew_value, 4)
    }

# -------------------------------------------------------------------------------------------------
# Function: basic_statistics
# Purpose: Display min, max, sum, and count as foundational descriptive metrics for a
# return column.
# Use Case: Statistical Analysis / Descriptive Statistics (Market & Volatility module)
# -------------------------------------------------------------------------------------------------
def basic_statistics(processed_df, column):
    """
    Calculate and display basic statistics for the specified column.

    This function calculates and displays the following basic statistics for the specified column
    in the dataframe (`processed_df`):
    - Minimum value
    - Maximum value
    - Sum of values
    - Count of non-null values

    The values are displayed as percentages (where applicable) or with four decimal places.

    Parameters:
    processed_df (pandas.DataFrame): The dataframe containing the data to analyze.
    column (str): The column name for which the basic statistics are calculated.

    Returns:
    None: Displays the calculated statistics.
    """
    st.write('**Basic Statistics**')

    # ✅ Define the values before usage
    min_value = processed_df[column].min() * 100
    st.write('Minimum')
    st.info(f'{min_value:.2f}%')

    max_value = processed_df[column].max() * 100
    st.write('Maximum')
    st.info(f'{max_value:.2f}%')

    sum_value = processed_df[column].sum()
    st.write('Sum')
    st.info(f'{sum_value:.4f}')

    count_value = processed_df[column].count()
    st.write('Count')
    st.info(count_value)

    # ✅ Return JSON snapshot block
    return {
        "Minimum (%)": round(min_value, 2),
        "Maximum (%)": round(max_value, 2),
        "Sum": round(sum_value, 4),
        "Count": int(count_value)
    }

# -------------------------------------------------------------------------------------------------
# Function: Create_histogram
# Purpose: Visualise distribution of returns using histograms with optional outlier filtering.
# Use Case: Statistical Analysis / Descriptive Statistics (Market & Volatility module)
# -------------------------------------------------------------------------------------------------
def create_histogram(processed_df, column, bin_size, hide_outliers):
    """
    Create and display a histogram of the specified column with optional outlier removal.

    This function generates a histogram of the specified column in the dataframe (`processed_df`),
    with a customizable bin size (`bin_size`). It also includes an option to hide outliers based
    on the interquartile range (IQR).

    Parameters:
    processed_df (pandas.DataFrame): The dataframe containing the data to visualize.
    column (str): The column name for which the histogram is created.
    bin_size (int): The bin size for the histogram.
    hide_outliers (bool): If True, outliers are removed based on the IQR.

    Returns:
    alt.Chart: An Altair chart object representing the histogram.
    """
    data = processed_df[[column]]

    # pylint: disable=C0103
    if hide_outliers:
        q1 = data[column].quantile(0.25)
        q3 = data[column].quantile(0.75)
        iqr = q3 - q1
        filter_condition = (data[column] >= q1 - 1.5 * iqr) & (data[column] <= q3 + 1.5 * iqr)
        data = data.loc[filter_condition]


    # Create histogram with labeled bins
    histogram = alt.Chart(data).mark_bar().encode(
        alt.X(
            column,
            bin=alt.Bin(
                step=bin_size,
                extent=[processed_df[column].min(), processed_df[column].max()]
            ),
            title='Percent Change',
            axis=alt.Axis(format='.0%')
        ),
        y='count()'
    )


    # Add vertical line at 0
    zero_line = alt.Chart(pd.DataFrame({'x': [0]})).mark_rule(color='red', strokeWidth=2).encode(
        x='x:Q'
    )

    # Combine histogram and zero line
    chart = (histogram + zero_line).properties(
        width=600,
        height=400,
        title='Percent Change Distribution for - ' + column
    ).configure_axis(
        labelFontSize=14,
        titleFontSize=16
    ).configure_title(
        fontSize=16
    )

    return chart

# -------------------------------------------------------------------------------------------------
# Function: calculate_frequencies
# Purpose: Calculate binned return frequencies and cumulative percentages for distribution tables.
# Use Case: Statistical Analysis / Descriptive Statistics (Market & Volatility module)
# -------------------------------------------------------------------------------------------------
def calculate_frequencies(processed_df, column, bin_size, hide_outliers):
    """
    Calculate frequency distribution of a column in the DataFrame, optionally hiding outliers.

    Parameters:
    - processed_df: DataFrame containing the data to analyze.
    - column: The column in the DataFrame to calculate frequencies for.
    - bin_size: The size of the bins for the histogram.
    - hide_outliers: Boolean flag to decide if outliers should be excluded from analysis.

    Returns:
    - freq_table: DataFrame with frequency distribution, percentages, and cumulative percentages.
    """
    # pylint: disable=C0103
    if hide_outliers:
    # Calculate IQR (Interquartile Range) for outlier filtering
        q1 = processed_df[column].quantile(0.25)
        q3 = processed_df[column].quantile(0.75)
        iqr = q3 - q1

        # Filter out data outside 1.5 * IQR from Q1 and Q3
        filter_condition = (
            (processed_df[column] >= q1 - 1.5 * iqr) &
            (processed_df[column] <= q3 + 1.5 * iqr)
        )
        processed_df = processed_df.loc[filter_condition]

    # Create frequency table using pandas cut to group values into intervals
    freq_table = pd.cut(
        processed_df[column],
        bins=np.arange(-0.2, 0.2001, bin_size)
    ).value_counts(sort=False)

    # Format interval labels as percentages and calculate frequencies and percentages
    freq_table.index = [
    f'{interval.left:.2%} to {interval.right:.2%}' for interval in freq_table.index
    ]
    freq_table.index.name = 'Interval'

    # Combine frequency and percentage columns, add cumulative percentage
    freq_table = pd.concat([freq_table, freq_table / freq_table.sum()], axis=1)
    freq_table.columns = ['Frequency', 'Percent']
    freq_table['Cumulative Percent'] = freq_table['Percent'].cumsum()

    # Format percentages as strings with two decimal places
    freq_table['Percent'] = freq_table['Percent'].apply(lambda x: f'{x:.2%}')
    freq_table['Cumulative Percent'] = freq_table['Cumulative Percent'].apply(lambda x: f'{x:.2%}')

    return freq_table

# -------------------------------------------------------------------------------------------------
# Function: calculate_summary
# Purpose: Summarise return types and compute average contribution of each (positive,
# negative, flat).
# Use Case: Statistical Analysis / Descriptive Statistics (Market & Volatility module)
# -------------------------------------------------------------------------------------------------
# pylint: disable=R0914
def calculate_summary(processed_df, column, hide_outliers):
    """
    Calculate a summary of returns, including positive, negative, and zero returns,
    along with their frequencies, average return percentages, and average daily
    return percentages. This function also allows for the exclusion of outliers
    using the Interquartile Range (IQR) method.

    Parameters:
    - processed_df (pd.DataFrame): The input data frame containing asset return data.
    - column (str): The column name representing the return values to be summarized.
    - hide_outliers (bool): Whether to exclude outliers based on the IQR method.

    Returns:
    - pd.DataFrame: A summary of return types (positive, negative, zero), including
                    their frequencies, average return percentages, and average
                    daily return percentages.
    """
    # pylint: disable=C0103
    if hide_outliers:
    # Calculate IQR (Interquartile Range) for outlier filtering
        q1 = processed_df[column].quantile(0.25)
        q3 = processed_df[column].quantile(0.75)
        iqr = q3 - q1

        # Filter out data outside 1.5 * IQR from Q1 and Q3
        filter_condition = (
            (processed_df[column] >= q1 - 1.5 * iqr) &
            (processed_df[column] <= q3 + 1.5 * iqr)
        )

        processed_df = processed_df.loc[filter_condition]

    # Extract relevant data for analysis
    data = processed_df[[column]]

    # Count frequencies of positive, negative, and zero returns
    freqpos = (data > 0).values.sum()
    freqneg = (data < 0).values.sum()
    freq0 = (data == 0).values.sum()

    # Calculate the average return for positive, negative, and zero returns
    positive_returns = data[data[column] > 0][column]
    average_positive_return = positive_returns.mean()

    negative_returns = data[data[column] < 0][column]
    average_negative_return = negative_returns.mean()

    flat_returns = data[data[column] == 0][column]
    average_flat_return = flat_returns.mean()

    # Create a summary DataFrame with the calculated values
    freq_summary = pd.DataFrame({
        'Type of Return': ['Positive', 'Negative', 'Zero'],
        'Average Return %': [
            average_positive_return, average_negative_return, average_flat_return
        ],
        'Frequency': [freqpos, freqneg, freq0],
        'Frequency %': [
            freqpos / data[column].count(),
            freqneg / data[column].count(),
            freq0 / data[column].count()
        ],
        'Average Daily %': [
            freqpos / data[column].count() * average_positive_return,
            freqneg / data[column].count() * average_negative_return,
            freq0 / data[column].count() * average_flat_return
        ],
    })

    # Apply formatting for percentages and frequencies using f-strings
    freq_summary['Average Return %'] = [f"{x:.2%}" for x in freq_summary['Average Return %']]
    freq_summary['Frequency'] = [f"{x:.0f}" for x in freq_summary['Frequency']]
    freq_summary['Frequency %'] = [f"{x:.2%}" for x in freq_summary['Frequency %']]
    freq_summary['Average Daily %'] = [f"{x:.2%}" for x in freq_summary['Average Daily %']]


    # Set 'Type of Return' as index for the summary table
    freq_summary = freq_summary.set_index('Type of Return')

    return freq_summary

# -------------------------------------------------------------------------------------------------
# Function: create_boxplot
# Purpose: Create a boxplot to visualise distribution and potential outliers of return data.
# Use Case: Statistical Analysis / Descriptive Statistics (Market & Volatility module)
# -------------------------------------------------------------------------------------------------
def create_boxplot(processed_df, column, hide_outliers):
    """
    Creates a boxplot to visualize the distribution of data for a given column, optionally
    excluding outliers.

    Parameters:
    processed_df (pd.DataFrame): The DataFrame containing the data to be visualized.
    column (str): The column name on which the boxplot will be based.
    hide_outliers (bool): Whether to exclude outliers from the boxplot based on IQR filtering.

    Returns:
    alt.Chart: An Altair chart object representing the boxplot.
    """
    # pylint: disable=C0103
    # Calculate the 1st and 3rd quartiles, and the Interquartile Range (IQR)
    q1 = processed_df[column].quantile(0.25)
    q3 = processed_df[column].quantile(0.75)
    iqr = q3 - q1

    # Define the lower and upper bounds for filtering based on IQR
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    # Define the filtering condition based on IQR to remove outliers
    filter_condition = (processed_df[column] >= lower_bound) & (processed_df[column] <= upper_bound)

    # Apply filtering if 'hide_outliers' is True
    if hide_outliers:
        processed_df = processed_df.loc[filter_condition].copy()  # Use .copy() to avoid warning

    # Add a constant column to the dataframe to serve as the x-axis for the boxplot
    processed_df["box"] = "Boxplot"

    # Create the boxplot using Altair, encoding the column values for the y-axis
    boxplot = alt.Chart(processed_df).mark_boxplot().encode(
        x='box:N',  # Nominal encoding for the x-axis, as we are displaying a single category
        y=f'{column}:Q'  # Quantitative encoding for the y-axis (the column being visualized)
    )

    return boxplot

# -------------------------------------------------------------------------------------------------
# Function: frequency_distribution
# Purpose: Integrate visual and tabular summaries of return distributions into a single workflow.
# Use Case: Statistical Analysis / Descriptive Statistics (Market & Volatility module)
# -------------------------------------------------------------------------------------------------
def frequency_distribution(processed_df, column):
    """
    Display the frequency distribution for a specified column in the given DataFrame, with
    options to filter the data by date range, hide outliers, and
    adjust the bin size for histograms.

    Parameters:
    processed_df (pd.DataFrame): The DataFrame containing the data to be analysed.
    column (str): The column name for which the frequency distribution will be calculated.

    This function:
    - Filters data by a date range selected by the user.
    - Displays a histogram, boxplot, frequency table, and summary of the frequency distribution.
    """

    st.header('Frequency Distribution')

    # Sidebar for selecting the bin size and whether to hide outliers
    bin_size_pct = st.sidebar.slider('Select frequency distribution interval size (%)', 0.25
    , 10.0, 1.00, 0.25)
    hide_outliers = st.sidebar.checkbox('Hide frequency distribution outliers')

    # Convert bin size from percentage to decimal
    bin_size = bin_size_pct / 100

    # Ensure bin size is not zero, set default if necessary
    if bin_size == 0:
        st.warning('Bin size cannot be zero. Setting default bin size to 1.00.')
        bin_size = 1.00

    # Create and display the histogram
    chart = create_histogram(processed_df, column, bin_size, hide_outliers)
    st.altair_chart(chart)

    # Create and display the boxplot
    boxplot = create_boxplot(processed_df, column, hide_outliers)
    st.altair_chart(boxplot)

    # Generate and display the frequency table
    freq_table = calculate_frequencies(processed_df, column, bin_size, hide_outliers)
    st.markdown("**Frequency Table**")
    st.write(freq_table)

    # Generate and display the frequency summary
    freq_summary = calculate_summary(processed_df, column, hide_outliers)
    st.write('**Frequency Table Summary**')
    st.write(freq_summary)

# -------------------------------------------------------------------------------------------------
# Descriptive Statistics Function Mapping
# -------------------------------------------------------------------------------------------------
options_descriptive_statistics_map = {
    'Measure of Central Tendency': centre_of_the_data_set,
    'Measures of Dispersion': measures_of_dispersion,
    'Measures of Shape': measures_of_shape,
    'Basic Statistics': basic_statistics,
    'Frequency Distribution': frequency_distribution
    # map other options to their corresponding functions here...
}
