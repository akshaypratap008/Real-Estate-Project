import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_icon='Plotting Demo')

df = pd.read_csv('artifacts/data/preprocessed-data/gurgaon_properties_with_lat_long.csv')

df['price_per_sqft'] = round((df['price']/df['built_up_area'])*10000000, 2)

group_df = df.groupby('sector')[['price', 'built_up_area', 'price_per_sqft', 'lat', 'lon']].mean()

st.dataframe(df)

st.title("Analytics")

property_type = st.multiselect(label = 'Property Type', options = ['flat', 'house'], width = 250)

def plot_map(df):
    fig = px.scatter_map(data_frame = df, lat = 'lat', lon='lon', color='price_per_sqft', size = 'built_up_area', color_continuous_scale = px.colors.cyclical.IceFire, zoom = 10, map_style='open-street-map', text = df.index, hover_name=df.index.str.upper())

    return st.plotly_chart(fig, use_container_width=True)

if not property_type:
    plot_map(group_df)
else:
    group_df = df[df['property_type'].isin(property_type)].groupby('sector')[['price', 'built_up_area', 'price_per_sqft', 'lat', 'lon']].mean()
    plot_map(group_df)









