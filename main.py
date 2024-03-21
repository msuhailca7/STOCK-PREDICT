import streamlit as st

st.markdown(
    """
    <style>
        body {
            background-color: #ffffff; /* White color code */
        }
    </style>
    """,
    unsafe_allow_html=True
)

from datetime import date
import yfinance as yf
from prophet import Prophet
from plotly import graph_objs as go
from prophet.plot import plot_plotly

START = "2017-01-01"
TODAY = date.today().strftime("%Y-%m-%d")
st.title("WELCOME TO STOCK PREDICT")
stocks = ("AAPL", "GOOG", "MSFT", "GME", "NVDA","RELIANCE.NS","TCS.NS","WIPRO.NS","INFOSYS.NS","TATAPOWER.NS","MRF.NS","ITC.NS","^NSEI")
selected_stock = st.selectbox("SELECT STOCK FOR PREDICTION", stocks)
n_years = st.slider("SELECT YEARS OF PREDICTION:", 1, 4)
period = n_years * 365

@st.cache_data
def load_data(ticker):
    data = yf.download(ticker, START, TODAY)
    data.reset_index(inplace=True)
    return data

data_load_state = st.text("LOAD DATA...")
data = load_data(selected_stock)
data_load_state.text("LOADING DATA...DONE!")

st.subheader('Raw data')
st.write(data.tail())

def plot_raw_data():
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name='stock_open'))
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name='stock_close'))
    fig.layout.update(title_text="Time Series Data", xaxis_rangeslider_visible=True)
    st.plotly_chart(fig)

plot_raw_data()

# Forecasting
df_train = data[['Date', 'Close']]
df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})

m = Prophet()
m.fit(df_train)
future = m.make_future_dataframe(periods=period)
forecast = m.predict(future)

st.subheader('Forecast data')
st.write(forecast.tail())

st.subheader('Forecast Plot')
fig1 = plot_plotly(m, forecast)
st.plotly_chart(fig1)

st.subheader('Forecast Components')
fig2 = m.plot_components(forecast)
st.write(fig2)


st.write("[Learn more>](https://finance.yahoo.com/)")