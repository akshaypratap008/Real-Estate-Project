import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import plotly.express as px
import ast

st.set_page_config(page_icon='Plotting Demo')
st.set_page_config(layout = 'centered')

df = pd.read_csv('artifacts/data/preprocessed-data/gurgaon_properties_with_lat_long.csv')

df['price_per_sqft'] = round((df['price']/df['built_up_area'])*10000000, 2)

group_df = df.groupby('sector')[['price', 'built_up_area', 'price_per_sqft', 'lat', 'lon']].mean()

st.dataframe(df)

st.header("Sector - Price per sqft Geopmap")

# map view
property_type = st.multiselect(label = 'Property Type', options = ['flat', 'house'], width = 250)

def plot_map(df):
    fig = px.scatter_map(data_frame = df, lat = 'lat', lon='lon', color='price_per_sqft', size = 'built_up_area', color_continuous_scale = px.colors.cyclical.IceFire, zoom = 10, map_style='open-street-map', text = df.index, hover_name=df.index.str.upper(), labels={'price_per_sqft': 'Price per sqft'})

    return st.plotly_chart(fig, use_container_width=True)

if not property_type:
    plot_map(group_df)
else:
    group_df = df[df['property_type'].isin(property_type)].groupby('sector')[['price', 'built_up_area', 'price_per_sqft', 'lat', 'lon']].mean()
    plot_map(group_df)

# wordcloud
st.header('Wordcloud')
df1 = pd.read_csv(r'C:\Users\apaks\Desktop\Real Estate Project\artifacts\data\preprocessed-data\gurgaon_properties_cleaned_v1.csv')

sector = st.multiselect(label = 'Select sector', options = df1['sector'].unique(), width = 500)

wordcloud_df = df1[['sector', 'features']]

def create_wordcloud(wordcloud_df):
    main = []
    for row in wordcloud_df['features'].dropna().apply(ast.literal_eval):       # ast.literal_eval convert the list into python list
        main.extend(row)       # items of the row list are added to the main list

    feature_text = ' '.join(main)

    # creating wordcloud 
    plt.rcParams['font.family'] = 'Arial'

    wordcloud = WordCloud(width = 800, height = 800, background_color='white', stopwords= set(['s']), min_font_size=5).generate(feature_text)

    fig, ax = plt.subplots(figsize=(6,6), facecolor=None)
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    plt.tight_layout(pad = 0)
    st.pyplot(fig, use_container_width=True)

if not sector:
    create_wordcloud(wordcloud_df)
else:
    wordcloud_df = wordcloud_df[wordcloud_df['sector'].isin(sector)]
    create_wordcloud(wordcloud_df)

# price vs built up area scatter plot
st.header('Area vs Price')

property_type = st.multiselect(label = 'Select property type', options = ['flat', 'house'], width = 250)

def create_scatter_plot(df):
    fig1 = px.scatter(df, x = 'built_up_area', y = 'price', color = 'bedRoom', labels={
            'built_up_area': 'Built-up Area (sq ft)',
            'price': 'Price (₹)',
            'bedRoom': 'Number of bedrooms'
        })
    return st.plotly_chart(fig1, use_container_width=False)

if len(property_type) > 0:
    df = df[df['property_type'].isin(property_type)]
    create_scatter_plot(df)
else:
    create_scatter_plot(df)



