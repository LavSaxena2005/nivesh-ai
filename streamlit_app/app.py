import streamlit as st
import requests

BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Nivesh AI", layout="wide")
st.title("📊 Nivesh AI (API Powered)")

# ---------------- INPUT ----------------
stock = st.text_input("Enter Stock (e.g. RELIANCE.NS)")

# ---------------- ANALYZE ----------------
if st.button("Analyze Stock"):
    if stock:
        try:
            res = requests.get(f"{BASE_URL}/analyze", params={"stock": stock})

            if res.status_code == 200:
                data = res.json()

                if "error" in data:
                    st.error(data["error"])
                else:
                    col1, col2, col3 = st.columns(3)
                    col1.metric("💰 Price", f"₹{round(data['price'],2)}")
                    col2.metric("📉 Signal", data["signal"])
                    col3.metric("📊 RSI", round(data["rsi"],2))

                    st.info(data.get("ai", "AI insight not available"))

                    if data["recommendation"] == "BUY":
                        st.success("🟢 BUY")
                    elif data["recommendation"] == "SELL":
                        st.error("🔴 SELL")
                    else:
                        st.warning("🟡 HOLD")

            else:
                st.error("Backend error")

        except Exception as e:
            st.error(f"Error: {e}")

# ---------------- SCAN ----------------
st.subheader("📊 Opportunity Radar")

if st.button("Scan Market"):
    try:
        res = requests.get(f"{BASE_URL}/scan")

        if res.status_code == 200:
            data = res.json()

            if len(data) == 0:
                st.warning("No opportunities found")
            else:
                for s in data:
                    st.success(
                        f"{s['stock']} → {s['signal']} | RSI: {round(s['rsi'],2)}"
                    )
        else:
            st.error("Backend error")

    except Exception as e:
        st.error(f"Error: {e}")

# ---------------- CHAT ----------------
st.subheader("🤖 Market ChatGPT")

query = st.text_input("Ask something")

if st.button("Ask AI"):
    if query:
        try:
            res = requests.get(f"{BASE_URL}/chat", params={"query": query})

            if res.status_code == 200:
                data = res.json()
                st.info(data["answer"])
            else:
                st.error("Backend error")

        except Exception as e:
            st.error(f"Error: {e}")

# ---------------- VIDEO ----------------
st.subheader("🎥 AI Market Video")

if st.button("Generate Video Script"):
    try:
        res = requests.get(f"{BASE_URL}/video")

        if res.status_code == 200:
            data = res.json()
            st.success("🎬 Market Update")
            st.write(data["script"])
        else:
            st.error("Backend error")

    except Exception as e:
        st.error(f"Error: {e}")