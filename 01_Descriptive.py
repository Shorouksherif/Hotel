import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv('df.csv')

df.drop('Unnamed: 0', axis=1, inplace= True)

# Set up the Streamlit page configuration
st.set_page_config(
    layout='wide',
    page_title='Descriptive Analysis',
    page_icon='📊'
)

st.markdown('<h1 style="text-align:center; color: #4169E1;">Descriptive Analysis</h1>', unsafe_allow_html=True)

# Create tabs for different analyses
tap1, tap2 = st.tabs(['📈 Numeric', '📊 Categorical'])

num = df.describe()
cat = df.describe(include='O')
with tap1:
    st.subheader('Numerical Descriptive Statistics')
    st.dataframe(num.T, 500, 400)
with tap2:
    st.subheader('Categorical Descriptive Statistics')
    st.dataframe(cat.T, 500, 400)
