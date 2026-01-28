"""
Test script to verify MT5 connection and symbol availability
Run this before starting the bot
"""

import MetaTrader5 as mt5
import sys


def test_mt5_connection():
    """
    Test MetaTrader5 connection and configuration
    """
    print("=" * 60)
    print("MetaTrader5 Connection Test")
    print("=" * 60)
    
    # Initialize MT5
    if not mt5.initialize():
        print("❌ ERROR: MT5 initialization failed")
        print(f"Error: {mt5.last_error()}")
        print("\nMake sure MetaTrader5 is installed and running!")
        return False
    
    print("✅ MT5 initialized successfully")
    
    # Get account info
    account_info = mt5.account_info()
    if account_info is None:
        print("❌ ERROR: Failed to get account info")
        print(f"Error: {mt5.last_error()}")
        mt5.shutdown()
        return False
    
    print("\n" + "=" * 60)
    print("Account Information")
    print("=" * 60)
    print(f"Login: {account_info.login}")
    print(f"Server: {account_info.server}")
    print(f"Name: {account_info.name}")
    print(f"Balance: ${account_info.balance:.2f}")
    print(f"Equity: ${account_info.equity:.2f}")
    print(f"Margin: ${account_info.margin:.2f}")
    print(f"Free Margin: ${account_info.margin_free:.2f}")
    print(f"Leverage: 1:{account_info.leverage}")
    print(f"Currency: {account_info.currency}")
    
    # Test symbol availability
    print("\n" + "=" * 60)
    print("Symbol Tests")
    print("=" * 60)
    
    symbols_to_test = ["XAUUSD", "XAUUSD+", "GOLD", "XAUUSD.a", "XAUUSDm"]
    
    found_symbols = []
    for symbol in symbols_to_test:
        symbol_info = mt5.symbol_info(symbol)
        if symbol_info is not None:
            print(f"✅ {symbol} - Available")
            
            # Get current price
            tick = mt5.symbol_info_tick(symbol)
            if tick:
                print(f"   Bid: {tick.bid:.2f}, Ask: {tick.ask:.2f}, Spread: {tick.ask - tick.bid:.2f}")
            
            print(f"   Contract Size: {symbol_info.trade_contract_size}")
            print(f"   Min Volume: {symbol_info.volume_min}")
            print(f"   Max Volume: {symbol_info.volume_max}")
            print(f"   Volume Step: {symbol_info.volume_step}")
            
            found_symbols.append(symbol)
        else:
            print(f"❌ {symbol} - Not available")
    
    if not found_symbols:
        print("\n❌ ERROR: No XAUUSD symbols found!")
        print("Please check with your broker for the correct symbol name.")
        mt5.shutdown()
        return False
    
    print("\n" + "=" * 60)
    print("Recommendation")
    print("=" * 60)
    print(f"Use one of these symbols in config.py: {', '.join(found_symbols)}")
    print(f"Recommended: SYMBOL = \"{found_symbols[0]}\"")
    
    # Test historical data
    print("\n" + "=" * 60)
    print("Historical Data Test")
    print("=" * 60)
    
    test_symbol = found_symbols[0]
    rates = mt5.copy_rates_from_pos(test_symbol, mt5.TIMEFRAME_M1, 0, 10)
    
    if rates is None or len(rates) == 0:
        print(f"❌ ERROR: Failed to get historical data for {test_symbol}")
        mt5.shutdown()
        return False
    
    print(f"✅ Successfully retrieved {len(rates)} bars of historical data")
    print(f"Latest close price: {rates[-1]['close']:.2f}")
    
    # Test trading permissions
    print("\n" + "=" * 60)
    print("Trading Permissions")
    print("=" * 60)
    
    if account_info.trade_allowed:
        print("✅ Trading is allowed")
    else:
        print("❌ WARNING: Trading is not allowed")
        print("Enable automated trading in MT5: Tools -> Options -> Expert Advisors")
    
    if account_info.trade_expert:
        print("✅ Expert Advisor trading is enabled")
    else:
        print("❌ WARNING: Expert Advisor trading is disabled")
        print("Enable 'Allow automated trading' in MT5")
    
    print("\n" + "=" * 60)
    print("Test Complete")
    print("=" * 60)
    print("✅ All tests passed! You can now run the bot.")
    print("\nTo start the bot, run: python bot.py")
    
    mt5.shutdown()
    return True


if __name__ == "__main__":
    try:
        success = test_mt5_connection()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
