import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests

st.title('요청/처리 건수(hour)')

def load_data():
    url = 'http://43.202.66.118:8009/all'
    r = requests.get(url)
    d = r.json()
    return d

data = load_data()
df = pd.DataFrame(data)

df['request_time'] = pd.to_datetime(df['request_time'])
df['req_time'] = df['request_time'].dt.strftime('%Y-%m-%d %H')
y = df.groupby('req_time').count()

plt.bar(y.index, y['num'], color = 'green')
bar = plt.bar(y.index, y['num'], color = 'green')
#plt.plot(x, y, label = 'y')

# 값 넣는 부분
for rect in bar:
    height = rect.get_height()
    plt.text(rect.get_x() + rect.get_width()/2.0, height, '%.1f' % height, ha='center', va='bottom', size = 12)

plt.xticks(rotation=45)
plt.xlabel("Request Time")
plt.ylabel("Number of Requests")
plt.title("Requests by Date and Time")
st.pyplot(plt)
