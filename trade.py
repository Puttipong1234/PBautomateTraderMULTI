from config import BINANCE_API_KEY , BINANCE_API_SECRET
import ccxt
import os

from binance.client import Client
from binance.helpers import round_step_size

from binance_f import RequestClient
from binance_f.constant.test import *
from binance_f.base.printobject import *
from binance_f.model.constant import *

from config import BINANCE_FUTURE_API_KEY , BINANCE_FUTURE_API_SECRET , TESTING

client = Client(BINANCE_API_KEY, BINANCE_API_SECRET)
future_client = RequestClient(api_key=BINANCE_FUTURE_API_KEY,secret_key=BINANCE_FUTURE_API_SECRET)

def connect_binance_client_ccxt(Binanceapikey,Binancesecretkey):
    print(type(TESTING))
    try:
        exchange = ccxt.binance({
        'apiKey':Binanceapikey,
        'secret':Binancesecretkey,
        'options': {
            'defaultType': 'future',
        },
    })
        if TESTING == "True":
            exchange.set_sandbox_mode(True)
        
        return exchange
        
    except Exception as e:
        err = json.loads(e.args[0].split("binance ")[1])
        return err


def CalculateAmount(AMOUNT_USDT,SYMBOL,LEVERAGE):

    result = future_client.get_mark_price(symbol=SYMBOL)
    ราคาปัจจุบัน = float(result.markPrice)
    AMOUNT_USDT = AMOUNT_USDT * LEVERAGE # Override ตัวแปร

    result = future_client.get_exchange_information()
    for i in result.symbols:
        if i.symbol == SYMBOL:
            # print(i.__dict__)
            print("STEP SIZE : " + i.filters[1]["stepSize"] )
            STEP_SIZE = float(i.filters[1]["stepSize"])
            print("pricePrecision : " + str(i.pricePrecision) )
            จำนวนที่ต้องการซื้อ = AMOUNT_USDT/ราคาปัจจุบัน
            print(จำนวนที่ต้องการซื้อ)
            print(round_step_size(จำนวนที่ต้องการซื้อ,STEP_SIZE))
            
            return str(round_step_size(จำนวนที่ต้องการซื้อ,STEP_SIZE)) # amount_coin ที่คำนวนจาก amount USDT



# เปิด BUY AT MARKET Order !
def buy(symbol,amount_coin):
    # ราคาเหรียญตอนนี้ = client.get_avg_price(symbol="BTCUSDT")
    # ราคาเหรียญตอนนี้ = float(ราคาเหรียญตอนนี้["price"])
    # จำนวนที่ต้องการซื้อ = 20/ราคาเหรียญตอนนี้
    จำนวนที่ต้องการซื้อ = amount_coin
    ข้อมูลเหรียญ = client.get_symbol_info(symbol)
    stepSize = float(ข้อมูลเหรียญ["filters"][2]["stepSize"])
    จำนวนที่ต้องการซื้อ = round_step_size(จำนวนที่ต้องการซื้อ,stepSize)
    # print(จำนวนที่ต้องการซื้อ)

    order = client.order_market_buy(
        symbol=symbol,
        quantity=จำนวนที่ต้องการซื้อ)


 #==================================================
# sell At market
def sell(symbol,amount_coin):
    # balance = float(client.get_asset_balance(asset="BTC")["free"])
    # print(balance)
    จำนวนที่ต้องการขาย = amount_coin
    ข้อมูลเหรียญ = client.get_symbol_info(symbol)
    stepSize = float(ข้อมูลเหรียญ["filters"][2]["stepSize"])
    จำนวนที่ต้องการขาย = round_step_size(จำนวนที่ต้องการขาย- stepSize,stepSize) # 0.00046 - 0.00001 => 0.00045
    # print(จำนวนที่ต้องการขาย)
    order = client.order_market_sell(
        symbol=symbol,
        quantity=จำนวนที่ต้องการขาย)


#======================FUTURE============================
def get_position_amount_by_symbol(symbol):
    
    result = future_client.get_position_v2()
    for i in result:
        data = i.__dict__
        if data["symbol"] == symbol:
            print(data["positionAmt"])
            print(data["unrealizedProfit"])
            
            return str(abs(float(data["positionAmt"])))

def TPSL_LONG(symbol):
    TPSLOrder = future_client.post_order(symbol = symbol,
                                      side = OrderSide.SELL,
                                      ordertype = OrderType.MARKET,
                                      quantity=get_position_amount_by_symbol(symbol),
                                      reduceOnly=True) # ถ้าเป็นการปิด position ต้องใส่ !

def TPSL_SHORT(symbol):
    TPSLOrder = future_client.post_order(symbol = symbol,
                                      side = OrderSide.BUY,
                                      ordertype = OrderType.MARKET,
                                      quantity=get_position_amount_by_symbol(symbol),
                                      reduceOnly=True) # ถ้าเป็นการปิด position ต้องใส่ !
    
def OPEN_LONG(symbol,amount_usdt,leverage):
    quantity = CalculateAmount(AMOUNT_USDT=amount_usdt, SYMBOL=symbol,LEVERAGE=leverage)
    
    try:
        TPSL_SHORT(symbol) # ปิด short ก่อนทุกกรณี
    
    except Exception as e:
        print(e)
    print("QUANTITY:" + str(quantity))
    result = future_client.change_initial_leverage(symbol=symbol, leverage=leverage)
    resultOrder = future_client.post_order(symbol = symbol,
                                        side = OrderSide.BUY, #เปิด LONG BUY , SHORT SELL
                                        ordertype = OrderType.MARKET,
                                        quantity = quantity)
    
    return

def OPEN_SHORT(symbol,amount_usdt,leverage):
    quantity = CalculateAmount(AMOUNT_USDT=amount_usdt, SYMBOL=symbol,LEVERAGE=leverage)
    
    try:
        TPSL_LONG(symbol) # ปิด short ก่อนทุกกรณี
    
    except Exception as e:
        print(e)
    
    result = future_client.change_initial_leverage(symbol=symbol, leverage=leverage)
    resultOrder = future_client.post_order(symbol = symbol,
                                        side = OrderSide.SELL, #เปิด LONG BUY , SHORT SELL
                                        ordertype = OrderType.MARKET,
                                        quantity = quantity)

    
#======================FUTURE============================



#====================== CCXT FUTURE =====================#
ccxt_client = connect_binance_client_ccxt(BINANCE_FUTURE_API_KEY,BINANCE_FUTURE_API_SECRET)

def Checkuser():
    r = ccxt_client.fetch_account_positions()
    result = "User Verify Pass"
    for i in r:
        if i["info"]["symbol"] == "BTCUSDT":

            if i["marginType"] == "isolated":
                ccxt_client.set_margin_mode(marginType="CROSS",symbol="BTCUSDT")
            if i["leverage"] != 10:
                ccxt_client.set_leverage(leverage=10,symbol="BTCUSDT")
            if not i["hedged"] :
                try:
                    ccxt_client.set_position_mode(hedged=True,symbol="BTCUSDT")
                except Exception as e:
                    result = e.args[0]

        
        if i["info"]["symbol"] == "ETHUSDT":
    
            if i["marginType"] == "isolated":
                ccxt_client.set_margin_mode(marginType="CROSS",symbol="ETHUSDT")
            if i["leverage"] != 10:
                ccxt_client.set_leverage(leverage=10,symbol="ETHUSDT")
            if not i["hedged"] :
                try:
                    ccxt_client.set_position_mode(hedged=True,symbol="ETHUSDT")
                except Exception as e:
                    result = e.args[0]

    return result


def CCXT_OPEN_LONG(symbol,amount_coin_factor,factor):
    """_summary_

    Args:
        symbol (_type_): _description_
        amount_coin_factor (_type_): _description_
        leverage (_type_): _description_
        
        side : buy
        posside : long
    """
    ccxt_client.set_leverage(leverage=10,symbol=symbol)
    amount_coin = (amount_coin_factor / factor)
    params={
            "positionSide":"LONG",
            "test":TESTING,
    }
    
    res = ccxt_client.create_order(symbol=symbol, type="market", side="buy", amount=amount_coin,params=params)

    return str(res)

def CCXT_OPEN_SHORT(symbol,amount_coin_factor,factor):
    """_summary_

    Args:
        symbol (_type_): _description_
        amount_coin_factor (_type_): _description_
        leverage (_type_): _description_
        
        side : sell
        posside : short
    """
    """_summary_

    Args:
        symbol (_type_): _description_
        amount_coin_factor (_type_): _description_
        leverage (_type_): _description_
        
        side : buy
        posside : long
    """
    ccxt_client.set_leverage(leverage=10,symbol=symbol)
    amount_coin = (amount_coin_factor / factor)
    params={
            "positionSide":"short",
            "test":TESTING,
    }
    
    res = ccxt_client.create_order(symbol=symbol, type="market", side="sell", amount=amount_coin,params=params)

    return str(res)

def CCXT_TPSL_LONG(symbol,amount_coin_factor,factor):
    """_summary_

    Args:
        symbol (_type_): _description_
        amount_coin_factor (_type_): _description_
        leverage (_type_): _description_
        
        side : sell
        posside : long
    """
    ccxt_client.set_leverage(leverage=10,symbol=symbol)
    amount_coin = (amount_coin_factor / factor)
    params={
            "positionSide":"long",
            "test":TESTING,
    }
    
    res = ccxt_client.create_order(symbol=symbol, type="market", side="sell", amount=amount_coin,params=params)

    return str(res)

def CCXT_TPSL_SHORT(symbol,amount_coin_factor,factor):
    """_summary_

    Args:
        symbol (_type_): _description_
        amount_coin_factor (_type_): _description_
        leverage (_type_): _description_
        
        side : buy
        posside : short
    """
    ccxt_client.set_leverage(leverage=10,symbol=symbol)
    amount_coin = (amount_coin_factor / factor)
    params={
            "positionSide":"short",
            "test":TESTING,
    }
    
    res = ccxt_client.create_order(symbol=symbol, type="market", side="buy", amount=amount_coin,params=params)

    return str(res)



if __name__ == "__main__":
    amount = 0.0004
    sym = "BTCUSDT"
    # buy(symbol=sym,amount_coin=amount)
    # sell(symbol=sym,amount_coin=amount)
    
    # res = CalculateAmount(1000,"BNBUSDT")
    # print(res)
    
    # OPEN_LONG(symbol="DOGEUSDT", amount_usdt=5, leverage=50)
    # TPSL_LONG(symbol="DOGEUSDT")
    # OPEN_SHORT(symbol="DOGEUSDT", amount_usdt=5, leverage=50)
    # TPSL_SHORT(symbol="DOGEUSDT")