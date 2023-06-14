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
        fig.add_trace(go.Scatter(x=stock_data['Date'], y=stock_data['Close'], name=stock,
                                 hovertemplate='날짜: %{x}<br>주식 가격: %{y:.0f}'))
        price_diff = stock_data['Close'].diff()
        color = ['blue' if diff < 0 else 'red' for diff in price_diff]
        fig.add_trace(go.Bar(x=stock_data['Date'], y=stock_data['High'] - stock_data['Low'],
                             base=stock_data['Low'], name='Price Range', marker=dict(color=color),
                             hovertemplate='날짜: %{x}<br>가격 범위: %{y:.0f}'))

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

    with st.expander('추가 그래프'):
        st.subheader('추가 그래프 선택')
        options = ['SLOW STC', 'MA']
        selected_graphs = st.multiselect('그래프를 선택하세요', options)

        for stock in selected_stocks:
            stock_data = df[(df['Name'] == stock) & (df['Date'] >= start_date) & (df['Date'] <= end_date)]

            if 'SLOW STC' in selected_graphs:
                st.subheader(f'SLOW STC - {stock}')
                fig_slow_stc = go.Figure()
                fig_slow_stc.add_trace(go.Scatter(x=stock_data['Date'], y=stock_data['slow_%K'], name='slow_%K',
                                                  hovertemplate='날짜: %{x}<br>SLOW %K: %{y:.0f}'))
                fig_slow_stc.add_trace(go.Scatter(x=stock_data['Date'], y=stock_data['slow_%D'], name='slow_%D',
                                                  hovertemplate='날짜: %{x}<br>SLOW %D: %{y:.0f}'))
                st.plotly_chart(fig_slow_stc)

            if 'MA' in selected_graphs:
                st.subheader(f'MA - {stock}')
                fig_ma = go.Figure()
                fig_ma.add_trace(go.Scatter(x=stock_data['Date'], y=stock_data['MA_5'], name='MA_5',
                                            hovertemplate='날짜: %{x}<br>MA_5: %{y:.0f}'))
                fig_ma.add_trace(go.Scatter(x=stock_data['Date'], y=stock_data['MA_10'], name='MA_10',
                                            hovertemplate='날짜: %{x}<br>MA_10: %{y:.0f}'))
                st.plotly_chart(fig_ma)

if __name__ == '__main__':
    main()