import streamlit as st
import requests

BASE_URL = "https://nivesh-backend.onrender.com"

st.set_page_config(page_title="Nivesh AI", layout="wide")

# ---------------- HEADER ----------------
st.markdown("<h1 style='text-align:center;color:#00ADB5;'>📊 Nivesh AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Smart Investing Made Simple</p>", unsafe_allow_html=True)

# ---------------- STOCK ----------------
st.markdown("## 📈 Stock Analysis")

col1, col2 = st.columns([3,1])

with col1:
    stock = st.text_input("Enter Stock (e.g. RELIANCE.NS)")

with col2:
    analyze = st.button("Analyze")

if analyze and stock:
    res = requests.get(f"{BASE_URL}/analyze", params={"stock": stock}).json()

    if "error" in res:
        st.error(res["error"])
    else:
        c1, c2, c3 = st.columns(3)
        c1.metric("Price", f"₹{round(res['price'],2)}")
        c2.metric("Signal", res["signal"])
        c3.metric("RSI", round(res["rsi"],2))

        st.info(res["ai"])

# ---------------- CHART ----------------
st.markdown("## 📈 Live Chart")

if stock:
    st.components.v1.iframe(
        f"https://s.tradingview.com/widgetembed/?symbol={stock}&interval=D&theme=dark",
        height=500
    )

# ---------------- RADAR ----------------
st.markdown("## 📊 Opportunity Radar")

if st.button("Scan Market"):
    res = requests.get(f"{BASE_URL}/scan").json()

    for s in res:
        st.success(f"{s['stock']} → {s['signal']} | RSI {round(s['rsi'],2)}")

# ---------------- CHAT ----------------
st.markdown("## 🤖 Market Chat")

query = st.text_input("Ask something")

if st.button("Ask AI"):
    res = requests.get(f"{BASE_URL}/chat", params={"query": query}).json()
    st.info(res["answer"])

# ---------------- VIDEO ----------------
st.markdown("## 🎥 Market Update")

if st.button("Generate Update"):
    res = requests.get(f"{BASE_URL}/video").json()
    st.success(res["script"])

# ---------------- TRADE ----------------
st.markdown("## 💰 Trade Simulator")

colA, colB, colC = st.columns(3)

with colA:
    stock_trade = st.text_input("Stock")

with colB:
    price = st.number_input("Price", value=100.0)

with colC:
    qty = st.number_input("Qty", value=1)

colD, colE = st.columns(2)

with colD:
    if st.button("BUY"):
        requests.post(f"{BASE_URL}/trade", params={
            "stock": stock_trade,
            "price": price,
            "qty": qty,
            "side": "BUY"
        })
        st.success("BUY executed")

with colE:
    if st.button("SELL"):
        requests.post(f"{BASE_URL}/trade", params={
            "stock": stock_trade,
            "price": price,
            "qty": qty,
            "side": "SELL"
        })
        st.success("SELL executed")

if st.button("Check PnL"):
    res = requests.get(f"{BASE_URL}/pnl").json()
    st.info(f"PnL: ₹{res['pnl']}")

# ---------------- PORTFOLIO ----------------
st.markdown("## 📊 Portfolio")

if st.button("View Portfolio"):
    res = requests.get(f"{BASE_URL}/portfolio").json()

    for k, v in res["portfolio"].items():
        st.write(f"{k}: {v} shares")

    st.write(f"Total Trades: {res['total_trades']}")
