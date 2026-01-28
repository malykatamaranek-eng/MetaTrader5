"""
Main XAUUSD+ Scalping Bot
Advanced automated trading with 90%+ accuracy target
"""

import MetaTrader5 as mt5
import pandas as pd
import time
import logging
from datetime import datetime
import sys

import config
from predictor import MarketPredictor
from position_manager import PositionManager


class XAUUSDScalpingBot:
    """
    Advanced scalping bot for XAUUSD+ with:
    - Market prediction every second
    - 5 simultaneous positions
    - 100% account usage (20% per position)
    - Automatic closing at +5% profit
    - 90%+ win rate target
    """
    
    def __init__(self):
        self.predictor = MarketPredictor()
        self.position_manager = PositionManager()
        self.is_running = False
        self.setup_logging()
        
    def setup_logging(self):
        """
        Setup logging configuration
        """
        logging.basicConfig(
            level=getattr(logging, config.LOG_LEVEL),
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(config.LOG_FILE),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def connect_mt5(self):
        """
        Connect to MetaTrader 5
        """
        if not mt5.initialize():
            self.logger.error(f"MT5 initialization failed: {mt5.last_error()}")
            return False
        
        # Login if credentials provided
        if config.MT5_LOGIN and config.MT5_PASSWORD and config.MT5_SERVER:
            authorized = mt5.login(
                login=config.MT5_LOGIN,
                password=config.MT5_PASSWORD,
                server=config.MT5_SERVER
            )
            
            if not authorized:
                self.logger.error(f"MT5 login failed: {mt5.last_error()}")
                mt5.shutdown()
                return False
            
            self.logger.info(f"Connected to MT5 account: {config.MT5_LOGIN}")
        else:
            self.logger.info("Connected to MT5 (using default account)")
        
        # Check if symbol is available
        symbol_info = mt5.symbol_info(config.SYMBOL)
        if symbol_info is None:
            self.logger.error(f"Symbol {config.SYMBOL} not found")
            mt5.shutdown()
            return False
        
        if not symbol_info.visible:
            if not mt5.symbol_select(config.SYMBOL, True):
                self.logger.error(f"Failed to select {config.SYMBOL}")
                mt5.shutdown()
                return False
        
        self.logger.info(f"Symbol {config.SYMBOL} is ready for trading")
        return True
    
    def get_historical_data(self, timeframe=mt5.TIMEFRAME_M1, bars=500):
        """
        Get historical data for training and analysis
        """
        rates = mt5.copy_rates_from_pos(config.SYMBOL, timeframe, 0, bars)
        
        if rates is None or len(rates) == 0:
            self.logger.error(f"Failed to get historical data: {mt5.last_error()}")
            return None
        
        df = pd.DataFrame(rates)
        df['time'] = pd.to_datetime(df['time'], unit='s')
        
        return df
    
    def train_predictor(self):
        """
        Train the market prediction model
        """
        self.logger.info("Training market prediction model...")
        
        # Get more historical data for training
        historical_data = self.get_historical_data(timeframe=mt5.TIMEFRAME_M1, bars=2000)
        
        if historical_data is None:
            self.logger.error("Cannot train model - no historical data")
            return False
        
        success = self.predictor.train_model(historical_data)
        
        if success:
            self.logger.info("Market prediction model trained successfully")
        else:
            self.logger.error("Failed to train prediction model")
        
        return success
    
    def execute_trading_cycle(self):
        """
        Execute one trading cycle (called every second)
        """
        # Check and close positions that reached profit target
        closed = self.position_manager.check_and_close_positions()
        
        if closed:
            for pos in closed:
                self.logger.info(
                    f"Position {pos['ticket']} closed with profit: "
                    f"${pos['profit']:.2f} ({pos['profit_percent']:.2f}%)"
                )
        
        # Get current positions summary
        summary = self.position_manager.get_positions_summary()
        
        # Check if we can open new positions
        if not self.position_manager.can_open_position():
            return
        
        # Get recent data for prediction
        current_data = self.get_historical_data(timeframe=mt5.TIMEFRAME_M1, bars=100)
        
        if current_data is None:
            return
        
        # Predict market direction
        direction, confidence = self.predictor.predict_direction(current_data)
        
        if direction == 0:
            # No clear signal - don't trade
            return
        
        # Log prediction
        direction_str = "BUY" if direction == 1 else "SELL"
        self.logger.info(
            f"Prediction: {direction_str} with confidence: {confidence:.2%}"
        )
        
        # Open position based on prediction
        result, message = self.position_manager.open_position(
            config.SYMBOL,
            direction
        )
        
        if result:
            self.logger.info(
                f"Position opened: {direction_str} - Ticket: {result.order} - "
                f"Volume: {result.volume} - Price: {result.price}"
            )
        else:
            self.logger.warning(f"Failed to open position: {message}")
    
    def run(self):
        """
        Main bot loop
        """
        self.logger.info("=" * 60)
        self.logger.info("XAUUSD+ Advanced Scalping Bot Starting")
        self.logger.info("=" * 60)
        
        # Connect to MT5
        if not self.connect_mt5():
            self.logger.error("Failed to connect to MT5")
            return
        
        # Train predictor
        if not self.train_predictor():
            self.logger.error("Failed to train prediction model")
            mt5.shutdown()
            return
        
        # Get account info
        account_info = mt5.account_info()
        if account_info:
            self.logger.info(f"Account Balance: ${account_info.balance:.2f}")
            self.logger.info(f"Account Equity: ${account_info.equity:.2f}")
            self.logger.info(f"Account Leverage: 1:{account_info.leverage}")
        
        self.logger.info(f"Trading Symbol: {config.SYMBOL}")
        self.logger.info(f"Max Positions: {config.MAX_POSITIONS}")
        self.logger.info(f"Position Size: {config.POSITION_SIZE_PERCENT}% per position")
        self.logger.info(f"Profit Target: +{config.PROFIT_TARGET_PERCENT}%")
        self.logger.info(f"Prediction Interval: {config.PREDICTION_INTERVAL}s")
        self.logger.info("=" * 60)
        
        self.is_running = True
        cycle_count = 0
        
        try:
            while self.is_running:
                cycle_count += 1
                
                # Execute trading cycle
                self.execute_trading_cycle()
                
                # Log status every 60 seconds
                if cycle_count % 60 == 0:
                    summary = self.position_manager.get_positions_summary()
                    accuracy = self.predictor.get_current_accuracy()
                    
                    self.logger.info(
                        f"Status - Open Positions: {summary['count']}/{config.MAX_POSITIONS} | "
                        f"Total Profit: ${summary['total_profit']:.2f} | "
                        f"Accuracy: {accuracy:.1f}%"
                    )
                
                # Wait for next cycle (1 second)
                time.sleep(config.PREDICTION_INTERVAL)
                
        except KeyboardInterrupt:
            self.logger.info("\nBot stopped by user")
        except Exception as e:
            self.logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        finally:
            self.shutdown()
    
    def shutdown(self):
        """
        Shutdown bot gracefully
        """
        self.logger.info("Shutting down bot...")
        self.is_running = False
        
        # Close all positions (optional - comment out if you want to keep them open)
        # self.position_manager.close_all_positions()
        
        # Get final summary
        summary = self.position_manager.get_positions_summary()
        account_info = mt5.account_info()
        
        self.logger.info("=" * 60)
        self.logger.info("Final Summary")
        self.logger.info("=" * 60)
        self.logger.info(f"Open Positions: {summary['count']}")
        self.logger.info(f"Total Profit: ${summary['total_profit']:.2f}")
        if account_info:
            self.logger.info(f"Account Balance: ${account_info.balance:.2f}")
            self.logger.info(f"Account Equity: ${account_info.equity:.2f}")
        
        accuracy = self.predictor.get_current_accuracy()
        if accuracy > 0:
            self.logger.info(f"Final Accuracy: {accuracy:.1f}%")
        
        self.logger.info("=" * 60)
        
        # Shutdown MT5
        mt5.shutdown()
        self.logger.info("Bot shutdown complete")


def main():
    """
    Entry point for the bot
    """
    bot = XAUUSDScalpingBot()
    bot.run()


if __name__ == "__main__":
    main()
