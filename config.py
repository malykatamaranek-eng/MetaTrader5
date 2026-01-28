"""
Configuration file for XAUUSD+ Scalping Bot
"""

# MT5 Connection Settings
MT5_LOGIN = 0  # Your MT5 account number
MT5_PASSWORD = ""  # Your MT5 password
MT5_SERVER = ""  # Your broker's server name

# Trading Parameters
SYMBOL = "XAUUSD+"  # Trading symbol
MAGIC_NUMBER = 234000  # Unique identifier for bot trades

# Position Management
MAX_POSITIONS = 5  # Number of simultaneous positions
ACCOUNT_RISK_PERCENT = 100  # Use 100% of available funds
POSITION_SIZE_PERCENT = 20  # Each position uses 20% (100/5)

# Profit Target
PROFIT_TARGET_PERCENT = 5  # Close at +5% profit

# Scalping Settings
PREDICTION_INTERVAL = 1  # Market prediction every 1 second
MIN_WIN_RATE = 90  # Target 90%+ win rate

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

# Stop Loss (conservative for safety)
STOP_LOSS_ATR_MULTIPLIER = 1.5  # Stop loss based on ATR

# Time Filters
TRADING_HOURS_START = 0  # 24h trading
TRADING_HOURS_END = 24

# Logging
LOG_LEVEL = "INFO"
LOG_FILE = "xauusd_bot.log"
