"""
Statistics and monitoring utilities for the bot
"""

import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime, timedelta
import config


class TradingStatistics:
    """
    Calculate and display trading statistics
    """
    
    def __init__(self):
        self.stats = {
            'total_trades': 0,
            'winning_trades': 0,
            'losing_trades': 0,
            'total_profit': 0.0,
            'total_loss': 0.0,
            'win_rate': 0.0,
            'avg_profit': 0.0,
            'avg_loss': 0.0,
            'profit_factor': 0.0,
            'max_drawdown': 0.0,
        }
    
    def get_historical_deals(self, days=7):
        """
        Get historical deals from MT5
        """
        from_date = datetime.now() - timedelta(days=days)
        deals = mt5.history_deals_get(from_date, datetime.now())
        
        if deals is None or len(deals) == 0:
            return None
        
        # Filter by magic number
        bot_deals = [d for d in deals if d.magic == config.MAGIC_NUMBER]
        
        return bot_deals
    
    def calculate_statistics(self, deals=None):
        """
        Calculate trading statistics
        """
        if deals is None:
            deals = self.get_historical_deals()
        
        if not deals:
            return self.stats
        
        # Create DataFrame for easier analysis
        df = pd.DataFrame(list(deals), columns=deals[0]._asdict().keys())
        
        # Filter only closed positions (exit deals)
        df = df[df['entry'] == 1]  # Entry 1 means out/close
        
        if len(df) == 0:
            return self.stats
        
        self.stats['total_trades'] = len(df)
        self.stats['winning_trades'] = len(df[df['profit'] > 0])
        self.stats['losing_trades'] = len(df[df['profit'] < 0])
        
        self.stats['total_profit'] = df[df['profit'] > 0]['profit'].sum()
        self.stats['total_loss'] = abs(df[df['profit'] < 0]['profit'].sum())
        
        if self.stats['total_trades'] > 0:
            self.stats['win_rate'] = (self.stats['winning_trades'] / self.stats['total_trades']) * 100
        
        if self.stats['winning_trades'] > 0:
            self.stats['avg_profit'] = self.stats['total_profit'] / self.stats['winning_trades']
        
        if self.stats['losing_trades'] > 0:
            self.stats['avg_loss'] = self.stats['total_loss'] / self.stats['losing_trades']
        
        if self.stats['total_loss'] > 0:
            self.stats['profit_factor'] = self.stats['total_profit'] / self.stats['total_loss']
        
        # Calculate max drawdown
        df['cumulative'] = df['profit'].cumsum()
        df['cumulative_max'] = df['cumulative'].cummax()
        df['drawdown'] = df['cumulative_max'] - df['cumulative']
        self.stats['max_drawdown'] = df['drawdown'].max()
        
        return self.stats
    
    def print_statistics(self):
        """
        Print formatted statistics
        """
        stats = self.calculate_statistics()
        
        print("\n" + "=" * 60)
        print("Trading Statistics")
        print("=" * 60)
        print(f"Total Trades: {stats['total_trades']}")
        print(f"Winning Trades: {stats['winning_trades']}")
        print(f"Losing Trades: {stats['losing_trades']}")
        print(f"Win Rate: {stats['win_rate']:.2f}%")
        print(f"\nTotal Profit: ${stats['total_profit']:.2f}")
        print(f"Total Loss: ${stats['total_loss']:.2f}")
        print(f"Net Profit: ${stats['total_profit'] - stats['total_loss']:.2f}")
        print(f"\nAverage Win: ${stats['avg_profit']:.2f}")
        print(f"Average Loss: ${stats['avg_loss']:.2f}")
        print(f"Profit Factor: {stats['profit_factor']:.2f}")
        print(f"Max Drawdown: ${stats['max_drawdown']:.2f}")
        print("=" * 60 + "\n")
        
        return stats


def monitor_positions():
    """
    Monitor and display current positions
    """
    positions = mt5.positions_get(symbol=config.SYMBOL)
    
    if positions is None or len(positions) == 0:
        print("No open positions")
        return
    
    # Filter by magic number
    bot_positions = [p for p in positions if p.magic == config.MAGIC_NUMBER]
    
    if len(bot_positions) == 0:
        print("No bot positions open")
        return
    
    print("\n" + "=" * 80)
    print("Current Positions")
    print("=" * 80)
    print(f"{'Ticket':<12} {'Type':<6} {'Volume':<8} {'Open':<10} {'Current':<10} {'Profit':<10} {'%':<8}")
    print("-" * 80)
    
    for pos in bot_positions:
        pos_type = "BUY" if pos.type == 0 else "SELL"
        current_price = pos.price_current
        profit_pct = (pos.profit / (pos.volume * pos.price_open)) * 100
        
        print(f"{pos.ticket:<12} {pos_type:<6} {pos.volume:<8.2f} {pos.price_open:<10.2f} "
              f"{current_price:<10.2f} ${pos.profit:<9.2f} {profit_pct:>6.2f}%")
    
    total_profit = sum(p.profit for p in bot_positions)
    print("-" * 80)
    print(f"Total Positions: {len(bot_positions)} | Total Profit: ${total_profit:.2f}")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    # Initialize MT5
    if not mt5.initialize():
        print("MT5 initialization failed")
        exit()
    
    # Display statistics
    stats_calculator = TradingStatistics()
    stats_calculator.print_statistics()
    
    # Monitor positions
    monitor_positions()
    
    mt5.shutdown()
