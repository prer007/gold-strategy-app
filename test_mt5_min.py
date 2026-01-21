import MetaTrader5 as mt5

if not mt5.initialize():
    print("Init failed:", mt5.last_error())
else:
    print("MT5 connected successfully")
    mt5.shutdown()
