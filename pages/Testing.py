import datetime as dt
import pandas as pd
import yfinance as yf
import financedatabase as fd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
if 'user' not in st.session_state:
    st.warning("Please log in first.")
    st.stop()










st.set_page_config(layout="wide", initial_sidebar_state = "expanded")
st.title("Investment Earnings Testing")

@st.cache_data
def load_data():
    ticker_list = fd.Equities().select().reset_index()[['symbol', 'name']]
    ticker_list = ticker_list[ticker_list.symbol.notna()]
    ticker_list['symbol_name'] = ticker_list.symbol + '-' + ticker_list.name
    return ticker_list
ticker_list = load_data()

with st.sidebar:
    sel_ticker = st.text_input("Enter Stock").upper()
    sel_date1 = st.date_input('Start Date', value=dt.datetime(2024,1,1), format='MM-DD-YYYY')
    sel_date2 = st.date_input('End Date', format='MM-DD-YYYY')
yfdata = None
if len(sel_ticker) == 0:
    st.info('Select options')
elif sel_ticker:  
    sel_ticker_row = ticker_list[ticker_list.symbol == sel_ticker]
    if len(sel_ticker_row) != 0:
        symbol = sel_ticker_row.symbol.values[0]
        yfdata = yf.download(symbol, 
                            start=sel_date1, 
                            end=sel_date2)['Close'].reset_index().melt(id_vars = ['Date'], 
                            var_name = 'ticker', 
                            value_name='price')
        yfdata['price_start'] = yfdata.groupby('ticker').price.transform('first')
        yfdata['price_pct_daily'] = yfdata.groupby('ticker').price.pct_change()
        yfdata['price_pct'] = (yfdata.price - yfdata.price_start) / yfdata.price_start
    else:
        st.warning("Stock not found.")











if yfdata is not None:
    column = st.columns((0.3,.7))
    cols = column[0].columns((0.1, 0.2))
    cols[0].subheader(sel_ticker)
    amount = cols[1].number_input('', key=sel_ticker, step = 50)
    st.empty()
    cols_goal = column[1].columns((0.13,0.2,0.7))
    cols_goal[0].subheader('Goal:')
    goal = cols_goal[1].number_input('', key='goal', step = 50)

    df = yfdata.copy()
    df['amount'] = amount * (1 + df.price_pct)

    figure = px.area(df, x='Date', y='amount', color='ticker')
    figure.add_hline(y=goal, line_color='rgb(255, 0, 0)', line_width=2)
    goal_achieved = df[df['amount'] >= goal]
    if goal_achieved.empty:
        column[1].warning("The goal can not be reached.")
    else:
        goal_date = goal_achieved['Date'].iloc[0]
        figure.add_vline(x=goal_date, line_color='rgb(255, 0, 0)', line_width=2)
        figure.add_trace(go.Scatter(x=[goal_date + dt.timedelta(days=7)], 
                                    y=[goal*1.1], 
                                    text=[goal_date.date()], 
                                    mode='text', 
                                    name="Goal Date", 
                                    textfont=dict(color='rgb(0,0,0)', 
                                    size=30)))
    figure.update_layout(xaxis_title="Date", yaxis_title="Price")
    column[1].plotly_chart(figure, use_container_width=True)