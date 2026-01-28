"""
Position Manager for XAUUSD+ Scalping Bot
Manages 5 simultaneous positions with 100% account usage
"""

import MetaTrader5 as mt5
from datetime import datetime
import config


class PositionManager:
    """
    Manages multiple simultaneous positions with automatic profit targets
    """
    
    def __init__(self):
        self.active_positions = []
        self.max_positions = config.MAX_POSITIONS
        
    def get_account_balance(self):
        """
        Get current account balance
        """
        account_info = mt5.account_info()
        if account_info is None:
            return 0
        return account_info.balance
    
    def get_account_equity(self):
        """
        Get current account equity
        """
        account_info = mt5.account_info()
        if account_info is None:
            return 0
        return account_info.equity
    
    def calculate_lot_size(self, symbol, direction):
        """
        Calculate lot size for position (20% of account per position)
        """
        account_info = mt5.account_info()
        if account_info is None:
            return 0.01
        
        # Get symbol info
        symbol_info = mt5.symbol_info(symbol)
        if symbol_info is None:
            return 0.01
        
        # Calculate position value based on account equity
        equity = account_info.equity
        position_value = equity * (config.POSITION_SIZE_PERCENT / 100)
        
        # Get current price
        tick = mt5.symbol_info_tick(symbol)
        if tick is None:
            return 0.01
        
        price = tick.ask if direction == 1 else tick.bid
        
        # Calculate lot size
        contract_size = symbol_info.trade_contract_size
        lot_size = position_value / (price * contract_size)
        
        # Round to allowed lot step
        lot_step = symbol_info.volume_step
        lot_size = round(lot_size / lot_step) * lot_step
        
        # Apply min/max lot limits
        lot_size = max(symbol_info.volume_min, min(lot_size, symbol_info.volume_max))
        
        return lot_size
    
    def get_open_positions_count(self):
        """
        Get number of currently open positions for this bot
        """
        positions = mt5.positions_get(symbol=config.SYMBOL)
        if positions is None:
            return 0
        
        # Filter by magic number
        bot_positions = [p for p in positions if p.magic == config.MAGIC_NUMBER]
        return len(bot_positions)
    
    def can_open_position(self):
        """
        Check if we can open a new position
        """
        return self.get_open_positions_count() < self.max_positions
    
    def open_position(self, symbol, direction, stop_loss_pips=None):
        """
        Open a new position
        direction: 1 for BUY, -1 for SELL
        """
        if not self.can_open_position():
            return None, "Maximum positions reached"
        
        # Get symbol info
        symbol_info = mt5.symbol_info(symbol)
        if symbol_info is None:
            return None, f"Symbol {symbol} not found"
        
        if not symbol_info.visible:
            if not mt5.symbol_select(symbol, True):
                return None, f"Failed to select {symbol}"
        
        # Calculate lot size
        lot = self.calculate_lot_size(symbol, direction)
        
        # Get current price
        tick = mt5.symbol_info_tick(symbol)
        if tick is None:
            return None, "Failed to get tick data"
        
        # Determine order type and price
        if direction == 1:  # BUY
            order_type = mt5.ORDER_TYPE_BUY
            price = tick.ask
        else:  # SELL
            order_type = mt5.ORDER_TYPE_SELL
            price = tick.bid
        
        # Calculate stop loss (conservative for safety)
        point = symbol_info.point
        if stop_loss_pips:
            if direction == 1:
                sl = price - stop_loss_pips * point * 10
            else:
                sl = price + stop_loss_pips * point * 10
        else:
            sl = 0  # No stop loss (will manage by profit target)
        
        # Prepare request
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": lot,
            "type": order_type,
            "price": price,
            "sl": sl,
            "tp": 0,  # Will manage TP manually for +5% target
            "deviation": 20,
            "magic": config.MAGIC_NUMBER,
            "comment": "XAUUSD+ Scalper",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
        
        # Send order
        result = mt5.order_send(request)
        
        if result is None:
            return None, "Order send failed"
        
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            return None, f"Order failed: {result.retcode} - {result.comment}"
        
        return result, "Position opened successfully"
    
    def check_and_close_positions(self):
        """
        Check all open positions and close if profit target reached (+5%)
        """
        positions = mt5.positions_get(symbol=config.SYMBOL)
        if positions is None or len(positions) == 0:
            return []
        
        closed_positions = []
        
        for position in positions:
            # Only manage our positions
            if position.magic != config.MAGIC_NUMBER:
                continue
            
            # Calculate profit percentage (profit / position value)
            # Position value = volume * contract_size * price
            contract_size = 100  # Standard for XAUUSD (100 troy ounces)
            position_value = position.volume * contract_size * position.price_open
            profit_percent = (position.profit / position_value) * 100
            
            # Close if profit target reached
            if profit_percent >= config.PROFIT_TARGET_PERCENT:
                result = self.close_position(position)
                if result:
                    closed_positions.append({
                        'ticket': position.ticket,
                        'profit': position.profit,
                        'profit_percent': profit_percent
                    })
        
        return closed_positions
    
    def close_position(self, position):
        """
        Close a specific position
        """
        # Determine close order type
        if position.type == mt5.ORDER_TYPE_BUY:
            order_type = mt5.ORDER_TYPE_SELL
            price = mt5.symbol_info_tick(position.symbol).bid
        else:
            order_type = mt5.ORDER_TYPE_BUY
            price = mt5.symbol_info_tick(position.symbol).ask
        
        # Prepare close request
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": position.symbol,
            "volume": position.volume,
            "type": order_type,
            "position": position.ticket,
            "price": price,
            "deviation": 100,  # Increased for gold volatility (1.00 dollar)
            "magic": config.MAGIC_NUMBER,
            "comment": "Close by profit target",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_RETURN,  # Try to fill at best price
        }
        
        # Send close order
        result = mt5.order_send(request)
        
        if result is None:
            return False
        
        return result.retcode == mt5.TRADE_RETCODE_DONE
    
    def close_all_positions(self):
        """
        Emergency close all positions
        """
        positions = mt5.positions_get(symbol=config.SYMBOL)
        if positions is None:
            return
        
        for position in positions:
            if position.magic == config.MAGIC_NUMBER:
                self.close_position(position)
    
    def get_positions_summary(self):
        """
        Get summary of all open positions
        """
        positions = mt5.positions_get(symbol=config.SYMBOL)
        if positions is None or len(positions) == 0:
            return {
                'count': 0,
                'total_profit': 0,
                'total_volume': 0
            }
        
        bot_positions = [p for p in positions if p.magic == config.MAGIC_NUMBER]
        
        total_profit = sum(p.profit for p in bot_positions)
        total_volume = sum(p.volume for p in bot_positions)
        
        return {
            'count': len(bot_positions),
            'total_profit': total_profit,
            'total_volume': total_volume,
            'positions': bot_positions
        }
