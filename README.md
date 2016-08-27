badges will be added here

# QStrader-mini

A mini / lightweight FX trading robot for the OANDA API. Oanda is an FX and commodity broker.

The code is based upon the dummy QSForex architecture, designed by Michael Halls-More in his blog series. The original article can be found  [here](https://www.quantstart.com/articles/Forex-Trading-Diary-1-Automated-Forex-Trading-with-the-OANDA-API)

This extension implements the following custom trading strategies into the original architecture:

* Relative Strenght Index
* others to follow

# Important note 

DO NOT DO REAL TRADING WITH THIS CODE. IT IS EXPERIMENTAL ONLY AND HIGHLY ALPHA STATE!!!!

# Installation and execution instructions

Main compatibility is with Python 3.5.2

* Install Python 3 on your machine
* Clone this repository

```
git clone https://github.com/terzim/qstrader-mini.git
cd qstrader-mini
```

* Install the required dependencies with pip (or pip3)

```
pip3 install requests
```

* Edit the configuration settings in the file settings.py (using your text editor)
```
DOMAIN = choose "practice" (for paper trading) or "live" (for real trading, NON RECOMMENDED)
ACCESS_TOKEN = Insert your access token for OANDA (e.g. 'abcdefghilmnopqrstuvz123456789')
ACCOUNT_ID = Insert your account ID for OANDA (e.g. '1234567')
```

* Launch the robot with: 

```
python3 trading.py
```

This project is constantly being developed, so unfortunately it is likely that it will encounter many issues along the way or may not work properly when installed on your machine.

If you have any questions about this please, or notice any bugs feel free to contact me by filing an "issue" request.

# License Terms

Copyright (c) 2015-2016 Michael Halls-Moore  
Copyright (c) 2016 Massimiliano Terzi

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# Trading Disclaimer

Trading equities or FOREX on margin carries a high level of risk, and may not be suitable for all investors. Past performance is not indicative of future results. The high degree of leverage can work against you as well as for you. Before deciding to invest in equities or FOREX you should carefully consider your investment objectives, level of experience, and risk appetite. The possibility exists that you could sustain a loss of some or all of your initial investment and therefore you should not invest money that you cannot afford to lose. You should be aware of all the risks associated with equities and FOREX trading, and seek advice from an independent financial advisor if you have any doubts.

