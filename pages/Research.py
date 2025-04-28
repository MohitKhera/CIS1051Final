import streamlit as st
from datetime import date
import yfinance as yf
import plotly.graph_objects as go

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
        st.subheader(f'Current Price: ${info["currentPrice"]}')
        price_history = price_history(symbol)
        st.header("Stock Price Chart")
        price_history = price_history.rename_axis('Date').reset_index()
        chart = go.Figure(data=[go.Candlestick(x=price_history['Date'],
                                               open=price_history['Open'],
                                               low=price_history['Low'],
                                               high=price_history['High'],
                                               close=price_history['Close'])])
        st.plotly_chart(chart, use_container_width=True)
