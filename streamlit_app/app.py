import streamlit as st
import requests

BASE_URL = "https://nivesh-backend.onrender.com"

st.set_page_config(page_title="Nivesh AI", layout="wide")

# ---------------- HEADER ----------------
st.title("📊 Nivesh AI")
st.caption("Smart Investing Made Simple")

# ---------------- STOCK ANALYSIS ----------------
st.markdown("## 📈 Stock Analysis")

stock = st.text_input("Enter Stock (e.g. RELIANCE.NS)", key="stock_main")

if st.button("Analyze Stock"):
    if stock:
        res = requests.get(f"{BASE_URL}/analyze", params={"stock": stock}).json()

        if "error" in res:
            st.error(res["error"])
        else:
            c1, c2, c3 = st.columns(3)
            c1.metric("Price", f"₹{round(res['price'],2)}")
            c2.metric("Signal", res["signal"])
            c3.metric("RSI", round(res["rsi"],2))

            st.info(res.get("ai", "No AI insight"))

# ---------------- CHART ----------------
if stock:
    st.markdown("## 📈 Live Chart")
    st.components.v1.iframe(
        f"https://s.tradingview.com/widgetembed/?symbol={stock}&theme=dark",
        height=400
    )

# ---------------- RADAR ----------------
st.markdown("---")
st.markdown("## 📊 Opportunity Radar")

if st.button("Scan Market"):
    res = requests.get(f"{BASE_URL}/scan").json()

    if len(res) == 0:
        st.warning("No opportunities found")
    else:
        for s in res:
            st.success(f"{s['stock']} → {s['signal']} | RSI {round(s['rsi'],2)}")

# ---------------- CHAT ----------------
st.markdown("---")
st.markdown("## 🤖 Market Chat")

query = st.text_input("Ask something", key="chat")

if st.button("Ask AI"):
    if query:
        res = requests.get(f"{BASE_URL}/chat", params={"query": query}).json()
        st.info(res["answer"])

# ---------------- VIDEO ----------------
st.markdown("---")
st.markdown("## 🎥 Market Update")

if st.button("Generate Update"):
    res = requests.get(f"{BASE_URL}/video").json()
    st.success(res["script"])

# ---------------- TRADE ----------------
st.markdown("---")
st.markdown("## 💰 Trade Simulator")

col1, col2, col3 = st.columns(3)

with col1:
    stock_trade = st.text_input("Stock", key="trade_stock")

with col2:
    price = st.number_input("Price", value=100.0)

with col3:
    qty = st.number_input("Qty", value=1)

col4, col5, col6 = st.columns(3)

with col4:
    if st.button("BUY"):
        if stock_trade:
            requests.post(f"{BASE_URL}/trade", params={
                "stock": stock_trade,
                "price": price,
                "qty": qty,
                "side": "BUY"
            })
            st.success("BUY executed")

with col5:
    if st.button("SELL"):
        if stock_trade:
            requests.post(f"{BASE_URL}/trade", params={
                "stock": stock_trade,
                "price": price,
                "qty": qty,
                "side": "SELL"
            })
            st.success("SELL executed")

with col6:
    if st.button("Check PnL"):
        res = requests.get(f"{BASE_URL}/pnl").json()
        st.info(f"PnL: ₹{res['pnl']}")

# ---------------- PORTFOLIO ----------------
st.markdown("---")
st.markdown("## 📊 Portfolio")

if st.button("View Portfolio"):
    res = requests.get(f"{BASE_URL}/portfolio").json()

    if len(res["portfolio"]) == 0:
        st.warning("No trades yet")
    else:
        for k, v in res["portfolio"].items():
            st.write(f"{k}: {v} shares")

        st.write(f"Total Trades: {res['total_trades']}")
