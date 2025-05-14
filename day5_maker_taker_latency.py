import asyncio
import websockets
import time
import matplotlib.pyplot as plt
from datetime import datetime
from collections import deque
import sqlite3

# WebSocket URL
url = "wss://ws.gomarket-cpp.goquant.io/ws/l2-orderbook/okx/BTC-USDT-SWAP"

# Store latencies (limited to MAX_LATENCY_POINTS)
latencies = deque(maxlen=100)  # Limit to last 100 latencies
MAX_LATENCY_COUNT = 1000  # Stop after receiving 1000 data points

# Plotting variables
plt.ion()  # Interactive mode on
fig, ax = plt.subplots()
line, = ax.plot([], [], 'r-')
ax.set_xlim(0, 100)
ax.set_ylim(0, 10)
ax.set_xlabel('Time')
ax.set_ylabel('Latency (seconds)')
ax.set_title('Latency vs Time')

# Function to calculate moving average
def calculate_moving_average(latencies, window_size=50):
    if len(latencies) < window_size:
        return sum(latencies) / len(latencies)
    return sum(latencies[-window_size:]) / window_size

# Function to plot latency
def plot_latency():
    ax.clear()
    ax.plot(latencies)
    ax.set_xlim(max(0, len(latencies) - 100), len(latencies))  # Show last 100 points
    ax.set_ylim(0, max(latencies) if latencies else 10)
    ax.set_xlabel('Time')
    ax.set_ylabel('Latency (seconds)')
    ax.set_title('Latency vs Time')
    plt.draw()
    plt.pause(0.1)  # Pause to update the plot

# SQLite Setup: Create DB and table
def create_db():
    conn = sqlite3.connect('latency_data.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS latencies (timestamp TEXT, latency REAL)''')
    conn.commit()
    conn.close()

# Function to save latency to the database
def save_to_db(latency):
    conn = sqlite3.connect('latency_data.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO latencies (timestamp, latency) VALUES (?, ?)", (str(datetime.utcnow()), latency))
    conn.commit()
    conn.close()

# Function to process WebSocket data
async def process_data():
    async with websockets.connect(url) as websocket:
        count = 0
        while True:
            try:
                message = await websocket.recv()
                data = eval(message)  # Convert string to dictionary
                timestamp_str = data['timestamp']  # Extract timestamp
                timestamp_obj = datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%SZ")
                current_time = datetime.utcnow()

                # Calculate latency
                latency = (current_time - timestamp_obj).total_seconds()
                latencies.append(latency)

                # Calculate and print moving average latency
                moving_average_latency = calculate_moving_average(latencies)
                print(f"Latency: {latency:.6f} seconds")
                print(f"Moving Average Latency (last 50 points): {moving_average_latency:.6f} seconds")

                # Check if latency exceeds threshold
                HIGH_LATENCY_THRESHOLD = 1.0  # 1 second
                if latency > HIGH_LATENCY_THRESHOLD:
                    print(f"Warning: High latency detected! Latency = {latency:.6f} seconds")

                # Save latency to database
                save_to_db(latency)

                # Save latency to file
                with open("latency_log.txt", "a") as f:
                    f.write(f"{time.time()},{latency}\n")

                # Plot latency
                plot_latency()

                count += 1
                if count >= MAX_LATENCY_COUNT:
                    print("Reached max latency count, closing connection.")
                    break

            except websockets.ConnectionClosed:
                print("Connection closed. Reconnecting...")
                await asyncio.sleep(1)  # Wait before reconnecting

# Main function to run the WebSocket client
async def main():
    create_db()  # Create the database and table if not already present
    await process_data()

# Run the program
if __name__ == "__main__":
    asyncio.run(main())
