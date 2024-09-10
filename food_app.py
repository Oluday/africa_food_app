
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

