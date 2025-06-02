import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

def _generate_plots_(df: pd.DataFrame) -> None:
    #speed plot
    fig = px.line(df,x='Elapsed_Time',y='Speed', title = 'Speed Over Time (Based on Video Frames)')
    st.plotly_chart(fig)

    #histogram of speed
    fig = px.histogram(df, x="Speed", nbins=15, title="Speed Distribution")
    st.plotly_chart(fig)

    #acceleration plot
    time_diffs = np.diff(df["Elapsed_Time"])
    min_dt = np.min(time_diffs)
    max_dt = np.max(time_diffs)
    if 0.3 <= min_dt <= 2.0 and max_dt <= 3.0:
        time = df["Elapsed_Time"].to_numpy()
        speed = df["Speed"].to_numpy()
        delta_v = np.diff(speed)
        delta_t = np.diff(time)
        delta_t[delta_t == 0] = np.nan
        accel = delta_v / delta_t
        accel_time = time[:-1] + delta_t / 2
        accel_df = pd.DataFrame({
            "Elapsed_Time": accel_time,
            "Acceleration": accel
        })
        fig = px.line(accel_df, x="Elapsed_Time", y="Acceleration", title="Acceleration Over Time")
        st.plotly_chart(fig)
    else:
        st.info("Acceleration plot skipped: Time intervals are too small or too large for reliable calculation.")
