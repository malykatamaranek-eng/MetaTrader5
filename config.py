"""
Configuration file for XAUUSD+ Scalping Bot

⚠️ IMPORTANT RISK WARNING:
This bot uses aggressive settings by default (100% fund utilization, no stop losses).
Start with demo account and reduce risk settings for live trading.
"""

# MT5 Connection Settings
# Note: Leave empty (0, "", "") to use currently logged-in MT5 account
MT5_LOGIN = 0  # Your MT5 account number
MT5_PASSWORD = ""  # Your MT5 password
MT5_SERVER = ""  # Your broker's server name

# Trading Parameters
SYMBOL = "XAUUSD+"  # Trading symbol
MAGIC_NUMBER = 234000  # Unique identifier for bot trades

# Position Management
MAX_POSITIONS = 5  # Number of simultaneous positions
POSITION_SIZE_PERCENT = 20  # Each position uses 20% (100/5)
# ⚠️ Risk: 5 positions × 20% = 100% of account. Consider reducing for safety.

# Profit Target
PROFIT_TARGET_PERCENT = 5  # Close at +5% profit per position

# Scalping Settings
PREDICTION_INTERVAL = 1  # Market evaluation every 1 second
# Note: Actual predictions use M1 (1-minute) bars which update every 60 seconds

# Technical Analysis Parameters
RSI_PERIOD = 14
RSI_OVERSOLD = 30
RSI_OVERBOUGHT = 70

EMA_FAST = 9
EMA_SLOW = 21

MACD_FAST = 12
MACD_SLOW = 26
MACD_SIGNAL = 9

ATR_PERIOD = 14

# Volume Analysis
VOLUME_MA_PERIOD = 20

# Risk Management
# ⚠️ Stop Loss is disabled by default (sl=0 in position_manager.py)
# To enable stop losses, modify open_position() in position_manager.py
# Recommended: Enable ATR-based stop losses for live trading

# Logging
LOG_LEVEL = "INFO"
LOG_FILE = "xauusd_bot.log"
