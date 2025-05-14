import asyncio
import json
import websockets
import time
from datetime import datetime, timezone
import numpy as np
import tkinter as tk
from tkinter import ttk
from sklearn.linear_model import LinearRegression, LogisticRegression
import matplotlib.pyplot as plt
from threading import Thread

# WebSocket and model globals
ORDERBOOK_URL = "wss://ws.gomarket-cpp.goquant.io/ws/l2-orderbook/okx/BTC-USDT-SWAP"
latencies = []
model_slippage = LinearRegression()
model_maker_taker = LogisticRegression()

# Dummy training for regression models
X = np.array([[1], [2], [3], [4], [5]])
y_slippage = np.array([0.1, 0.15, 0.25, 0.35, 0.45])  # Dummy slippage values
y_maker_taker = np.array([1, 1, 0, 0, 0])             # Dummy classification
model_slippage.fit(X, y_slippage)
model_maker_taker.fit(X, y_maker_taker)

# UI setup
root = tk.Tk()
root.title("GoQuant Trade Simulator")
root.geometry("700x400")

# --- Left Panel: Inputs ---
frame_left = tk.Frame(root)
frame_left.pack(side=tk.LEFT, padx=10, pady=10)

tk.Label(frame_left, text="Exchange:").pack()
exchange_entry = ttk.Combobox(frame_left, values=["OKX"])
exchange_entry.set("OKX")
exchange_entry.pack()

tk.Label(frame_left, text="Asset:").pack()
asset_entry = ttk.Combobox(frame_left, values=["BTC-USDT-SWAP"])
asset_entry.set("BTC-USDT-SWAP")
asset_entry.pack()

tk.Label(frame_left, text="Order Type:").pack()
order_entry = ttk.Combobox(frame_left, values=["market"])
order_entry.set("market")
order_entry.pack()

tk.Label(frame_left, text="Quantity (USD):").pack()
quantity_entry = tk.Entry(frame_left)
quantity_entry.insert(0, "100")
quantity_entry.pack()

tk.Label(frame_left, text="Volatility:").pack()
volatility_entry = tk.Entry(frame_left)
volatility_entry.insert(0, "0.02")
volatility_entry.pack()

tk.Label(frame_left, text="Fee Tier (%):").pack()
fee_entry = tk.Entry(frame_left)
fee_entry.insert(0, "0.1")
fee_entry.pack()

# --- Right Panel: Outputs ---
frame_right = tk.Frame(root)
frame_right.pack(side=tk.RIGHT, padx=10, pady=10)

output_labels = {}
for label in [
    "Expected Slippage", "Expected Fees", "Market Impact",
    "Net Cost", "Maker/Taker", "Internal Latency"
]:
    tk.Label(frame_right, text=label).pack()
    output_labels[label] = tk.Label(frame_right, text="--")
    output_labels[label].pack()

# --- Utility Functions ---
def update_outputs(slippage, fees, impact, net_cost, maker_taker, latency):
    output_labels["Expected Slippage"].config(text=f"{slippage:.4f}")
    output_labels["Expected Fees"].config(text=f"{fees:.4f}")
    output_labels["Market Impact"].config(text=f"{impact:.4f}")
    output_labels["Net Cost"].config(text=f"{net_cost:.4f}")
    output_labels["Maker/Taker"].config(text="Maker" if maker_taker == 1 else "Taker")
    output_labels["Internal Latency"].config(text=f"{latency:.4f} s")

def estimate_fees(qty, fee_percent):
    return (qty * fee_percent) / 100

def estimate_market_impact(qty, volatility):
    return 0.5 * volatility * np.sqrt(qty / 100)

# --- WebSocket Logic ---
async def stream_orderbook():
    async with websockets.connect(ORDERBOOK_URL) as ws:
        while True:
            try:
                start = time.time()
                msg = await ws.recv()
                end = time.time()
                latency = end - start
                latencies.append(latency)

                data = json.loads(msg)
                timestamp = datetime.strptime(data["timestamp"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
                current_time = datetime.now(timezone.utc)
                tick_latency = (current_time - timestamp).total_seconds()

                qty = float(quantity_entry.get())
                volatility = float(volatility_entry.get())
                fee_pct = float(fee_entry.get())

                # Models
                slippage = model_slippage.predict([[qty]])[0]
                fees = estimate_fees(qty, fee_pct)
                impact = estimate_market_impact(qty, volatility)
                net_cost = slippage + fees + impact
                maker_taker = model_maker_taker.predict([[qty]])[0]

                update_outputs(slippage, fees, impact, net_cost, maker_taker, tick_latency)

            except Exception as e:
                print("WebSocket Error:", e)
                await asyncio.sleep(1)

# --- Thread Wrapper ---
def run_async_loop():
    asyncio.run(stream_orderbook())

def run_ui():
    Thread(target=run_async_loop, daemon=True).start()
    root.mainloop()

run_ui()
