import tkinter as tk
from tkinter import ttk

def on_submit():
    asset = asset_entry.get()
    quantity = quantity_entry.get()
    fee_tier = fee_tier_var.get()

    # Simulated output (replace with actual calculations later)
    slippage = "0.1%"  # Example slippage
    fees = "0.2%"  # Example fees
    market_impact = "0.3%"  # Example market impact
    net_cost = "0.6%"  # Sum of slippage + fees + market impact

    # Update output labels
    slippage_label.config(text=f"Expected Slippage: {slippage}")
    fees_label.config(text=f"Expected Fees: {fees}")
    market_impact_label.config(text=f"Market Impact: {market_impact}")
    net_cost_label.config(text=f"Net Cost: {net_cost}")

# Create main window
window = tk.Tk()
window.title("GoQuant Trade Simulator")
window.geometry("600x300")

# --- Left Panel: Input Fields ---
left_frame = tk.Frame(window, padx=10, pady=10)
left_frame.pack(side="left", fill="both", expand=True)

# Exchange
tk.Label(left_frame, text="Exchange:").pack(anchor="w")
tk.Label(left_frame, text="OKX").pack(anchor="w")  # fixed value

# Asset
tk.Label(left_frame, text="Spot Asset:").pack(anchor="w")
asset_entry = tk.Entry(left_frame)
asset_entry.insert(0, "BTC-USDT")
asset_entry.pack(anchor="w")

# Order Type
tk.Label(left_frame, text="Order Type:").pack(anchor="w")
tk.Label(left_frame, text="Market").pack(anchor="w")  # fixed value

# Quantity
tk.Label(left_frame, text="Quantity (USD):").pack(anchor="w")
quantity_entry = tk.Entry(left_frame)
quantity_entry.insert(0, "100")
quantity_entry.pack(anchor="w")

# Fee Tier
tk.Label(left_frame, text="Fee Tier:").pack(anchor="w")
fee_tier_var = tk.StringVar(value="Tier 1")
fee_tier_menu = ttk.Combobox(left_frame, textvariable=fee_tier_var)
fee_tier_menu['values'] = ("Tier 1", "Tier 2", "Tier 3")
fee_tier_menu.pack(anchor="w")

# Submit Button
submit_btn = tk.Button(left_frame, text="Submit", command=on_submit)
submit_btn.pack(pady=10)

# --- Right Panel: Output Display ---
right_frame = tk.Frame(window, padx=10, pady=10)
right_frame.pack(side="right", fill="both", expand=True)

# Labels to display results
slippage_label = tk.Label(right_frame, text="Expected Slippage: N/A")
slippage_label.pack(anchor="w")

fees_label = tk.Label(right_frame, text="Expected Fees: N/A")
fees_label.pack(anchor="w")

market_impact_label = tk.Label(right_frame, text="Market Impact: N/A")
market_impact_label.pack(anchor="w")

net_cost_label = tk.Label(right_frame, text="Net Cost: N/A")
net_cost_label.pack(anchor="w")

# Run the app
window.mainloop()
