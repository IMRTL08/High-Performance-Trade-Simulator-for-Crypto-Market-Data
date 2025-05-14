# day1_ws.py
import asyncio
import websockets
import json

async def connect_and_listen():
    url = "wss://ws.gomarket-cpp.goquant.io/ws/l2-orderbook/okx/BTC-USDT-SWAP"
    
    async with websockets.connect(url) as ws:
        print("✅ Connected to WebSocket...\n")
        
        while True:
            try:
                message = await ws.recv()
                data = json.loads(message)
                
                # Show best bid and ask prices
                best_bid = data['bids'][0]
                best_ask = data['asks'][0]
                print(f"Best Bid: {best_bid[0]} | Best Ask: {best_ask[0]}")
            
            except Exception as e:
                print(f"❌ Error: {e}")
                break

# Start the async listener
asyncio.run(connect_and_listen())
