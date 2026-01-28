# Advanced Usage and Customization Guide

## 🎨 Customizing the Bot

### Adjusting Prediction Accuracy

The bot targets 90%+ accuracy through multiple layers:

#### 1. Machine Learning Parameters
In `predictor.py`, modify the Random Forest:
```python
self.model = RandomForestClassifier(
    n_estimators=200,  # More trees = better but slower
    max_depth=15,      # Deeper trees = more complex patterns
    random_state=42,
    min_samples_split=10  # Higher = more conservative
)
```

#### 2. Confidence Threshold
In `predictor.py`, adjust minimum confidence:
```python
min_confidence = 0.80  # Higher = fewer but better trades
```

#### 3. Technical Indicator Weights
In `predictor.py`, the signal system weighs indicators differently:
- RSI signals: Weight 2 (most important)
- EMA/MACD: Weight 1 each
- Volume: Weight 1

Adjust by changing the numbers:
```python
if latest['rsi'] < config.RSI_OVERSOLD:
    bullish_signals += 3  # Increase weight
```

### Position Sizing Strategies

#### Conservative (Lower Risk)
```python
# config.py
MAX_POSITIONS = 3
POSITION_SIZE_PERCENT = 10  # 30% total exposure
PROFIT_TARGET_PERCENT = 3
```

#### Moderate (Balanced)
```python
# config.py
MAX_POSITIONS = 4
POSITION_SIZE_PERCENT = 15  # 60% total exposure
PROFIT_TARGET_PERCENT = 4
```

#### Aggressive (High Risk/Reward)
```python
# config.py
MAX_POSITIONS = 5
POSITION_SIZE_PERCENT = 20  # 100% total exposure
PROFIT_TARGET_PERCENT = 5
```

#### Dynamic Sizing (Advanced)
Modify `position_manager.py`:
```python
def calculate_lot_size(self, symbol, direction, confidence=1.0):
    # Base calculation
    equity = account_info.equity
    
    # Adjust by confidence
    position_value = equity * (config.POSITION_SIZE_PERCENT / 100) * confidence
    
    # Rest of calculation...
```

### Time-Based Filters

Add trading hour restrictions in `bot.py`:

```python
def should_trade_now(self):
    """
    Check if current time is within trading hours
    """
    current_hour = datetime.now().hour
    
    # Trade only during high liquidity (London + NY overlap)
    if 13 <= current_hour <= 20:  # 13:00-20:00 UTC
        return True
    
    return False
```

Then in `execute_trading_cycle`:
```python
def execute_trading_cycle(self):
    if not self.should_trade_now():
        return
    
    # Rest of logic...
```

### Technical Indicator Optimization

#### RSI Settings
```python
# config.py
RSI_PERIOD = 14        # Standard: 14, Sensitive: 7, Slow: 21
RSI_OVERSOLD = 25      # More trades: 35, Fewer: 20
RSI_OVERBOUGHT = 75    # More trades: 65, Fewer: 80
```

#### EMA Settings
```python
# config.py
EMA_FAST = 9   # Faster: 5, Slower: 12
EMA_SLOW = 21  # Faster: 13, Slower: 26
```

#### MACD Settings
```python
# config.py
MACD_FAST = 12   # Standard values
MACD_SLOW = 26
MACD_SIGNAL = 9
```

### Adding Stop Loss

Enable stop loss in `position_manager.py`:

```python
def open_position(self, symbol, direction, stop_loss_pips=None):
    # ... existing code ...
    
    # Calculate ATR-based stop loss
    if not stop_loss_pips:
        # Get recent data
        rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M1, 0, 20)
        df = pd.DataFrame(rates)
        
        # Calculate ATR
        from ta.volatility import AverageTrueRange
        atr = AverageTrueRange(df['high'], df['low'], df['close'], 14)
        atr_value = atr.average_true_range().iloc[-1]
        
        # Set SL to 1.5x ATR
        stop_loss_pips = int((atr_value / point) / 10 * 1.5)
```

### Multiple Symbol Trading

Create separate bot instances for different symbols:

```python
# multi_bot.py
from bot import XAUUSDScalpingBot
import config

# Save original symbol
original_symbol = config.SYMBOL

# Bot 1: XAUUSD
config.SYMBOL = "XAUUSD+"
bot1 = XAUUSDScalpingBot()

# Bot 2: EURUSD
config.SYMBOL = "EURUSD"
bot2 = XAUUSDScalpingBot()

# Run in separate threads
import threading
thread1 = threading.Thread(target=bot1.run)
thread2 = threading.Thread(target=bot2.run)

thread1.start()
thread2.start()
```

## 📊 Advanced Monitoring

### Real-time Performance Dashboard

Create `dashboard.py`:
```python
import time
from statistics import TradingStatistics, monitor_positions
import MetaTrader5 as mt5

def run_dashboard():
    if not mt5.initialize():
        print("Failed to initialize MT5")
        return
    
    stats = TradingStatistics()
    
    while True:
        # Clear screen (Unix/Linux)
        print("\033[2J\033[H")
        
        # Display statistics
        stats.print_statistics()
        
        # Display positions
        monitor_positions()
        
        # Wait 10 seconds
        time.sleep(10)

if __name__ == "__main__":
    run_dashboard()
```

Run alongside the bot:
```bash
# Terminal 1
python bot.py

# Terminal 2
python dashboard.py
```

### Telegram Notifications

Add Telegram bot integration:

```python
# telegram_notifier.py
import requests

class TelegramNotifier:
    def __init__(self, bot_token, chat_id):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.base_url = f"https://api.telegram.org/bot{bot_token}"
    
    def send_message(self, message):
        url = f"{self.base_url}/sendMessage"
        data = {
            "chat_id": self.chat_id,
            "text": message,
            "parse_mode": "HTML"
        }
        try:
            requests.post(url, data=data)
        except Exception as e:
            print(f"Failed to send Telegram notification: {e}")
```

Use in `bot.py`:
```python
# Add to __init__
self.notifier = TelegramNotifier("YOUR_BOT_TOKEN", "YOUR_CHAT_ID")

# In execute_trading_cycle
if result:
    message = f"✅ Position opened: {direction_str}\nProfit Target: +5%"
    self.notifier.send_message(message)
```

## 🔧 Debugging and Optimization

### Enable Debug Logging

```python
# config.py
LOG_LEVEL = "DEBUG"
```

This shows:
- Every prediction with confidence
- All technical indicator values
- Detailed position calculations
- MT5 API calls and responses

### Performance Profiling

Add timing to key functions:

```python
import time

class Timer:
    def __init__(self, name):
        self.name = name
    
    def __enter__(self):
        self.start = time.time()
        return self
    
    def __exit__(self, *args):
        elapsed = time.time() - self.start
        print(f"{self.name} took {elapsed:.3f}s")

# Use it:
with Timer("Prediction"):
    direction, confidence = self.predictor.predict_direction(data)
```

### Backtesting

Create `backtest.py`:
```python
from predictor import MarketPredictor
import MetaTrader5 as mt5
import pandas as pd

def backtest(symbol, start_date, end_date):
    # Get historical data
    rates = mt5.copy_rates_range(symbol, mt5.TIMEFRAME_M1, start_date, end_date)
    df = pd.DataFrame(rates)
    
    # Initialize predictor
    predictor = MarketPredictor()
    
    # Train on first 80%
    train_size = int(len(df) * 0.8)
    predictor.train_model(df[:train_size])
    
    # Test on remaining 20%
    correct = 0
    total = 0
    
    for i in range(train_size, len(df) - 1):
        current_data = df[:i]
        direction, confidence = predictor.predict_direction(current_data)
        
        # Check if prediction was correct
        actual = 1 if df.iloc[i+1]['close'] > df.iloc[i]['close'] else -1
        
        if direction != 0:
            total += 1
            if (direction > 0 and actual > 0) or (direction < 0 and actual < 0):
                correct += 1
    
    accuracy = (correct / total * 100) if total > 0 else 0
    print(f"Backtest Accuracy: {accuracy:.2f}% ({correct}/{total})")
    
    return accuracy
```

## 🚀 Performance Optimization

### Reduce Prediction Interval
For faster systems:
```python
# config.py
PREDICTION_INTERVAL = 0.5  # 500ms instead of 1s
```

### Optimize Indicator Calculation
Cache recent calculations:
```python
class MarketPredictor:
    def __init__(self):
        self.indicator_cache = {}
        self.cache_time = 0
```

### Parallel Processing
Process multiple tasks simultaneously:
```python
from concurrent.futures import ThreadPoolExecutor

def process_signals_parallel(self, df):
    with ThreadPoolExecutor(max_workers=4) as executor:
        rsi_future = executor.submit(self.calculate_rsi, df)
        ema_future = executor.submit(self.calculate_ema, df)
        macd_future = executor.submit(self.calculate_macd, df)
        
        # Wait for all
        rsi = rsi_future.result()
        ema = ema_future.result()
        macd = macd_future.result()
```

## 💡 Advanced Strategies

### Martingale (Risk Warning!)
Double position size after loss:
```python
def calculate_lot_size_martingale(self, last_trade_profit):
    base_size = self.calculate_lot_size(...)
    
    if last_trade_profit < 0:
        return base_size * 2
    else:
        return base_size
```

⚠️ **WARNING**: Martingale is extremely risky!

### Trailing Stop
Move stop loss as profit increases:
```python
def update_trailing_stop(self, position):
    profit_pct = (position.profit / ...) * 100
    
    if profit_pct >= 3:  # Lock in profit at 3%
        new_sl = position.price_current * 0.98  # 2% trailing
        # Modify position with new SL
```

### News Filter
Avoid trading during major news:
```python
def is_news_time(self):
    # Check economic calendar
    # Avoid trading 15 min before/after major news
    pass
```

---

**Remember**: More complexity = more risk. Test thoroughly on demo!
