# GoQuant Real-Time Trade Simulator

This project is a real-time trading simulator built as part of the GoQuant assignment. It connects to the OKX exchange's WebSocket L2 order book and calculates key metrics like slippage, fees, market impact, and latency for market orders in a live environment.

---

## Project Overview

The main goal was to simulate market order execution using real-time market data and estimate transaction costs including:
- Slippage
- Exchange fees
- Market impact
- Latency
- Maker/Taker execution probability

---

## Technologies Used

- Python 3.12
- Tkinter (GUI)
- WebSockets (`websockets`)
- Matplotlib (live latency plotting)
- Scikit-learn (for regression models)
- NumPy

---

## Features

### ✅ Input Panel (GUI)
- **Exchange**: OKX
- **Asset**: BTC-USDT-SWAP
- **Order Type**: Market
- **Quantity**: User-defined (~$100 simulated)
- **Volatility**: Manual input
- **Fee Tier**: Selectable

### ✅ Output Panel
- **Estimated Slippage** (Linear Regression)
- **Estimated Fees** (Based on rulebook)
- **Estimated Market Impact** (Almgren-Chriss Model)
- **Net Cost** (Slippage + Fees + Impact)
- **Maker/Taker Prediction** (Logistic Regression)
- **Live Latency Graph**

---

## Data Source

- **WebSocket Endpoint**:  
  `wss://ws.gomarket-cpp.goquant.io/ws/l2-orderbook/okx/BTC-USDT-SWAP`
  
- Each tick contains full depth L2 order book data with timestamps.

---

## Models and Logic

- **Slippage**: Predicted using linear regression based on recent order book depth and quantity.
- **Fees**: Calculated using fixed fee tiers (e.g., 0.1%, 0.08%).
- **Market Impact**: Estimated using the Almgren-Chriss model.
- **Maker/Taker**: Logistic regression based on top-of-book pressure and quantity.
- **Latency**: Computed per tick by comparing the order book timestamp to local UTC time.

---

## How to Run

1. **Install requirements**
   ```bash
   pip install websockets matplotlib scikit-learn numpy
