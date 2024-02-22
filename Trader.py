from dis import Positions
#from logging import raiseExceptions
from re import T
import config as cf
import time
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest, QueryOrderStatus, GetOrdersRequest, CancelOrderResponse
from alpaca.trading.enums import OrderSide, TimeInForce


class Trader(object):
    def __init__(self) -> None:
        # Create REST API connection
        self.client = TradingClient(cf.ALPACA_API_KEY, cf.ALPACA_SECRET_KEY, paper=True)
        
        self.signal_generator = Signal_Generator()

    def buy_market_order(self, symbol, qty, time_in_force = 'day') -> str:
        # preparing orders
        market_order_data = MarketOrderRequest(
                    symbol          = symbol,
                    qty             = qty,
                    side            = OrderSide.BUY,
                    time_in_force   = TimeInForce.DAY)

        # Submit market order to buy stock
        market_order = self.client.submit_order(order_data=market_order_data)

        # Wait before checking for live changes to your portfolio to give time for your account to update
        time.sleep(5)

        # Get stock position
        try:
            positions = self.client.get_all_positions()
        except:
            positions = None

        return positions[0]

    def cancel_all_orders(self):
        # Cancel order
        #status = CancelOrderResponse()
        self.client.cancel_orders()
        
    def wait_for_signal(self, symbol, buy=True) -> bool:
        if self.signal_generator.has_signalled(symbol, buy=buy):
            return True
        else:
            return False
        

class Signal_Generator(object):
    def __init__(self) -> None:
        pass

    def has_signalled(self, symbol, buy) -> bool:
        return True

    def get_qty(self, symbol) -> int:
        return 1



