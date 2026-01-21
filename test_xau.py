import MetaTrader5 as mt5

# Connect to MT5
mt5.initialize()

# Get all symbols that contain XAU
symbols = [s.name for s in mt5.symbols_get() if "XAU" in s.name]

print("Gold symbols found:")
print(symbols)

mt5.shutdown()
