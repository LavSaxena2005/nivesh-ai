from fastapi import FastAPI
import yfinance as yf
import pandas as pd
from ta.momentum import RSIIndicator
from ta.trend import MACD

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Nivesh AI running 🚀"}

# ---------------- DATA ----------------
def get_data(stock):
    return yf.download(stock, period="3mo", interval="1d")

def add_indicators(df):
    close = pd.Series(df['Close'].values.flatten()).astype(float)
    df['rsi'] = RSIIndicator(close).rsi()
    df['macd'] = MACD(close).macd()
    return df

def get_safe_rsi(df):
    rsi_series = df['rsi'].dropna()
    return float(rsi_series.iloc[-1].item()) if len(rsi_series) > 0 else 50.0

def detect_signal(df):
    latest = float(df['Close'].iloc[-1].item())
    prev = float(df['Close'].iloc[-2].item())
    change = (latest - prev) / prev

    if change > 0.03:
        return "Breakout", round(change * 100, 2)
    elif change < -0.03:
        return "Breakdown", round(change * 100, 2)
    return "Sideways", round(change * 100, 2)

# ---------------- ANALYZE ----------------
@app.get("/analyze")
def analyze(stock: str):
    df = get_data(stock)

    if df.empty or len(df) < 3:
        return {"error": "Not enough data"}

    df = add_indicators(df)

    signal, change = detect_signal(df)
    rsi = get_safe_rsi(df)
    price = float(df['Close'].iloc[-1].item())

    return {
        "stock": stock,
        "price": price,
        "signal": signal,
        "price_change_%": change,
        "rsi": rsi,
        "ai": f"{stock} is {signal} with RSI {round(rsi,2)}",
        "recommendation": "BUY" if signal == "Breakout" else "HOLD"
    }

# ---------------- SCAN ----------------
@app.get("/scan")
def scan():
    stocks = ["RELIANCE.NS", "TCS.NS", "INFY.NS"]
    results = []

    for s in stocks:
        try:
            df = get_data(s)

            if df is None or df.empty or len(df) < 3:
                continue

            df = add_indicators(df)
            signal, _ = detect_signal(df)
            rsi = get_safe_rsi(df)

            results.append({
                "stock": s,
                "signal": signal,
                "rsi": rsi
            })

        except Exception as e:
            print(f"Error in {s}: {e}")
            continue

    return results
# ---------------- CHAT ----------------
@app.get("/chat")
def chat(query: str):
    return {"answer": "AI suggests focusing on breakout stocks with strong RSI."}

# ---------------- VIDEO ----------------
@app.get("/video")
def video():
    return {
        "script": "📊 Market Update:\n\nReliance under pressure, IT stable, market mixed."
    }