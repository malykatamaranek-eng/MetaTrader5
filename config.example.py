"""
Example configuration for demo/testing
Copy this to config.py and modify with your settings
"""

# ============================================
# EXAMPLE CONFIGURATION
# Copy values to config.py and customize
# ============================================

# MT5 Connection Settings - DEMO ACCOUNT
MT5_LOGIN = 0  # Your demo account number (e.g., 12345678)
MT5_PASSWORD = ""  # Your demo account password
MT5_SERVER = ""  # Demo server (e.g., "ICMarkets-Demo", "XMGlobal-Demo")

# For testing without login (uses currently logged-in account):
# Leave MT5_LOGIN = 0, MT5_PASSWORD = "", MT5_SERVER = ""

# Trading Parameters
SYMBOL = "XAUUSD+"  # May vary by broker: "XAUUSD", "GOLD", "XAUUSD+", "XAUUSD.a"

# Start with smaller settings for testing:
# MAX_POSITIONS = 2  # Start with 2 positions for testing
# POSITION_SIZE_PERCENT = 10  # Use only 10% per position for safety

# Risk Management
# ACCOUNT_RISK_PERCENT = 20  # For testing, use only 20% of account
