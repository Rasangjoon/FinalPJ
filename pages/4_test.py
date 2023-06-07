import streamlit as st
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt

def main():
    df = pd.read_csv('all.csv')
    st.title('주린이들을 위한 주식추천')

    st.subheader('주식 변동 추이')

    stocks = sorted(df['Name'].unique())

    # 사이드 바에서 종목명 선택
    selected_stock = st.sidebar.selectbox('Select Brand', stocks)

    # 선택된 종목 데이터만 필터링
    df_filtered = df[df['Name'] == selected_stock]

    # 데이터 전처리: 전날 대비 등락 여부 계산
    df_filtered['Change'] = df_filtered['Close'].diff()
    df_filtered['Change_color'] = ['Up' if x >= 0 else 'Down' for x in df_filtered['Change']]

    # 차트의 크기 설정
    chart_height = st.sidebar.slider("Chart Height", 200, 800, 500)

    # 선 그래프 생성 (종가)
    line_chart = alt.Chart(df_filtered).mark_line().encode(
        x="Date:T",
        y=alt.Y("Close:Q", title="Close"),
        color=alt.Color(
            "Change_color:N",
            scale=alt.Scale(domain=['Up', 'Down'], range=['red', 'blue']),
            legend=alt.Legend(title="Price Change")
        )
    )

    # 바 그래프 생성 (고가와 저가)
    bar_chart = alt.Chart(df_filtered).mark_bar().encode(
        x="Date:T",
        y=alt.Y("Low:Q", title="Low"),
        y2="High:Q",
        color=alt.Color(
            "Change_color:N",
            scale=alt.Scale(domain=['Up', 'Down'], range=['red', 'blue']),
            legend=None
        )
    )

    # 차트 합치기
    chart = alt.layer(line_chart, bar_chart).resolve_scale(y="independent").properties(
        width=800,  # 그래프의 너비 조정
        height=chart_height  # 그래프의 높이 조정
    ).interactive()

    st.altair_chart(chart)
    
    
    def visualize_stock_data(df):
    # 데이터 전처리: 전날 대비 등락율 계산
        df['Change_pct'] = df['Close'].pct_change() * 100

        # 그래프 크기 설정
        plt.figure(figsize=(12, 6))

        # 선 그래프 (종가)
        plt.plot(df['Date'], df['Close'], label='Close', color='black')

        # 바 그래프 (고가와 저가)
        plt.bar(df['Date'], df['High'] - df['Low'], bottom=df['Low'], color=['red' if c > 0 else 'blue' for c in df['Change_pct']], alpha=0.5)

        # 전날 대비 상승/하락 여부에 따라 색상 표시
        for i in range(1, len(df)):
            if df['Change_pct'].iloc[i] > 0:
                plt.axvspan(df['Date'].iloc[i - 1], df['Date'].iloc[i], color='red', alpha=0.1)
            elif df['Change_pct'].iloc[i] < 0:
                plt.axvspan(df['Date'].iloc[i - 1], df['Date'].iloc[i], color='blue', alpha=0.1)

        # 그래프 제목과 레이블 설정
        plt.title('Stock Price Analysis')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.legend()

        # 그래프 출력
        plt.show()

    # 데이터 로드
    df = pd.read_csv('all.csv')

    # 종목 선택
    selected_stocks = ['삼성전자']  # 원하는 종목 입력

    # 종목 필터링
    df_filtered = df[df['Name'].isin(selected_stocks)]

    # 그래프 시각화
    visualize_stock_data(df_filtered)
    
    

if __name__ == '__main__':
    main()