# -------------------------------------------------------------------------------------------------
# 📊 Correlation Charting Utilities (Platinum Build)
# -------------------------------------------------------------------------------------------------
# pylint: disable=invalid-name

"""
Enhanced correlation visualisation components.

Includes:
- Heatmap (Altair)
- Pairwise Scatter Plot (Plotly)
- Rolling Correlation Trendlines (Altair)
- Correlation Boxplot (optional)
"""

import pandas as pd
import numpy as np
import altair as alt
import plotly.graph_objects as go
import plotly.express as px

# -------------------------------------------------------------------------------------------------
# Heatmap Chart (Altair)
# -------------------------------------------------------------------------------------------------
def generate_correlation_heatmap(corr_matrix):
    """
    Generates aesthetically aligned Altair heatmap.
    """
    corr_df = corr_matrix.reset_index().melt(id_vars='index')
    corr_df.columns = ['Asset X', 'Asset Y', 'Correlation']

    heatmap = alt.Chart(corr_df).mark_rect().encode(
        x=alt.X('Asset X:O', sort=None),
        y=alt.Y('Asset Y:O', sort=None),
        color=alt.Color('Correlation:Q',
                        scale=alt.Scale(scheme='redblue', domain=[-1, 1])),
        tooltip=['Asset X', 'Asset Y', alt.Tooltip('Correlation:Q', format='.2f')]
    ).properties(
        width=600,
        height=400,
        title='📊 Correlation Heatmap'
    )

    return heatmap

# -------------------------------------------------------------------------------------------------
# Pairwise Scatter Plot (Plotly)
# -------------------------------------------------------------------------------------------------
def plot_pairwise_scatter(df, asset_x, asset_y):
    """
    Enhanced pairwise scatter plot with regression line and correlation coefficient.
    """
    corr_coeff = df[asset_x].corr(df[asset_y])

    # Create regression line
    slope, intercept = np.polyfit(df[asset_x], df[asset_y], 1)
    regression_line = slope * df[asset_x] + intercept

    fig = go.Figure()

    # Scatter points
    fig.add_trace(go.Scatter(
        x=df[asset_x],
        y=df[asset_y],
        mode='markers',
        marker=dict(color='royalblue', size=5, opacity=0.7),
        name='Data Points'
    ))

    # Regression line
    fig.add_trace(go.Scatter(
        x=df[asset_x],
        y=regression_line,
        mode='lines',
        line=dict(color='orange', width=2),
        name='Regression Line'
    ))

    fig.update_layout(
        title=f'🔎 Pairwise Scatter: {asset_x} vs {asset_y} (r = {corr_coeff:.2f})',
        xaxis_title=asset_x,
        yaxis_title=asset_y,
        template='plotly_white',
        width=600,
        height=500
    )
    return fig

# -------------------------------------------------------------------------------------------------
# Rolling Correlation Trendline (Altair)
# -------------------------------------------------------------------------------------------------
def plot_rolling_correlation(df_x, df_y, window=30):
    """
    Enhanced rolling correlation trendline.
    """
    rolling_corr = df_x.rolling(window).corr(df_y)
    corr_df = pd.DataFrame({
        'Date': df_x.index,
        'Rolling Correlation': rolling_corr
    }).dropna()

    chart = alt.Chart(corr_df).mark_line(interpolate='monotone').encode(
        x=alt.X('Date:T'),
        y=alt.Y('Rolling Correlation:Q', scale=alt.Scale(domain=[-1, 1])),
        tooltip=['Date:T', alt.Tooltip('Rolling Correlation:Q', format='.2f')]
    ).properties(
        width=700,
        height=300,
        title=f'📈 Rolling Correlation ({window}-Day Window)'
    )

    return chart

# -------------------------------------------------------------------------------------------------
# Optional Boxplot (Altair)
# -------------------------------------------------------------------------------------------------
def plot_correlation_boxplot(corr_matrix):
    """
    Boxplot showing distribution of correlation coefficients.
    """
    corr_flat = corr_matrix.where(~np.eye(corr_matrix.shape[0],dtype=bool)).stack().reset_index()
    corr_flat.columns = ['Asset X', 'Asset Y', 'Correlation']

    chart = alt.Chart(corr_flat).mark_boxplot(extent='min-max').encode(
        y=alt.Y('Correlation:Q', scale=alt.Scale(domain=[-1, 1])),
        tooltip=[alt.Tooltip('Correlation:Q', format='.2f')]
    ).properties(
        width=300,
        height=300,
        title='📊 Correlation Distribution'
    )

    return chart
