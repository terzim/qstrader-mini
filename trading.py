import queue
import threading
import time
import decimal

from execution import Execution
from settings import STREAM_DOMAIN, API_DOMAIN, ACCESS_TOKEN, ACCOUNT_ID
from strategy import RSIStrategy
from streaming import StreamingForexPrices


def trade(events, strategy, execution):
    """
    Carries out an infinite while loop that polls the
    events queue and directs each event to either the
    strategy component of the execution handler. The
    loop will then pause for "heartbeat" seconds and
    continue.
    """
    while True:
        decimal.getcontext().prec = 7
        try:
            event = events.get(False)
        except queue.Empty:
            pass
        else:
            if event is not None:
                if event.type == 'TICK':
                    strategy.pricelist(event)
                    strategy.print_signals(event)
                    strategy.calculate_signals(event)
                elif event.type == 'ORDER':
                    print("Executing order!")
                    execution.execute_order(event)
        time.sleep(heartbeat)


if __name__ == "__main__":
    # heartbeat = 0.5  # Half a second between polling
    heartbeat = 0.5  # Half a seconds between polling
    events = queue.Queue()

    # Trade 10000 units of EUR/USD
    instrument = "EUR_USD"
    units = 5
    min_window = 20
    rsiupboundary = 80
    rsilowboundary = 20

    # Create the OANDA market price streaming class
    # making sure to provide authentication commands
    prices = StreamingForexPrices(
        STREAM_DOMAIN, ACCESS_TOKEN, ACCOUNT_ID,
        instrument, events
    )

    # Create the execution handler making sure to
    # provide authentication commands
    execution = Execution(API_DOMAIN, ACCESS_TOKEN, ACCOUNT_ID)

    # Create the strategy/signal generator, passing the
    # instrument, quantity of units and the events queue
    strategy = RSIStrategy(instrument, units, events, min_window, rsilowboundary, rsiupboundary)

    # Create two separate threads: One for the trading loop
    # and another for the market price streaming class
    trade_thread = threading.Thread(target=trade, args=(events, strategy, execution))
    price_thread = threading.Thread(target=prices.stream_to_queue, args=[])

    # Start both threads
    trade_thread.start()
    price_thread.start()