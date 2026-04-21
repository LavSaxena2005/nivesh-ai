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
        try:
            res = requests.get(f"{BASE_URL}/analyze", params={"stock": stock})

            if res.status_code == 200:
                data = res.json()

                if "error" in data:
                    st.error(data["error"])
                else:
                    c1, c2, c3 = st.columns(3)
                    c1.metric("💰 Price", f"₹{round(data['price'],2)}")
                    c2.metric("📉 Signal", data["signal"])
                    c3.metric("📊 RSI", round(data["rsi"],2))

                    st.success("Analysis Loaded ✅")
                    st.info(data.get("ai", "No AI insight"))
            else:
                st.error("Backend error ❌")

        except Exception as e:
            st.error(f"Error: {e}")

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
    try:
        res = requests.get(f"{BASE_URL}/scan")

        if res.status_code == 200:
            data = res.json()

            if len(data) == 0:
                st.warning("No opportunities found")
            else:
                for s in data:
                    st.success(f"{s['stock']} → {s['signal']} | RSI {round(s['rsi'],2)}")
        else:
            st.error("Backend error")

    except Exception as e:
        st.error(f"Error: {e}")

# ---------------- CHAT ----------------
st.markdown("---")
st.markdown("## 🤖 Market Chat")

query = st.text_input("Ask something", key="chat")

if st.button("Ask AI"):
    if query:
        with st.spinner("Thinking..."):
            try:
                res = requests.get(f"{BASE_URL}/chat", params={"query": query})

                if res.status_code == 200:
                    data = res.json()
                    st.success("Response received ✅")
                    st.info(data.get("answer", "No answer"))
                else:
                    st.error("Backend not responding ❌")

            except Exception as e:
                st.error(f"Error: {e}")

# ---------------- VIDEO ----------------
st.markdown("---")
st.markdown("## 🎥 Market Update")

if st.button("Generate Update"):
    with st.spinner("Generating..."):
        try:
            res = requests.get(f"{BASE_URL}/video")

            if res.status_code == 200:
                data = res.json()
                st.success("Update Generated ✅")
                st.write(data["script"])
            else:
                st.error("Backend error")

        except Exception as e:
            st.error(f"Error: {e}")

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
        try:
            requests.post(f"{BASE_URL}/trade", params={
                "stock": stock_trade,
                "price": price,
                "qty": qty,
                "side": "BUY"
            })
            st.success("BUY executed ✅")
        except Exception as e:
            st.error(f"Error: {e}")

with col5:
    if st.button("SELL"):
        try:
            requests.post(f"{BASE_URL}/trade", params={
                "stock": stock_trade,
                "price": price,
                "qty": qty,
                "side": "SELL"
            })
            st.success("SELL executed ✅")
        except Exception as e:
            st.error(f"Error: {e}")

with col6:
    if st.button("Check PnL"):
        try:
            res = requests.get(f"{BASE_URL}/pnl")

            if res.status_code == 200:
                st.info(f"PnL: ₹{res.json()['pnl']}")
            else:
                st.error("Failed to fetch PnL")

        except Exception as e:
            st.error(f"Error: {e}")

# ---------------- PORTFOLIO ----------------
st.markdown("---")
st.markdown("## 📊 Portfolio")

if st.button("View Portfolio"):
    try:
        res = requests.get(f"{BASE_URL}/portfolio")

        if res.status_code == 200:
            data = res.json()

            if len(data["portfolio"]) == 0:
                st.warning("No trades yet")
            else:
                for k, v in data["portfolio"].items():
                    st.write(f"{k}: {v} shares")

                st.success("Portfolio loaded ✅")
                st.write(f"Total Trades: {data['total_trades']}")
        else:
            st.error("Backend error")

    except Exception as e:
        st.error(f"Error: {e}")
