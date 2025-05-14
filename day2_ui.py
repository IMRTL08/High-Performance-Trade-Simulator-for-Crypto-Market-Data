import tkinter as tk

def submit():
    exchange = exchange_var.get()
    asset = asset_var.get()
    quantity = quantity_var.get()

    print("User Input:")
    print(f"Exchange: {exchange}")
    print(f"Asset: {asset}")
    print(f"Quantity (USD): {quantity}")

# Create window
root = tk.Tk()
root.title("GoQuant Trade Simulator")

# Input: Exchange
tk.Label(root, text="Exchange").grid(row=0, column=0, padx=10, pady=5)
exchange_var = tk.StringVar(value="OKX")
tk.Entry(root, textvariable=exchange_var).grid(row=0, column=1, padx=10, pady=5)

# Input: Asset
tk.Label(root, text="Spot Asset").grid(row=1, column=0, padx=10, pady=5)
asset_var = tk.StringVar(value="BTC-USDT")
tk.Entry(root, textvariable=asset_var).grid(row=1, column=1, padx=10, pady=5)

# Input: Quantity
tk.Label(root, text="Quantity ($)").grid(row=2, column=0, padx=10, pady=5)
quantity_var = tk.StringVar(value="100")
tk.Entry(root, textvariable=quantity_var).grid(row=2, column=1, padx=10, pady=5)

# Submit Button
tk.Button(root, text="Submit", command=submit).grid(row=3, columnspan=2, pady=10)

# Start the UI loop
root.mainloop()
