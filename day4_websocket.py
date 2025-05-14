import asyncio
import websockets
import json

# Function to calculate slippage
def calculate_slippage(asks, bids):
    best_bid = float(bids[0][0])  # Highest price in bids
    best_ask = float(asks[0][0])  # Lowest price in asks
    slippage = best_ask - best_bid
    return slippage

# Function to calculate market impact using a simple model
def calculate_market_impact(quantity, asks, bids):
    best_bid = float(bids[0][0])
    best_ask = float(asks[0][0])
    liquidity_factor = 0.0001  # Price change per $1,000 trade
    market_impact = liquidity_factor * quantity
    return market_impact

# Function to process order book data and calculate slippage and market impact
def process_orderbook(data, quantity):
    asks = data.get("asks", [])
    bids = data.get("bids", [])

    # Simulate slippage
    slippage = calculate_slippage(asks, bids)
    print(f"\nSlippage: {slippage:.4f}")

    # Simulate market impact
    market_impact = calculate_market_impact(quantity, asks, bids)
    print(f"Market Impact: {market_impact:.4f}")

    # Best bid and ask prices for reference
    best_bid = float(bids[0][0])
    best_ask = float(asks[0][0])

    print(f"\nBest Bid: {best_bid}, Best Ask: {best_ask}")

# WebSocket connection function to receive data
async def connect_to_websocket():
    url = "wss://ws.gomarket-cpp.goquant.io/ws/l2-orderbook/okx/BTC-USDT-SWAP"
    quantity = 100  # Example trade size in USD

    async with websockets.connect(url) as websocket:
        while True:
            message = await websocket.recv()  # Receive data
            data = json.loads(message)  # Parse the JSON data
            print("Received Data:", data)
            process_orderbook(data, quantity)  # Process the orderbook

# Run the WebSocket connection
asyncio.get_event_loop().run_until_complete(connect_to_websocket())
