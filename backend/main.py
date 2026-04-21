from fastapi import FastAPI
import yfinance as yf
import pandas as pd
from ta.momentum import RSIIndicator
from ta.trend import MACD

app = FastAPI()

# ---------------- GLOBAL STORAGE ----------------
trades = []

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
    return float(rsi_series.iloc[-1]) if len(rsi_series) > 0 else 50.0

def detect_signal(df):
    latest = float(df['Close'].iloc[-1])
    prev = float(df['Close'].iloc[-2])
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
    price = float(df['Close'].iloc[-1])

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
            print(e)
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
        "script": "📊 Market Update:\nReliance weak, IT stable, market mixed."
    }

# ---------------- TRADE ----------------
@app.post("/trade")
def trade(stock: str, price: float, qty: int, side: str):
    trade_data = {
        "stock": stock,
        "price": price,
        "qty": qty,
        "side": side
    }
    trades.append(trade_data)

    return {
        "message": "Trade executed",
        "total_trades": len(trades)
    }

# ---------------- PNL ----------------
@app.get("/pnl")
def pnl():
    total = 0

    for t in trades:
        if t["side"] == "BUY":
            total -= t["price"] * t["qty"]
        else:
            total += t["price"] * t["qty"]

    return {"pnl": total}

# ---------------- PORTFOLIO ----------------
@app.get("/portfolio")
def portfolio():
    data = {}

    for t in trades:
        qty = t["qty"] if t["side"] == "BUY" else -t["qty"]

        if t["stock"] not in data:
            data[t["stock"]] = 0

        data[t["stock"]] += qty

    return {
        "portfolio": data,
        "total_trades": len(trades)
    }
