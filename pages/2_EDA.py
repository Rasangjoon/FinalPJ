import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import plotly.express as px
from datetime import datetime
import plotly.graph_objects as go

def main():
    df = pd.read_csv('all.csv')
    st.title('주린이들을 위한 주식추천')

    st.subheader('주식 변동 추이')

    stocks = sorted(df['Name'].unique())

    date = sorted(df['Date'].unique())

    # 사이드 바에서 종목명과 날짜를 고를 수 있게.
    selected_stocks = st.sidebar.multiselect('Select Brands', stocks, default=stocks)
    start_year, end_year = st.sidebar.select_slider('Select Year Range', options=date, value=(date[0], date[-1]))

    # 선택에 맞게 필터 만들기
    mask = (
        df['Name'].isin(selected_stocks) &
        (df['Date'] >= start_year) & (df['Date'] <= end_year)
    )
    df_filtered = df.loc[mask]

    # y_value를 선택하면 나올 수 있게 만들기
    y_values = st.sidebar.multiselect("Select y value", ["Close", "Open", "High", "Low", "Change", "MA_5", "slow_%K", "slow_%D,","RSI"])

    # 라인 차트에 필터링을 추가
    line_charts = []
    for y_value in y_values:
        chart = alt.Chart(df_filtered).mark_line().encode(
            x="Date:T",
            y=alt.Y(y_value + ":Q", title=y_value),
            color="Name:N"
        ).properties(
            width=1000,
            height=600
        )
        line_charts.append(chart)

    combined_chart = alt.vconcat(*line_charts)
    st.altair_chart(combined_chart)

    
    #당일 종가 및 전날 대비 등락율 계산
    df["Change"] = df["Close"].diff()
    
    df["Change_pct"] = df["Change"] / df["Close"].shift() * 100
    # 최신 데이터 가져오기
    latest_close = df["Close"].iloc[-1]
    latest_change_pct = df["Change_pct"].iloc[-1]

    # 등락 여부에 따라 색상 설정
    if latest_change_pct > 0:
        change_color = "red"
    elif latest_change_pct < 0:
        change_color = "blue"
    else:
        change_color = "black"

    # 당일 종가 메트릭 표시
    st.metric("Latest Close Price", f"{latest_close:.2f}원")

    # 전날 대비 등락율 텍스트 표시
    st.markdown(f"<font color='{change_color}'>Change: {latest_change_pct:.2f}%</font>", unsafe_allow_html=True)
    
    #파이차트: 점수 합 비율을 넣는 것 약간 매수/매도 사인 비슷할 수 있음.
    # 날씨 이미지(이모지: 크기가 조정 가능할 때), 주가 시계열 데이터 그래프, 전일 종가 데이터, 
    #CSV로 만든 그래프로 MA-5, CHANGE 보고 5일 합으로 이미지 출력하게 
    #세영님 코드 참고해서 해보기.
    

    
if __name__ == '__main__' :
    main()
#C:\Users\82106\Desktop\workspace\final project\Stock_price (2)\samsung.csv
