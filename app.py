import streamlit as st
import yfinance as yf
import pandas as pd
import ta
import matplotlib.pyplot as plt

st.set_page_config(page_title="AI S&P 500 Market Dashboard", layout="wide")
st.markdown("""
<style>
/* Main app background */
.stApp {
    background: linear-gradient(180deg, #FFF0F6 0%, #FFE4EE 100%);
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #FFD6E8;
}

/* Metric cards */
[data-testid="stMetric"] {
    background-color: white;
    padding: 18px;
    border-radius: 18px;
    box-shadow: 0 6px 15px rgba(255, 105, 180, 0.25);
    text-align: center;
}

/* Buttons */
.stButton > button {
    background-color: #FF69B4;
    color: white;
    border-radius: 20px;
    padding: 0.5rem 1.5rem;
    border: none;
    font-weight: bold;
}

/* Select boxes */
div[data-baseweb="select"] > div {
    border-radius: 15px;
    background-color: white;
}

/* Charts container */
.stPlotlyChart, .stLineChart, .stPyplot {
    background-color: white;
    border-radius: 20px;
    padding: 10px;
}
</style>
""", unsafe_allow_html=True)
st.title("AI Market Dashboard 🐹")
st.subheader("Technical Signals for AI Stocks")
st.markdown("---")

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.title("AI Market Controls")

tickers = {
    "NVIDIA": "NVDA",
    "Microsoft": "MSFT",
    "Apple": "AAPL",
    "Google": "GOOGL",
    "Meta": "META",
    "Amazon": "AMZN"
}

selected_stock = st.sidebar.selectbox("Select AI Stock", list(tickers.keys()))
ticker = tickers[selected_stock]

start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2023-01-01"))
end_date = st.sidebar.date_input("End Date", pd.to_datetime("today"))

# -----------------------------
# Data Download
# -----------------------------
data = yf.download(ticker, start=start_date, end=end_date)

st.title(f"{selected_stock} ({ticker}) — AI Market Signals")

if data.empty:
    st.warning("No data available.")
    st.stop()

# -----------------------------
# Technical Indicators
# -----------------------------
close = data["Close"].squeeze()

data["SMA_50"] = ta.trend.sma_indicator(close, window=50)
data["SMA_200"] = ta.trend.sma_indicator(close, window=200)
data["RSI"] = ta.momentum.rsi(close, window=14)

macd = ta.trend.MACD(close)
data["MACD"] = macd.macd()
data["MACD_Signal"] = macd.macd_signal()

# -----------------------------
# Price Chart
# -----------------------------
st.subheader("Price & Moving Averages")

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(data["Close"], label="Close Price")
ax.plot(data["SMA_50"], label="SMA 50")
ax.plot(data["SMA_200"], label="SMA 200")
ax.legend()
ax.grid()

st.pyplot(fig)

# -----------------------------
# RSI
# -----------------------------
st.subheader("Relative Strength Index (RSI)")

fig, ax = plt.subplots(figsize=(10, 2))
ax.plot(data["RSI"], color="purple")
ax.axhline(70, linestyle="--")
ax.axhline(30, linestyle="--")
ax.set_ylim(0, 100)
ax.grid()

st.pyplot(fig)

# -----------------------------
# MACD
# -----------------------------
st.subheader("MACD Indicator")

fig, ax = plt.subplots(figsize=(10, 3))
ax.plot(data["MACD"], label="MACD")
ax.plot(data["MACD_Signal"], label="Signal")
ax.legend()
ax.grid()

st.pyplot(fig)

# -----------------------------
# Signal Interpretation
# -----------------------------
latest_rsi = data["RSI"].iloc[-1]

st.subheader("AI Signal Summary")

if latest_rsi > 70:
    st.error("🔴 Overbought (Possible Pullback)")
elif latest_rsi < 30:
    st.success("🟢 Oversold (Potential Buy Zone)")
else:
    st.info("🟡 Neutral Momentum")
