import streamlit as st
from streamlit_login_auth_ui.widgets import __login__
from datetime import date
import yfinance as yf
from prophet import Prophet
from prophet.plot import plot_plotly
import plotly.graph_objs as go  # Import graph_objs from Plotly

# Function to simulate the content of main.py
def main_content():
    st.title("Welcome to the Main Page")
    st.write("This is the main content of your application.")

# Initialize the login object with authentication token
__login__obj = __login__(
    auth_token="pk_prod_Q7S8YDR7CMMZB1MEW9T9Z0WMBKVP",  # Replace with your Courier auth token
    company_name="STOCK PREDICT",
    width=200, 
    height=250, 
    logout_button_name='Logout', 
    hide_menu_bool=False, 
    hide_footer_bool=False, 
    lottie_url='https://assets2.lottiefiles.com/packages/lf20_jcikwtux.json'
)

# Build the login UI
LOGGED_IN = __login__obj.build_login_ui()

# Check if the user is logged in
if LOGGED_IN:
    
    START = "2017-01-01"
    TODAY = date.today().strftime("%Y-%m-%d")
    st.title("WELCOME TO STOCK PREDICT")
    
    # Sidebar for selecting market
    market = st.sidebar.radio("SELECT MARKET", ("INDIAN MARKET", "USA MARKET"))

    # Select stock based on market
    if market == "INDIAN MARKET":
        selected_stock = st.selectbox("SELECT STOCK FOR PREDICTION", (
            "ADANIPORTS.NS", "ASIANPAINT.NS", "AXISBANK.NS", "BAJAJ-AUTO.NS", "BAJAJFINSV.NS",
            "BAJFINANCE.NS", "BHARTIARTL.NS", "BPCL.NS", "BRITANNIA.NS", "CIPLA.NS", "COALINDIA.NS",
            "DIVISLAB.NS", "DRREDDY.NS", "EICHERMOT.NS", "GRASIM.NS", "HCLTECH.NS", "HDFC.NS",
            "HDFCBANK.NS", "HDFCLIFE.NS", "HEROMOTOCO.NS", "HINDALCO.NS", "HINDUNILVR.NS", "ICICIBANK.NS",
            "INDUSINDBK.NS", "INFY.NS", "IOC.NS", "ITC.NS", "JSWSTEEL.NS", "KOTAKBANK.NS", "LT.NS", "M&M.NS",
            "MARUTI.NS", "NESTLEIND.NS", "NTPC.NS", "ONGC.NS", "POWERGRID.NS", "RELIANCE.NS", "SBILIFE.NS",
            "SBIN.NS", "SHREECEM.NS", "SUNPHARMA.NS", "TATACONSUM.NS", "TATAMOTORS.NS", "TATASTEEL.NS",
            "TCS.NS", "TECHM.NS", "TITAN.NS", "ULTRACEMCO.NS", "UPL.NS", "WIPRO.NS"
        ))
    else:
        selected_stock = st.selectbox("SELECT STOCK FOR PREDICTION", (
            "AAPL", "MSFT", "AMZN", "GOOG", "TSLA", "FB", "NVDA", "JPM", "JNJ", "V", "MA", "PG", "DIS",
            "HD", "NFLX", "UNH", "PYPL", "ADBE", "CMCSA", "VZ", "KO", "PEP", "NKE", "INTC", "CSCO", "MRK",
            "BAC", "WMT", "XOM", "T", "CVX", "PFE", "ABT", "CRM", "ORCL", "ACN", "QCOM", "NVS", "ABBV", "MDT"
        ))
    
    n_years = st.slider("SELECT YEARS OF PREDICTION:", 1, 4)
    period = n_years * 365

    @st.cache_resource 
    def load_data(ticker):
        START = "2017-01-01"
        TODAY = date.today().strftime("%Y-%m-%d")
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
        fig.update_layout(title_text="Time Series Data", xaxis_rangeslider_visible=True)
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

    st.write("TO KNOW MORE ABOUT THE STOCK")
    st.write("[CLICK HERE>](https://finance.yahoo.com/)")

    # About button in the sidebar
    if st.sidebar.button("About Us"):
        st.sidebar.info("This is an application for predicting stock prices using Prophet and Streamlit.Stock predict is a website created for users to view stock analysys Created by: Muhammed Suhail C A            Contact us on: https://github.com/msuhailca7")
else:
    st.error("Login Failed!")   
