import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
def main():
    df = pd.read_csv('all.csv')
    st.title('주식추천')
    st.subheader('주식 변동 추이')
    stocks = sorted(df['Name'].unique())
    selected_stocks = st.sidebar.multiselect('Select Brands', stocks, default=stocks[0])
    
    start_date = st.sidebar.date_input('Start Date')
    end_date = st.sidebar.date_input('End Date')
    start_date = start_date.strftime('%Y-%m-%d')
    end_date = end_date.strftime('%Y-%m-%d')
    fig = go.Figure()
    for stock in selected_stocks:
        stock_data = df[(df['Name'] == stock) & (df['Date'] >= start_date) & (df['Date'] <= end_date)]
        fig.add_trace(go.Scatter(x=stock_data['Date'], y=stock_data['Close'], name=stock))
        price_diff = stock_data['Close'].diff()
        color = ['blue' if diff < 0 else 'red' for diff in price_diff]
        
        fig.add_trace(go.Bar(x=stock_data['Date'], y=stock_data['High'] - stock_data['Low'],
            base=stock_data['Low'], name='Price Range', marker=dict(color=color)))
        fig.update_layout(
        title='주식 가격 변동 추이',
        xaxis_title='날짜',
        yaxis_title='주식 가격',
        hovermode='x',
        legend=dict(orientation='h', yanchor='bottom', y=1.02),
        barmode='stack',
        autosize=False,
        width=800,
        height=500
        )
    st.plotly_chart(fig)
if __name__ == '__main__':
    main()
