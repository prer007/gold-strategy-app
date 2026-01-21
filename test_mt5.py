import MetaTrader5 as mt5

terminal_path = r"C:\Program Files\XM Global MT5\terminal64.exe"

# Initialize MT5 (this will START MT5 automatically)
if not mt5.initialize(path=terminal_path):
    print("Init failed:", mt5.last_error())
    quit()

print("MT5 connected successfully")

# Check account info
account = mt5.account_info()
print("Account:", account.login)
print("Server:", account.server)

mt5.shutdown()
