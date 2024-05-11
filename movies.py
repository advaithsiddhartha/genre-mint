import streamlit as st
import numpy as np
import pandas as pd
import altair as alt


st.set_page_config(page_title='GenreMint', page_icon='🎬')
st.title('🎥 🎞️ Genre Mint ')
st.write('Here .. Have Some Popcorn .. 🍿')
st.write("Based on the Dataset : [TMDB 5000 Movie Dataset](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata)")
st.write("About Me .. CLICK HERE =>  : [My Portfolio ](https://advaithsid.web.app/)")
st.markdown('<style> body {background-image: url("cine.jpg");}  </style>',unsafe_allow_html=True)
with st.expander('What is Genre Mint ?'):
  st.success('We give you Performance in order of revenue of each genre from 1986 to 2016 ')
  st.markdown('**What can this app do?**')
  st.info('This application demonstrates the utilization of Pandas for manipulating data, Altair for generating graphs, and an editable dataframe for interacting with the data.')
  st.markdown('**How to use the app?**')
  st.warning('In order to interact with the application, 1. Choose your preferred genres from the drop-down menu and then 2. Choose the time frame of the year using the slider tool. Consequently, this will produce a revised DataFrame that can be edited and a line plot.')
  
st.subheader('Lets Find out Revenue Pressure ($) of Each Genre in the World of Cinema ')

# Load data
df = pd.read_csv('./movies.csv')
df.year = df.year.astype('int')
# Input widgets
## Genres selection
genres_list = df.genre.unique()
genres_selection = st.multiselect('**Select genres**', genres_list, ['Action', 'Adventure', 'Biography', 'Comedy', 'Drama', 'Horror'])

## Year selection
year_list = df.year.unique()
year_selection = st.slider('**Select year duration**', 1986, 2006, (2000, 2016))
year_selection_list = list(np.arange(year_selection[0], year_selection[1]+1))
st.write('Data')

df_selection = df[df.genre.isin(genres_selection) & df['year'].isin(year_selection_list)]
reshaped_df = df_selection.pivot_table(index='year', columns='genre', values='gross', aggfunc='sum', fill_value=0)
reshaped_df = reshaped_df.sort_values(by='year', ascending=False)


# Display DataFrame

df_editor = st.data_editor(reshaped_df, height=212, use_container_width=True,
                            column_config={"year": st.column_config.TextColumn("Year")},
                            num_rows="dynamic")
df_chart = pd.melt(df_editor.reset_index(), id_vars='year', var_name='genre', value_name='gross')

# Display chart
chart = alt.Chart(df_chart).mark_line().encode(
            x=alt.X('year:N', title='Year'),
            y=alt.Y('gross:Q', title='Gross earnings ($)'),
            color='genre:N'
            ).properties(height=320)
st.write('Chart - 1')

st.altair_chart(chart, use_container_width=True)
st.write('Chart - 2')

import plotly.graph_objects as go

# Create a scatter plot with lines
fig = go.Figure()

# Add lines for each genre
for genre, data in df_chart.groupby('genre'):
    fig.add_trace(go.Scatter(x=data['year'], y=data['gross'], mode='lines+markers', name=genre))

# Update layout
fig.update_layout(xaxis_title='Year', yaxis_title='Gross earnings ($)', height=400)

# Display Plotly figure using Streamlit
st.plotly_chart(fig)
