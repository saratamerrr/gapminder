import pandas as pd
import streamlit as st
import plotly.express as px

# Load CSV files
@st.cache_data
def load_data(file_path):
    df = pd.read_csv(file_path)
    return df

population_df = load_data('pop.csv')
life_expectancy_df = load_data('lex.csv')
gni_per_capita_df = load_data('gni.csv')

# Impute missing values using forward filling
population_df = population_df.ffill()
life_expectancy_df = life_expectancy_df.ffill()
gni_per_capita_df = gni_per_capita_df.ffill()

# Transform dataframes into tidy format
population_df = population_df.melt(id_vars=['country'], var_name='year', value_name='population')
life_expectancy_df = life_expectancy_df.melt(id_vars=['country'], var_name='year', value_name='life_expectancy')
gni_per_capita_df = gni_per_capita_df.melt(id_vars=['country'], var_name='year', value_name='gni_per_capita')

# Merge dataframes
merged_df = pd.merge(population_df, life_expectancy_df, on=['country', 'year'])
merged_df = pd.merge(merged_df, gni_per_capita_df, on=['country', 'year'])

# Streamlit app
st.title('Global Indicators Dashboard')

# Interactive widgets
selected_year = st.slider('Select a year', min_value=int(merged_df['year'].min()), 
                          max_value=int(merged_df['year'].max()), value=int(merged_df['year'].max()))

selected_countries = st.multiselect('Select countries', merged_df['country'].unique())

# Filter data by selected year and countries
filtered_df = merged_df[(merged_df['year'] == str(selected_year)) & (merged_df['country'].isin(selected_countries))]

# Bubble chart
fig = px.scatter(filtered_df, x='gni_per_capita', y='life_expectancy', size='population', color='country', 
                 log_x=True, hover_name='country', size_max=60)
fig.update_layout(title='Global Indicators',
                  xaxis_title='Logarithmic GNI per capita (PPP)',
                  yaxis_title='Life Expectancy',
                  showlegend=True)

st.plotly_chart(fig)
