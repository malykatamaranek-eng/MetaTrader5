# Quick Start Guide - XAUUSD+ Scalping Bot

## 🚀 5-Minute Setup

### Step 1: Prerequisites
- Install Python 3.8+ from python.org
- Install MetaTrader 5 from your broker
- Open a demo account (recommended for testing)

### Step 2: Install Bot
```bash
# Clone repository
git clone https://github.com/malykatamaranek-eng/MetaTrader5.git
cd MetaTrader5

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Configure
Edit `config.py`:
```python
MT5_LOGIN = 12345678  # Your account number
MT5_PASSWORD = "your_password"
MT5_SERVER = "YourBroker-Demo"
SYMBOL = "XAUUSD+"  # Check with test_connection.py
```

**Or use without login:** Leave settings empty to use the currently logged-in MT5 account.

### Step 4: Test Connection
```bash
python test_connection.py
```

This will:
- ✅ Verify MT5 connection
- ✅ Check account info
- ✅ Find available GOLD symbols
- ✅ Test trading permissions

### Step 5: Run Bot
```bash
python bot.py
```

Bot will:
1. Connect to MT5
2. Train prediction model
3. Start trading every second
4. Open up to 5 positions
5. Close automatically at +5% profit

## 📊 What to Expect

### First Minute
```
XAUUSD+ Advanced Scalping Bot Starting
Connected to MT5 account: 12345678
Training market prediction model...
Model trained successfully
Account Balance: $10000.00
Max Positions: 5
```

### During Trading
```
Prediction: BUY with confidence: 82.5%
Position opened: BUY - Ticket: 123456 - Volume: 0.10
Position 123456 closed with profit: $52.30 (5.1%)
Status - Open Positions: 3/5 | Total Profit: $127.50 | Accuracy: 91.2%
```

## ⚙️ Configuration Tips

### For Conservative Trading
```python
MAX_POSITIONS = 2
POSITION_SIZE_PERCENT = 10
PROFIT_TARGET_PERCENT = 3
```

### For Aggressive Trading
```python
MAX_POSITIONS = 5
POSITION_SIZE_PERCENT = 20
PROFIT_TARGET_PERCENT = 5
```

## 🎯 Bot Strategy Explained

### Prediction System (90%+ Target)
- **Machine Learning**: Random Forest on 2000 historical bars
- **RSI**: Detects oversold/overbought
- **EMA**: Trend direction (9 vs 21)
- **MACD**: Momentum confirmation
- **Volume**: Entry confirmation

### Position Management
- Opens position only with 75%+ ML confidence
- Requires multiple indicator confirmation
- Each position = 20% of account (5 × 20% = 100%)
- Monitors every second for +5% profit

### Risk Management
- Maximum 5 positions simultaneously
- Automatic profit taking at +5%
- Optional ATR-based stop loss
- High win rate minimizes losses

## 📱 Monitoring

### Watch These Metrics
- **Open Positions**: Should stay between 0-5
- **Accuracy**: Target 90%+, acceptable 85%+
- **Total Profit**: Should grow over time
- **Confidence**: Only trades when 75%+

### Red Flags
- Accuracy below 80% (market conditions may be unsuitable)
- Frequent position opening/closing (spread too high)
- Unable to open positions (insufficient margin)

## 🛑 Stopping the Bot

Press `Ctrl+C` to stop gracefully. The bot will:
- Stop opening new positions
- Show final summary
- Close MT5 connection
- Keep existing positions open (optional to close)

## 💡 Pro Tips

1. **Start Small**: Test with 2 positions first
2. **Monitor First Hour**: Watch bot behavior closely
3. **Check Symbol**: Use `test_connection.py` to find correct symbol
4. **Demo First**: Always test on demo account
5. **Check Spread**: Gold spread affects profitability
6. **Trading Hours**: Bot works 24/5, but best during high liquidity

## ❓ Common Issues

### "Symbol not found"
- Run `test_connection.py` to find correct symbol name
- Update `SYMBOL` in config.py

### "Insufficient margin"
- Reduce `MAX_POSITIONS` or `POSITION_SIZE_PERCENT`
- Add more funds to account

### "Trading not allowed"
- Enable automated trading in MT5
- Tools → Options → Expert Advisors → Allow automated trading

### Low accuracy
- Bot needs 100+ trades to stabilize
- Market conditions affect performance
- Consider adjusting technical indicator parameters

## 📈 Performance Expectations

### Realistic Goals
- **Win Rate**: 85-92% (target 90%+)
- **Profit per Trade**: +5% (set in config)
- **Trades per Day**: Varies (depends on market signals)
- **Daily Return**: 1-5% (with good conditions)

### Important Notes
- Past performance ≠ future results
- Market conditions vary
- Always have a backup plan
- Never risk more than you can afford to lose

## 🎓 Learning Resources

- `bot.py`: Main bot logic
- `predictor.py`: ML and technical analysis
- `position_manager.py`: Position handling
- `config.py`: All adjustable parameters

## 🆘 Need Help?

1. Check logs: `xauusd_bot.log`
2. Run: `python test_connection.py`
3. Review README.md for detailed docs
4. Open issue on GitHub

---

**Ready to Trade! 🚀**

Remember: Start with demo account, monitor closely, and scale gradually!
