import pandas as pd
import streamlit as st
from streamlit import column_config

df = pd.read_pickle("preloaded_asset_summary.pkl")
st.write(df.columns.tolist())
st.write(df)
