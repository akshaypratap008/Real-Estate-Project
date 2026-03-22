import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import plotly.express as px
import ast
import plotly.figure_factory as ff

st.set_page_config(page_icon='Plotting Demo')
st.set_page_config(page_title="Market Analytics", layout="wide")

lat_long_df = pd.read_csv('artifacts/data/preprocessed-data/gurgaon_properties_with_lat_long.csv')

lat_long_df['price_per_sqft'] = round((lat_long_df['price']/lat_long_df['built_up_area'])*10000000, 2)

group_df = lat_long_df.groupby('sector')[['price', 'built_up_area', 'price_per_sqft', 'lat', 'lon']].mean()

st.header("Sector - Price per sqft Geopmap")
st.caption('*Shows how average price‑per‑sqft varies across Gurgaon sectors, visualized geographically for quick spatial comparison.*')

# map view
property_type = st.pills(label = 'Select Property Type', options = ['Flat', 'House'], selection_mode='multi')

def plot_map(dataframe):
    fig = px.scatter_map(data_frame = dataframe, lat = 'lat', lon='lon', color='price_per_sqft', size = 'built_up_area', color_continuous_scale = px.colors.cyclical.IceFire, zoom = 10, map_style='open-street-map', text = dataframe.index, hover_name=dataframe.index.str.upper(), labels={'price_per_sqft': 'Price per sqft'})

    return st.plotly_chart(fig, use_container_width=True)

if not property_type:
    plot_map(group_df)
else:
    group_df = lat_long_df[lat_long_df['property_type'].isin([i.lower() for i in property_type])].groupby('sector')[['price', 'built_up_area', 'price_per_sqft', 'lat', 'lon']].mean()
    plot_map(group_df)
st.divider()

# wordcloud
st.header('Features Wordcloud')
st.caption('*Highlights the most frequently mentioned property features across listings, giving a quick sense of common amenities and selling points.*')
st.write()
original_df_uncleaned = pd.read_csv('artifacts/data/preprocessed-data/gurgaon_properties_cleaned_v1.csv')

sector = st.multiselect(label = 'Select sectors', options = [i.upper() for i in original_df_uncleaned['sector'].unique()])

wordcloud_df = original_df_uncleaned[['sector', 'features']]

def create_wordcloud(wordcloud_df):
    main = []
    for row in wordcloud_df['features'].dropna().apply(ast.literal_eval):       # ast.literal_eval convert the list into python list
        main.extend(row)       # items of the row list are added to the main list

    feature_text = ' '.join(main)

    # creating wordcloud 
    plt.rcParams['font.family'] = 'Arial'

    wordcloud = WordCloud(width = 800, height = 800, background_color='#0E1117', stopwords= set(['s']), min_font_size=5, colormap='Set3').generate(feature_text)

    fig, ax = plt.subplots(figsize=(4,4), facecolor='#0E1117')
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    plt.tight_layout(pad = 0)
    st.pyplot(fig, use_container_width=False)

if not sector:
    create_wordcloud(wordcloud_df)
else:
    wordcloud_df = wordcloud_df[wordcloud_df['sector'].isin(i.lower() for i in sector)]
    create_wordcloud(wordcloud_df)
st.divider()

# price vs built up area scatter plot
st.header('Area vs Price')
st.caption('*Displays how property prices scale with built‑up area, helping identify size‑to‑price trends and outliers.*')

original_df_cleaned= pd.read_csv('artifacts/data/preprocessed-data/gurgaon_properties_post_feature_selection.csv')

selected_property_type = st.segmented_control(label = 'Select property type', options = ['Flat', 'House'], width = 250, selection_mode = 'multi', key = 'property_type_scatterplot')

def create_scatter_plot(dataframe):
    fig1 = px.scatter(dataframe, x = 'built_up_area', y = 'price', color = 'bedRoom', labels={
            'built_up_area': 'Built-up Area (sq ft)',
            'price': 'Price in Crores(₹)',
            'bedRoom': 'No. of bedrooms'
        })
    return st.plotly_chart(fig1, use_container_width=False)

if len(selected_property_type) > 0:
    df = original_df_cleaned[original_df_cleaned['property_type'].isin([item.lower() for item in selected_property_type])]
    create_scatter_plot(dataframe = df)
else:
    create_scatter_plot(dataframe = original_df_cleaned)
st.divider() 

# pie chart for number of bedrooms
st.header('Bedroom Count: Overall & Sector‑Wise')
st.caption('*Compares the distribution of bedroom counts across all properties and within specific sectors to reveal housing mix patterns.*')

def create_pie(df):
    fig2 = px.pie(data_frame=df, names = 'bedRoom')  
    fig2.update_layout(width = 300, height = 420)
    return st.plotly_chart(fig2, use_container_width=False)

col1, col2 = st.columns(2)

with col1:
    selected_property_type = st.segmented_control(label = 'Select property type', options = ['Flat', 'House'], width = 250, selection_mode = 'multi', key = 'property_type_pie_chart')

    if len(selected_property_type) > 0:
        df = original_df_cleaned[original_df_cleaned['property_type'].isin([item.lower() for item in selected_property_type])]
        create_pie(df)
    else:
        create_pie(original_df_cleaned)

with col2:
    selected_sector = st.selectbox(label = 'Select sector', options = [item.upper() for item in original_df_cleaned['sector'].unique()], width = 250, placeholder='SECTOR 1')

    df = original_df_cleaned[original_df_cleaned['sector'] == selected_sector.lower()]
    create_pie(df)
st.divider()   

# box plot for different bedroom prices
st.header('Price distribution of Number of Bedrooms')
st.caption('*Shows how property prices vary across different bedroom categories, helping compare affordability across configurations.*')

selected_property_type = st.segmented_control(label = 'Select property type', options = ['Flat', 'House'], width = 250, selection_mode = 'multi', key = 'property_type_price_distribution')

df3 = original_df_cleaned[original_df_cleaned['bedRoom'] <= 4]

def plot_box_plot(dataframe):
    fig4 = px.box(data_frame=dataframe, x = 'bedRoom', y = 'price', labels = {'bedRoom': 'No. of Bedrooms', 'price': 'Price in Crores'})
    return st.plotly_chart(fig4, use_container_width=False)

if len(selected_property_type) > 0:
        dataframe = df3[df3['property_type'].isin([item.lower() for item in selected_property_type])]
        plot_box_plot(dataframe)
else:
    plot_box_plot(df3)
st.divider()

# dist plot of flats and houses distplot
st.header('Price distribution of Flats and Houses')
st.caption('*Compares the overall price distribution of flats versus houses to highlight differences in market positioning.*')
flat_hist_data = original_df_cleaned[original_df_cleaned['property_type'] == 'flat']['price'].tolist()
house_hist_data = original_df_cleaned[original_df_cleaned['property_type'] == 'house']['price'].tolist()
fig5 = ff.create_distplot(hist_data= [flat_hist_data, house_hist_data], group_labels=['Flats', 'House'], show_rug=False)
fig5.update_layout(xaxis_title = 'Price in Crores', yaxis_title = 'Probability Density')

st.plotly_chart(fig5, use_container_width=False)
st.divider()

# top sectors by price per sqft
st.header('Sector Price Ranking')
st.caption('*Shows the five most expensive and five most affordable sectors based on average price per square foot.*')
selected_order = st.pills(label = '', options = ['Top 5 sectors', 'Bottom 5 sectors'], width = 250, selection_mode='single', key = 'per_sqft_order', label_visibility='hidden')

original_df_cleaned['price_per_sqft'] = round((original_df_cleaned['price'] / original_df_cleaned['built_up_area'])*10000000, 2)

if selected_order == 'Bottom 5 sectors':
    data = original_df_cleaned.groupby('sector')['price_per_sqft'].mean().sort_values(ascending= True).head(5)
    fig6 = px.bar(data, x=data.index, y=data.values)
    fig6.update_layout(xaxis_title = 'Sector', yaxis_title= 'Avg price per sqft')
    st.plotly_chart(fig6, use_container_width=False)

else:
    data = original_df_cleaned.groupby('sector')['price_per_sqft'].mean().sort_values(ascending= False).head(5)
    fig6 = px.bar(data, x=data.index, y=data.values)
    fig6.update_layout(xaxis_title = 'Sector', yaxis_title= 'Avg price per sqft')
    st.plotly_chart(fig6, use_container_width=False)
    





