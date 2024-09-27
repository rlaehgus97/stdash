import streamlit as st
from streamlit_option_menu import option_menu

import pandas as pd
import matplotlib.pyplot as plt
import requests

def func(x):
    if x[0] == 'n':
        return x
    
def load_data():
    url = 'http://43.202.66.118:8077/all'
    r = requests.get(url)
    d = r.json()
    return d

def main():
    st.set_page_config(layout="wide")
    with st.sidebar:
        choice = option_menu("Menu", ['원본데이터', '시각화'],
                            icons=['bi bi-people', 'bi bi-map'],
                            menu_icon="bi bi-app-indicator", default_index=0,
                            styles={
            "container": {"padding": "4!important", "background-color": "#fafafa"},
            "icon": {"color": "black", "font-size": "25px"},
            "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#fafafa"},
            "nav-link-selected": {"background-color": "#08c7b4"},
        })

    if choice == '원본데이터':
        st.title('CNN Model build')

        data = load_data()
        df = pd.DataFrame(data)
        df

        df['request_time'] = pd.to_datetime(df['request_time'])
        df['req_time'] = df['request_time'].dt.strftime("%Y-%m-%d %H")
        df_req = df.groupby('req_time').count()
        st.header('시간별 요청 건수')
        df_req
        st.divider()

        df['prediction_time'] = pd.to_datetime(df['prediction_time'])
        df['pred_time'] = df['prediction_time'].dt.strftime("%Y-%m-%d %H")
        df_pred = df.groupby('pred_time').count()
        st.header('시간별 예측 건수')
        df_pred
        st.divider()

    elif choice == '시각화':
        st.title('다양한 시각화')

        data = load_data()
        df = pd.DataFrame(data)

        df['request_time'] = pd.to_datetime(df['request_time'])
        df['req_time'] = df['request_time'].dt.strftime("%Y-%m-%d %H")
        df_req = df.groupby('req_time').count()

        df['prediction_time'] = pd.to_datetime(df['prediction_time'])
        df['pred_time'] = df['prediction_time'].dt.strftime("%Y-%m-%d %H")
        df_pred = df.groupby('pred_time').count()

        st.header('요청 / 처리 건수(h)')
        plt.bar(df_req.index, df_req['num'])
        plt.plot(df_pred.index, df_pred['num'], 'ro-')
        plt.title('Requests by Date and Time')
        plt.xlabel('Date and Time')
        plt.ylabel('Number of Requests')
        plt.xticks(rotation = 45)
        st.pyplot(plt)
        st.divider()

        st.header('요청 예측 불균형')

        df['prediction_model'] = df['prediction_model'].astype(dtype='str')
        df2 = df['prediction_model'].map(func).to_frame()
        pred_usr = df2.value_counts()
        req_usr = df[['request_user']].value_counts()
        df_usr = pd.concat([req_usr, pred_usr], axis = 1)
        df_usr.columns = ['req_count', 'pred_count']
        df_usr = df_usr.reset_index()
        df_usr = df_usr.set_index('level_0')
        df_usr = df_usr.fillna(0)

        import numpy as np
        w = 0.25
        ind = np.arange(len(df_usr))
        plt.bar(ind - w, df_usr['req_count'], width = w+0.1, label = 'request count', color = 'b')
        plt.bar(ind + w, df_usr['pred_count'], width = w+0.1, label = 'predict count', color = 'r')
        plt.xticks(ind, labels = df_usr.index)
        plt.xlabel('User')
        plt.ylabel('Count')
        plt.legend()
        st.pyplot(plt)

if __name__ == '__main__':
    main()
