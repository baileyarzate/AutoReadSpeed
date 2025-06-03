import streamlit as st
import pandas as pd
import numpy as np
def _write_statistics_(df: pd.DataFrame) -> None:
    st.write(f"Minimum Speed: {min(df['Speed']):.0f} {df['Unit'].iloc[0]}")
    st.write(f"Maximum Speed: {max(df['Speed']):.0f} {df['Unit'].iloc[0]}")
    st.write(f"Mean Speed: {np.mean(df['Speed']):.2f} {df['Unit'].iloc[0]}")
    st.write(f"Median Speed: {np.median(df['Speed']):.1f} {df['Unit'].iloc[0]}")
    st.write(f"Variance Speed: {np.var(df['Speed']):.2f} {df['Unit'].iloc[0]}")
    st.write(f"Total Duration: {df["Elapsed_Time"].iloc[-1] - df["Elapsed_Time"].iloc[0]:.2f} seconds")
    speed = df["Speed"].to_numpy()
    time = df["Elapsed_Time"].to_numpy()
    delta_t = np.diff(time)
    delta_v = speed[:-1] / 3600 #convert to miles
    # Distance = speed * time
    distance = np.sum(delta_v * delta_t)
    if df['Unit'].iloc[0] == 'MPH':
        st.write(f"Estimated Distance Traveled: {distance:.2f} miles")
    else:
        st.write(f"Estimated Distance Traveled: {distance:.2f} miles")