import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#import plotly as px
import seaborn as sns
#import matplotlib.pyplot as plt



# page config
st.set_page_config(page_title="Africa food prices", layout='wide',initial_sidebar_state='expanded', page_icon='📊')
#with open('style.css') as f:
#    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Title
st.title(" 📊  Africa food prices - Web App")
st.markdown("##")
@st.cache_data
def load_data():
    #df = pd.read_csv("africa_food_prices.csv")
    df = pd.read_csv('https://www.kaggle.com/datasets/jogwums/python-mini-project-2022')
    # dropping columns
    df.drop(columns=['Unnamed: 0','mp_commoditysource','currency_id','country_id',
                 'market_id','state_id','produce_id','pt_id','quantity'],  inplace= True)

    # fiiling none columns state
    df['state'].fillna('unknown', inplace=True)
    #df['year'] = df.year.replace(',', '.')
    
    #renaming two columns
    df.rename({'um_unit_id': 'exchanged_qty'}, axis=1, inplace=True)
    #cleaning produce column and renaming it
    df['core_produce'] = df['produce'].str.extract(r'([^\(]+)')
    df['core_produce'] = df['core_produce'].str.split('-').str[0]
    df['core_produce'] = df['core_produce'].str.strip()
    return df


df = load_data()
#st.subheader("Data  Preview")
#st.dataframe(df.tail())
st.sidebar.title("filters")
produces = df['core_produce'].unique()
years = df['year'] = df.year.replace(',', '')
years = df['year'].unique()
countries = df['country'].unique()
no_exchanged =df['exchanged_qty'].sum()
sumPrice =df['price'].sum().round(2)
naija = df[df['country'] == 'Nigeria']


#lengths
no_produces = len(produces)
no_years = len(years)
no_countries = len(countries)

# create a multislect for produces
selected_produces = st.sidebar.multiselect("select products", produces,[produces[0]])
selected_years = st.sidebar.multiselect("Select year", years,[years[0]])
selected_countries = st.sidebar.multiselect("select country", countries,[countries[0]])



# display in columns
st.markdown('###')
col1, col2, col3 = st.columns(3)
col1.metric("No of produce", f'{no_produces:,}')
col2.metric("Total Price", f'{sumPrice:,}')
col3.metric("Quantity exchanged", f'{no_exchanged:,}')



# returning filtered table
new_table = df.query("core_produce == @selected_produces & year == @selected_years & country == @selected_countries")
no_new_table = new_table['produce'].nunique()

#catching error
st.subheader("Filtered tables")
if not selected_produces:
    st.error("select an article")
elif not selected_years:
    st.error("select year")
elif not selected_countries: 
    st.error("select country")
elif new_table.empty:
    st.warning("No data available based on the current filter settings!")
    st.stop() # This will halt the app from further execution.
else:
    st.dataframe(new_table.sample(3))

# calculations
total_produce_selected = len(selected_produces)
total_selected_country = len(selected_countries)
no_years_selected = len(selected_years)

# display in columns
col1,col2,col3 = st.columns(3)
if total_produce_selected:
    col1.metric("Produce selected",f'{total_produce_selected:,}')
else:
    col1.metric("No of produce to pick from", f'{no_produces:,}')
if total_selected_country:
    col3.metric("Countries selected",f'{total_selected_country:,}')
else:
    col3.metric("Countries to pick from", f'{no_countries:,}')
if no_years_selected:
    col2.metric("Years selected",f'{no_years_selected:,}')
else:
    col2.metric("Years to pic from", f'{no_years:,}')







c1, c2 = st.columns((5,5))
with c1:
    grouped_marketype = new_table.groupby('market_type')['price'].sum().reset_index()
    grouped_marketype = grouped_marketype.sort_values(by = 'price', ascending = False)
    st.subheader("Market Type")
    fig2, ax2 = plt.subplots(figsize=(7,2))
    ax2.pie(grouped_marketype['price'], labels=grouped_marketype['market_type'], autopct="%1.1f%%")
    st.pyplot(fig2)
    
with c2:
    st.subheader("Average price per country")
    country_grp = df.groupby('country')['price'].mean()
    country_grp = country_grp.sort_values(ascending=False)[:-3]
    table = country_grp.reset_index()
    filtered_table = table[table['country'].isin(selected_countries)]
    fig1, ax = plt.subplots(figsize=(11,9.5))
    sns.barplot( x= filtered_table['country'], y= filtered_table['price'], ax=ax)
    ax.tick_params(axis="x", labelsize=10)
    ax.tick_params(axis="y", labelsize=10)
    st.pyplot(fig1)











c1, c2 = st.columns((5,5))
with c1:
    st.subheader("Bar chart price volatility per state")
    state_volatility = new_table.groupby('state')['price'].std().sort_values(ascending=False)
    fig9, ax9 = plt.subplots(figsize=(10,6))
    ax9.bar(new_table['state'], new_table['price'])
    st.pyplot(fig9)


with c2:


    st.subheader("Price volatility per country")
    country_volatility = df.groupby('country')['price'].std()
    country_volatility = country_volatility.sort_values(ascending=False)[:-3]
    table = country_volatility.reset_index()
    volatility_table = table[table['country'].isin(selected_countries)]
    fig13, ax13 = plt.subplots(figsize=(10,7))
    sns.barplot( x= volatility_table['country'], y= volatility_table['price'], ax=ax13)
    ax.tick_params(axis="x", labelsize=10)
    ax.tick_params(axis="y", labelsize=10)
    st.pyplot(fig13)






st.subheader("Trend analysis")
daily_sales = df.groupby('year')['price'].sum()
fig7, ax7 = plt.subplots(figsize=(12,6))
ax7.plot(daily_sales.index, daily_sales.values)
st.pyplot(fig7)



# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)


df = load_data()
st.subheader("Data  Preview")
st.dataframe(df.tail())
st.sidebar.title("filters")
