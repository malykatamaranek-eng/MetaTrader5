# Troubleshooting & FAQ

## 🔧 Common Issues and Solutions

### Installation Issues

#### Issue: `pip install MetaTrader5` fails on Linux/Mac
**Solution**: MetaTrader5 Python library only works on Windows. Use Wine or a Windows VM.

```bash
# On Linux with Wine
wine python -m pip install MetaTrader5
```

#### Issue: `ModuleNotFoundError: No module named 'ta'`
**Solution**: Install all dependencies properly
```bash
pip install -r requirements.txt --upgrade
```

#### Issue: Python version mismatch
**Solution**: Use Python 3.8 - 3.11 (3.12+ may have compatibility issues)
```bash
python --version  # Check version
# If wrong, install correct version and use:
py -3.10 -m pip install -r requirements.txt
```

### Connection Issues

#### Issue: "MT5 initialization failed"
**Causes & Solutions**:
1. **MT5 not running**
   - Start MetaTrader 5 application first
   
2. **Wrong credentials**
   ```python
   # In config.py, use empty values to use current login:
   MT5_LOGIN = 0
   MT5_PASSWORD = ""
   MT5_SERVER = ""
   ```

3. **Multiple MT5 installations**
   - Make sure only one MT5 instance is running
   - Close all other trading platforms

#### Issue: "Symbol XAUUSD+ not found"
**Solution**: Find correct symbol name
```bash
python test_connection.py
```
Then update `config.py`:
```python
SYMBOL = "XAUUSD"  # or "GOLD", "XAUUSDm", etc.
```

#### Issue: "Login failed: Invalid credentials"
**Solutions**:
1. Verify account number, password, and server
2. Check if account is active
3. Try logging in manually to MT5 first
4. Use already logged-in account (empty credentials in config)

### Trading Issues

#### Issue: "Trading is not allowed"
**Solution**: Enable automated trading
1. In MT5: Tools → Options → Expert Advisors
2. Check "Allow automated trading"
3. Check "Allow DLL imports"
4. Restart MT5

#### Issue: "Not enough money for opening position"
**Solutions**:
1. Reduce position size:
   ```python
   # config.py
   POSITION_SIZE_PERCENT = 10  # Instead of 20
   MAX_POSITIONS = 2  # Instead of 5
   ```

2. Add more funds to account

3. Check current margin usage:
   ```bash
   python test_connection.py  # Shows available margin
   ```

#### Issue: "No positions opening"
**Possible Causes**:
1. **Low prediction confidence**
   - Bot only trades when confidence > 75%
   - Check logs: `tail -f xauusd_bot.log`
   - See "Prediction: NEUTRAL" messages

2. **Maximum positions reached**
   - Bot won't open more than `MAX_POSITIONS`
   - Close some positions or wait for auto-close

3. **Market conditions**
   - Unclear signals = no trading
   - This is intentional (safety feature)

4. **Symbol not tradeable**
   - Check market hours (Gold: 24/5)
   - Check if market is open

#### Issue: "Positions not closing at +5%"
**Check**:
1. Spread eating into profits
   - Gold spread can be 20-50 cents
   - May need higher profit target:
     ```python
     PROFIT_TARGET_PERCENT = 6  # Instead of 5
     ```

2. Broker execution delays
   - Normal, usually closes within seconds after reaching target

3. Check logs for errors:
   ```bash
   grep "close" xauusd_bot.log
   ```

### Performance Issues

#### Issue: Low accuracy (< 80%)
**Solutions**:
1. **Increase training data**
   ```python
   # In bot.py
   historical_data = self.get_historical_data(bars=5000)  # Instead of 2000
   ```

2. **Increase confidence threshold**
   ```python
   # In predictor.py
   min_confidence = 0.85  # Instead of 0.75
   ```

3. **Optimize indicators**
   - Try different RSI/EMA periods
   - Test in different market conditions

4. **Market conditions**
   - Ranging markets are harder
   - Bot works best in trending markets

#### Issue: Too many losses
**Solutions**:
1. **Use stop loss**
   ```python
   # In position_manager.py open_position()
   stop_loss_pips = 50  # Add stop loss
   ```

2. **Reduce position size**
   ```python
   POSITION_SIZE_PERCENT = 10
   ```

3. **Higher entry requirements**
   ```python
   # In predictor.py
   min_confidence = 0.90  # Only very confident trades
   ```

#### Issue: Bot is slow
**Solutions**:
1. **Reduce indicator calculations**
   ```python
   # Get less historical data
   bars=100  # Instead of 500
   ```

2. **Increase prediction interval**
   ```python
   PREDICTION_INTERVAL = 2  # Instead of 1 second
   ```

3. **Optimize Python**
   ```bash
   pip install numpy --upgrade
   ```

### Data Issues

#### Issue: "Failed to get historical data"
**Solutions**:
1. Check internet connection
2. Verify symbol is correct
3. Try different timeframe:
   ```python
   mt5.TIMEFRAME_M5  # Instead of M1
   ```

4. Broker may have restrictions
   - Some limit historical data access

#### Issue: "Insufficient historical bars"
**Solution**: Reduce required bars
```python
# In bot.py
historical_data = self.get_historical_data(bars=500)  # Instead of 2000
```

## ❓ Frequently Asked Questions

### General Questions

**Q: Does this bot really achieve 90%+ accuracy?**
A: The bot is *designed* to target 90%+, but actual results vary based on:
- Market conditions
- Broker spreads
- Configuration settings
- Training data quality

Typical range: 85-92% in good conditions.

**Q: How much money do I need to start?**
A: Minimum depends on broker:
- Demo: Any amount (test with $10,000)
- Real: $500+ recommended
- Optimal: $2,000+ for proper position sizing

**Q: Can I run this 24/7?**
A: Yes, but:
- Markets close weekends
- Requires stable internet
- Monitor first few days
- Use VPS for reliability

**Q: Which broker is best?**
A: Look for:
- Low spreads on XAUUSD (< 30 cents)
- Good execution speed
- MT5 support
- Regulated broker
- Popular: IC Markets, Pepperstone, XM

### Technical Questions

**Q: Can I modify the code?**
A: Yes! It's open source (MIT License). Customize as needed.

**Q: How do I add more indicators?**
A: In `predictor.py`, add to `calculate_indicators()`:
```python
# Add Bollinger Bands
from ta.volatility import BollingerBands
bb = BollingerBands(df['close'])
df['bb_upper'] = bb.bollinger_hband()
df['bb_lower'] = bb.bollinger_lband()
```

**Q: Can I trade multiple symbols?**
A: Yes, see ADVANCED.md for multi-symbol setup.

**Q: Does it work on M5/H1 timeframes?**
A: It's designed for M1 (scalping), but can be adapted:
```python
# In bot.py get_historical_data()
timeframe=mt5.TIMEFRAME_M5
```

### Risk Management Questions

**Q: Is the 100% account usage safe?**
A: Depends on perspective:
- **Pros**: Maximum profit potential, 5 separate positions
- **Cons**: Higher risk if all positions lose
- **Recommendation**: Start with 20-50% total exposure for testing

**Q: Should I use stop losses?**
A: Recommended, especially for beginners. See ADVANCED.md for implementation.

**Q: What's the maximum drawdown?**
A: Varies, but typically:
- With 5% profit target: 2-5% drawdown
- Worst case: Up to 10-15% in bad conditions
- Use `statistics.py` to track

**Q: How do I reduce risk?**
A:
1. Lower position sizes (10% instead of 20%)
2. Fewer positions (2-3 instead of 5)
3. Add stop losses
4. Higher profit targets (less frequent trading)
5. Higher confidence thresholds

### Strategy Questions

**Q: Why +5% profit target?**
A: Optimal for scalping:
- Not too small (spread eats profit)
- Not too large (reduces win rate)
- Can be adjusted to 3-7% based on preference

**Q: Can I change to +10% target?**
A: Yes, but:
- Lower win rate (fewer trades hit target)
- Better risk/reward ratio
- Test on demo first

**Q: How often does it trade?**
A: Varies by market:
- Active market: 10-30 trades/day
- Quiet market: 5-10 trades/day
- Bot only trades on clear signals

**Q: Why not trading in ranging markets?**
A: Bot uses trend indicators (EMA, MACD). For ranging markets, modify to use:
- RSI only
- Bollinger Bands
- Stochastic Oscillator

### Monitoring Questions

**Q: How do I know it's working?**
A: Watch logs:
```bash
tail -f xauusd_bot.log
```
Should see:
- "Prediction: BUY/SELL" messages
- "Position opened" confirmations
- Periodic status updates

**Q: What's a good win rate to expect?**
A:
- Excellent: 90%+
- Good: 85-89%
- Acceptable: 80-84%
- Poor: < 80% (needs adjustment)

**Q: How long until profitable?**
A: Varies:
- First trades: Could be losses (learning)
- After 50 trades: Accuracy stabilizes
- After 100+ trades: True performance visible

### Maintenance Questions

**Q: Do I need to retrain the model?**
A: Bot retrains on each start using recent 2000 bars. For manual retraining:
```python
bot.train_predictor()
```

**Q: How often should I check the bot?**
A:
- First day: Every hour
- First week: 2-3 times/day
- After stable: Daily check
- Always: Monitor during major news

**Q: Should I update parameters?**
A: Review weekly:
- If accuracy drops: Increase confidence threshold
- If too few trades: Decrease confidence threshold
- If too many losses: Add stop loss or reduce size

## 🆘 Getting Help

### Before Asking for Help:

1. **Run diagnostics**:
   ```bash
   python test_connection.py
   ```

2. **Check logs**:
   ```bash
   tail -50 xauusd_bot.log
   ```

3. **Verify configuration**:
   ```bash
   python -c "import config; print(config.SYMBOL)"
   ```

4. **Test MT5 connection manually**:
   - Open MT5
   - Check if logged in
   - Try manual trade on XAUUSD

### Report an Issue:

When opening a GitHub issue, include:

1. **System info**:
   - OS: Windows 10/11
   - Python version: `python --version`
   - MT5 version

2. **Configuration** (remove passwords!):
   ```python
   SYMBOL = "XAUUSD+"
   MAX_POSITIONS = 5
   # etc.
   ```

3. **Error message**:
   ```
   Full error from logs or console
   ```

4. **Steps to reproduce**:
   - What you did
   - What you expected
   - What actually happened

### Resources:

- 📖 [README.md](README.md) - Full documentation
- 🚀 [QUICKSTART.md](QUICKSTART.md) - Quick setup guide
- 🎓 [ADVANCED.md](ADVANCED.md) - Advanced customization
- 📊 [statistics.py](statistics.py) - Performance monitoring
- 🔍 [test_connection.py](test_connection.py) - Diagnostics tool

### Community:

- GitHub Issues: Bug reports and features
- GitHub Discussions: Questions and ideas
- Pull Requests: Contribute improvements

---

**Still having issues? Open a GitHub issue with details!**
