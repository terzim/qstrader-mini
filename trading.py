import queue
import threading
import time
import decimal

from execution import Execution
from settings import ENVIRONMENTS
from strategy import RSIStrategy
from streaming import StreamingForexPrices
from gui import GUI
from tkinter import *

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
                    strategy.gainsandlosses(event)
                    strategy.print_signals(event)
                    strategy.calculate_signals(event)
                elif event.type == 'ORDER':
                    print("Executing order!")
                    execution.execute_order(event)
        time.sleep(heartbeat)


if __name__ == "__main__":

    def on_closing():
        sys.exit()

    root = Tk()
    root.title("QSForex-mini by M.Terzi")
    gui = GUI(root)
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

    # heartbeat = 0.5  # Half a second between polling
    heartbeat = int(gui.variables[5].get())  # Half a seconds between polling
    events = queue.Queue()

    # Trade 10000 units of EUR/USD
    instrument = gui.variables[3].get()
    units = int(gui.variables[4].get())
    min_window = int(gui.variables[7].get())
    persistence = int(gui.variables[8].get())
    rsiupboundary = int(gui.variables[9].get())
    rsilowboundary = int(gui.variables[10].get())

    STREAM_DOMAIN = ENVIRONMENTS["streaming"][gui.variables[0].get()]
    API_DOMAIN = ENVIRONMENTS["api"][gui.variables[0].get()]
    ACCESS_TOKEN = gui.variables[2].get()
    ACCOUNT_ID = gui.variables[1].get()

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
    strategy = RSIStrategy(instrument, units, events, min_window, persistence, rsilowboundary, rsiupboundary)

    # Create two separate threads: One for the trading loop
    # and another for the market price streaming class
    trade_thread = threading.Thread(target=trade, args=(events, strategy, execution))
    price_thread = threading.Thread(target=prices.stream_to_queue, args=[])

    # Start both threads
    trade_thread.start()
    price_thread.start()
