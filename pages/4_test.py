import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt
import plotly.graph_objects as go
from bokeh.plotting import figure
from bokeh.models import HoverTool, ColumnDataSource
import plotly.express as px

def main():
    tab11, tab12, tab13, tab14, tab15 = st.tabs(["상관관계 분석","박스플롯","거래량 변동","등락률 산점도","테스트3"])
    with tab11:
        df = pd.read_csv('all.csv')


        st.title('주식추천')
        st.subheader('변수 간 상관관계 히트맵')

        # 필요한 변수들 선택
        selected_columns = ['Open', 'High', 'Low', 'Close', 'Volume', 'Change', 'Code', 'MA_5', 'fast_%K', 'slow_%K',
                            'slow_%D', 'RSI', 'STD', 'Upper', 'Lower', 'fast_10', 'Score', 'pos_score', 'MA_10']
        data = df[selected_columns]

        # 상관계수 계산
        correlation = data.corr()

        # 히트맵 생성
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(correlation, cmap='coolwarm', annot=True, fmt=".2f", annot_kws={"fontsize": 8}, ax=ax)

        # 그래프 출력
        st.pyplot(fig)

        st.subheader('상관관계가 높은 변수들:')
        # 상관관계가 0.5보다 큰 변수들 출력
        high_correlation = correlation.unstack().reset_index()
        high_correlation = high_correlation[high_correlation['level_0'] != high_correlation['level_1']]
        high_correlation.columns = ['Variable 1', 'Variable 2', 'Correlation']
        high_correlation = high_correlation.dropna()
        high_correlation = high_correlation.drop_duplicates(subset=['Correlation'], keep='first')
        high_correlation = high_correlation.sort_values(by='Correlation', ascending=False)
        high_correlation.reset_index(drop=True, inplace=True)  # 인덱스 초기화

        # 변수들을 정비례 관계와 반비례 관계로 분할
        positive_correlation = high_correlation[high_correlation['Correlation'] > 0]
        negative_correlation = high_correlation[high_correlation['Correlation'] < 0]

        # Streamlit의 columns 레이아웃을 사용하여 col1, col2로 분할하여 출력
        col1, col2, col3 = st.columns(3)

        with col1:
            st.subheader('모든 변수')
            st.write(high_correlation)

        with col2:
            st.subheader('정비례 관계')
            st.write(positive_correlation)
        
        with col3:
            st.subheader('반비례 관계')
            st.write(negative_correlation)
            
        
        st.title('상관관계에 따른 산점도 그래프')
        st.header("-------")

        

        # 사용자 입력을 받아 상위 순위 선택
        threshold_options = [0.95, 0.96, 0.97, 0.98, 0.99]
        
        threshold_input = col2.selectbox('상관관계의 임계값을 선택하세요:', threshold_options)
        
        # 버튼 클릭 시 산점도 그래프 출력
        if col2.button('그래프 그리기'):
            for _, row in high_correlation.iterrows():
                var1 = row['Variable 1']
                var2 = row['Variable 2']
                corr = row['Correlation']

                if corr >= threshold_input:
                    plt.figure(figsize=(8, 6))
                    sns.scatterplot(data=data, x=var1, y=var2)
                    # 반올림 되지 않게 소수점 4자리까지 확인
                    plt.title(f'{var1} vs {var2} (Correlation: {corr:.4f})')
                    plt.xlabel(var1)
                    plt.ylabel(var2)
                    plt.show()
                    st.pyplot(plt)
                
    with tab12:
        df = pd.read_csv('all.csv')

        # 선택한 종목 리스트
        selected_stocks = ['Samsung_electronic', 'Hyundai Motor Company', 'POSCO', 'Samsung life Insurance', 'Celltrion']


        # 선택한 종목들의 데이터 필터링
        filtered_df = df[df['Name'].isin(selected_stocks)]

        # 중앙값을 계산
        median_df = filtered_df.groupby('Name')['Close'].median().reset_index()

        # 이상치를 제외한 데이터를 필터링
        filtered_data = filtered_df[~filtered_df['Close'].isin(median_df['Close'])]

        # Boxplot을 생성하기 위한 데이터 준비
        boxplot_data = []
        for name, group in filtered_df.groupby('Name'):
            boxplot_data.append(go.Box(
                name=name,
                y=group['Close'],
                boxpoints='outliers',
                marker=dict(color='rgb(107, 174, 214)'),
                line=dict(color='rgb(8, 81, 156)')
            ))

        # 중앙값을 표시하기 위한 Scatter 데이터 준비
        scatter_data = []
        for name, group in median_df.groupby('Name'):
            scatter_data.append(go.Scatter(
                name=name,
                x=[name],
                y=group['Close'],
                mode='markers',
                marker=dict(color='red', size=8),
            ))

        # 그래프 레이아웃 설정
        layout = go.Layout(
            title='주식 종가의 분포와 중앙값 비교',
            xaxis=dict(title='종목'),
            yaxis=dict(title='종가'),
            showlegend=False
        )

        # Boxplot과 Scatterplot을 결합한 Figure 생성
        fig = go.Figure(data=boxplot_data + scatter_data, layout=layout)

        # 그래프 출력
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("박스플롯(Box plot)이란? : 중앙값, 이상치, 분포 등을 시각화하고 파악하는데 도움이 되는 그래프.")
        st.write("1. 2018년부터 2023년까지 셀트리온, 포스코, 현대자동차는 사분위 범위(박스의 높이)를 보면 주식 가격의 변동에 커다란 변화가 있었음을 알 수 있음.")
        st.write("2. 2018년부터 2023년까지 삼성생명과 삼성전자는 다른 종목들에 비해 (박스플롯)q1~q3까지의 크기가 작게 형성")
        st.write("3. 삼성생명과 삼성전자가 다른 3종목보다는 안정적이라는 것을 알 수 있음.")
        st.write("4. 하지만 삼성생명에서 박스의 위와 아래에 있는 가로선을 벗어난 데이터 포인트(이상치)를 발견.")
        st.write("5. ")
    
    with tab13:
            #(3) 날짜 별, 연도 별 거래량 그래프 확인. ()
        df = pd.read_csv('all.csv')
        available_names = df['Name'].unique()

        # 멀티셀렉트 박스로 종목명 선택
        selected_names = st.multiselect('Select Names', available_names)

        # 선택한 종목명에 해당하는 데이터 필터링
        filtered_df = df[df['Name'].isin(selected_names)] if selected_names else df

        # 날짜를 datetime 형식으로 변환
        filtered_df['Date'] = pd.to_datetime(filtered_df['Date'])

        # 날짜 별 거래량 그래프
        fig1 = px.line(filtered_df, x='Date', y='Volume', color='Name',
                    title='Volume by Date', labels={'Volume': 'Volume', 'Date': 'Date'})
        fig1.update_traces(hovertemplate='Date: %{x}<br>Volume: %{y}')

        # 연도 별 거래량 그래프
        filtered_df['Year'] = filtered_df['Date'].dt.year
        yearly_volumes = filtered_df.groupby(['Year', 'Name'])['Volume'].sum().reset_index()
        fig2 = px.bar(yearly_volumes, x='Year', y='Volume', color='Name',
                    title='년도별 거래량 추이', labels={'Volume': 'Volume', 'Year': 'Year'})
        fig2.update_traces(hovertemplate='Year: %{x}<br>Volume: %{y}')

        # 거래량 최소값, 최대값 표시
        min_year = filtered_df['Date'].dt.year.min()
        max_year = filtered_df['Date'].dt.year.max()
        min_volume = filtered_df[filtered_df['Date'].dt.year == min_year]['Volume'].min()
        max_volume = filtered_df[filtered_df['Date'].dt.year == max_year]['Volume'].max()

        fig1.update_layout(annotations=[
            dict(x=min_year, y=min_volume, xref='x', yref='y',
                text=f"Min Volume: {min_volume}", showarrow=True, arrowhead=1, ax=0, ay=-40),
            dict(x=max_year, y=max_volume, xref='x', yref='y',
                text=f"Max Volume: {max_volume}", showarrow=True, arrowhead=1, ax=0, ay=-60)
        ])

        fig2.update_layout(annotations=[
            dict(x=min_year, y=yearly_volumes[yearly_volumes['Year'] == min_year]['Volume'].min(),
                xref='x', yref='y',
                text="Min Volume", showarrow=True, arrowhead=1, ax=0, ay=-40),
            dict(x=max_year, y=yearly_volumes[yearly_volumes['Year'] == max_year]['Volume'].max(),
                xref='x', yref='y',
                text="Max Volume", showarrow=True, arrowhead=1, ax=0, ay=-60)
        ])

        fig1.update_layout(width=1000, height=600)
        fig2.update_layout(width=800, height=600)

        # 그래프 출력
        st.plotly_chart(fig1)
        st.plotly_chart(fig2)
        
        with tab14:

            # 등락률과 날짜 데이터 추출
            changes = df['Change']
            dates = pd.to_datetime(df['Date'])

            # 등락률의 양수값과 음수값 분리
            positive_changes = changes[changes > 0]
            negative_changes = changes[changes < 0]

            # 그래프 생성
            fig = go.Figure()

            # 양수 등락률 산점도 추가
            fig.add_trace(go.Scatter(
                x=dates[changes > 0],
                y=positive_changes,
                mode='markers',
                marker=dict(color='green', size=3),
                name='Positive Changes'
            ))

            # 음수 등락률 산점도 추가
            fig.add_trace(go.Scatter(
                x=dates[changes < 0],
                y=negative_changes,
                mode='markers',
                marker=dict(color='red', size=3),
                name='Negative Changes'
            ))

            # 레이아웃 설정
            fig.update_layout(
                title="등락률",
                xaxis=dict(title="Date"),
                yaxis=dict(title="Change"),
                hovermode="x",
                width=900,  # 그래프 전체 가로 크기 조정
                height=500  # 그래프 전체 세로 크기 조정
            )

            # 그래프 출력
            st.plotly_chart(fig)
            
        #(4) 날짜에 따른 등락률 분포 확인(산점도).
        #with tab15:   
        #(5) 거래량의 합계 계산. 

if __name__ == '__main__':
    main()