from binance_f import RequestClient
from binance_f.constant.test import *
from binance_f.base.printobject import *
from binance_f.model.constant import *
from trade import ccxt_client

from config import BINANCE_FUTURE_API_KEY , BINANCE_FUTURE_API_SECRET





from trade import CCXT_OPEN_LONG , CCXT_OPEN_SHORT , CCXT_TPSL_LONG , CCXT_TPSL_SHORT , Checkuser
r = Checkuser()
print(r)
# r = CCXT_OPEN_LONG(symbol="BTCUSDT", amount_coin_factor=3.62, factor=100)
# r = CCXT_OPEN_SHORT(symbol="BTCUSDT", amount_coin_factor=3.62, factor=100)
# r = CCXT_TPSL_LONG(symbol="BTCUSDT", amount_coin_factor=3.62, factor=100)
# r = CCXT_TPSL_SHORT(symbol="BTCUSDT", amount_coin_factor=3.62, factor=100)







            