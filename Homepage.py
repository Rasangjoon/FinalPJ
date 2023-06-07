import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import plotly.express as px
from datetime import datetime

st.set_page_config(
    page_title='Multipage App',
    page_icon = "!@!@",
)

st.header(" - 💹주가, 기사, 재무제표 분석을 통한 데이터 분석")
st.sidebar.success("Select a page above.")

def main():
    st.markdown(
    """
    ### 1. 프로젝트 목적
    - 주식 투자 초심자들이 정보 탐색 인풋을 줄이고 안정적으로 자산을 운용할 수 있게 돕기 위해
    ### 2. 프로젝트 개요
    - 주가, 기사, 재무제표 데이터를 바탕으로 종목의 주가를 분석.
    - 매도/매수 정보를 정리하여 시각화하고 그 인사이트를 제공해주는 서비스를 구현.
    
    
    """
    )
    
    
    st.write("This is some text.")
    df=pd.read_csv('samsung1.csv')
    df1=pd.read_csv('Hyundai Motor Company.csv')
    df2=pd.read_csv('POSCO.csv')
    df3=pd.read_csv('Celltrion.csv')
    df4=pd.read_csv('Samsung life Insurance.csv')
    
    #여기다가는 상승 하락을 나타내주는것을 표시하면 어떨까?
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    with col1:
        st.header('text')
    
    with col2:
        st.header('text')
    
    with col3:
        st.header('text')
        
    with col4:
        st.header('text')
        
    with col5:
        st.header('text')
        
    with col6:
        st.header('text')    
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["삼성전자", "현대차", "포스코", "셀트리온", "삼성생명"])
    
    with tab1:
        st.header("삼성전자")
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
    
    with tab2:
        st.header("현대차")
         #당일 종가 및 전날 대비 등락율 계산
        df1["Change"] = df1["Close"].diff()
        
        df1["Change_pct"] = df1["Change"] / df1["Close"].shift() * 100
        # 최신 데이터 가져오기
        latest_close = df1["Close"].iloc[-1]
        latest_change_pct = df1["Change_pct"].iloc[-1]

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
        
    with tab3:
        st.header("포스코")
        df2["Change"] = df2["Close"].diff()
        
        df2["Change_pct"] = df2["Change"] / df2["Close"].shift() * 100
        # 최신 데이터 가져오기
        latest_close = df2["Close"].iloc[-1]
        latest_change_pct = df2["Change_pct"].iloc[-1]

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
        
    with tab4:
        st.header("셀트리온")
        df3["Change"] = df3["Close"].diff()
        
        df3["Change_pct"] = df3["Change"] / df3["Close"].shift() * 100
        # 최신 데이터 가져오기
        latest_close = df3["Close"].iloc[-1]
        latest_change_pct = df3["Change_pct"].iloc[-1]

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
    with tab5:
        st.header("삼성생명")
        df4["Change"] = df4["Close"].diff()
        
        df4["Change_pct"] = df4["Change"] / df4["Close"].shift() * 100
        # 최신 데이터 가져오기
        latest_close = df4["Close"].iloc[-1]
        latest_change_pct = df4["Change_pct"].iloc[-1]

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
        
    



    

    
    #st.title("Title")
    #st.header("Header")
    #st.subheader("Subheader")
    
    #st.write("Write")
    
    
    
    
    #st.header("목적")
    #st.write ("주식 투자 초심자들이 정보탐색 인풋을 줄이고 안정적으로 자산을 운용할 수 있게 돕기 위해")

    
if __name__ == '__main__' :
    main()
    
