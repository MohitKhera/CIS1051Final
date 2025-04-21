import streamlit as st
from datetime import date
import yfinance as yf

if 'user' not in st.session_state:
    st.warning("Please log in first.")
    st.stop()

@st.cache_data
def stock_info(symbol):
    stock = yf.Ticker(symbol)
    if "longName" in stock.info:
        return stock.info
    return None

@st.cache_data
def price_history(symbol):
    stock = yf.Ticker(symbol)
    return stock.history(period = '1y', interval = '1wk')

st.title("Dashboard")
symbol = st.text_input("Enter Stock")

if symbol == "":
    st.warning("Enter a stock")
else:
    info = stock_info(symbol)
    if info is None:
        st.warning("Enter a valid stock")
    else:
        st.header("Company Information")
        st.subheader(f'Name: {info["longName"]}')
        st.subheader(f'Market Cap: {info["marketCap"]}')
        st.subheader(f'Sector: {info["sector"]}')
        st.subheader(f'Current Price: ${info["currentPrice"]}')