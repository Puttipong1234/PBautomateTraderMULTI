from flask import Flask , request

app = Flask(__name__)

@app.route("/") # add path url
def hello_world():
    return "Hello, World!"

@app.route("/webhook")
def webhook():
    return "This is url for webhook!"

@app.route("/signals",methods=['POST'])
def signals():
    print("Someone Post Signals to me !")
    import json
    from trade import CCXT_OPEN_LONG , CCXT_OPEN_SHORT , CCXT_TPSL_LONG , CCXT_TPSL_SHORT , Checkuser
    signal = request.data.decode("utf-8")
    signal = json.loads(signal) # เปลี่ยนจาก json ให้เป็น dictionary

    trade_side = signal["ACTION"]
    amount_coin = float(signal["AMOUNT_COIN"])
    amount_usdt = float(signal["AMOUNT_USDT"])
    leverage = int(signal["LEV"])
    symbol = signal["SYMBOL"]
    password = signal["PASSWORD"]
    factor = float(signal["FACTOR"])
    
    if password != "1100801127618":
        print("WRONG PASSWORD")
        return "403"

    
    print("Check USer")
    print(Checkuser())
    print("ได้รับสัญญาณการซื้อขาย ดังนี้.....")
    print(trade_side)
    print(amount_coin)
    print(leverage)
    print(symbol)
    print("บอทเริ่มทำคำสั่งซื้อขายอัตโนมัติ ไปที่ ไบแนน.....")

    message = f"🤖🤖🤖🤖🤖🤖🤖\n🤖ได้รับสัญญาณการซื้อขาย ดังนี้..... \n🤖รูปแบบการเทรด {trade_side} {symbol}\n🤖จำนวนที่เปิด {amount_coin} \n🤖LEVERAGE {leverage}\n🤖🤖🤖🤖🤖🤖🤖"
    # Line notify Process
    from line_notify import LineNotify
    Access_Token = "bYMefbv4lFK3Bn5esd45e8SqVmw78oHsqL9LrIVQ2DZ" # generate line notify
    notify = LineNotify(Access_Token)
    notify.send(message) # ส่งไปที่ห้องแชท

    # รับสัญญาณ SPOT 
    from trade import buy , sell
    if trade_side == "OPEN LONG" and leverage == 0: # if leverage = 0 => trade spot
        buy(symbol=symbol,amount_coin=amount_coin) # ซื้อแบบ market
    
    elif trade_side == "TPSL LONG" and leverage == 0: # if leverage = 0 => trade spot
        sell(symbol=symbol,amount_coin=amount_coin) # ขายแบบ takeprofit stoploss
    
    # รับสัญญาณ FUTURE
    # from trade import OPEN_LONG , OPEN_SHORT , TPSL_LONG , TPSL_SHORT
    
    # รับแบบ future Cross Mode
    
    # INPUT ของเรา จะเทรดที่ไม้ละกี่ดอล
    AMOUT_USDT = amount_usdt # USER SETTING FUTURE 
    
    # open long
    if trade_side == "OPEN LONG" and leverage > 0:
        # OPEN_LONG(symbol=symbol, amount_usdt=AMOUT_USDT, leverage=leverage)
        CCXT_OPEN_LONG(symbol, amount_coin, factor)
    
    # tpsl long
    elif trade_side == "TPSL LONG" and leverage > 0:
        # TPSL_LONG(symbol=symbol)
        CCXT_TPSL_LONG(symbol, amount_coin, factor)
    
    # open short
    elif trade_side == "OPEN SHORT" and leverage > 0:
        # OPEN_SHORT(symbol=symbol, amount_usdt=AMOUT_USDT, leverage=leverage)
        CCXT_OPEN_SHORT(symbol, amount_coin, factor)
        
    # tpsl short
    elif trade_side == "TPSL SHORT" and leverage > 0:
        # TPSL_SHORT(symbol=symbol)
        CCXT_TPSL_SHORT(symbol, amount_coin, factor)
    return "200"

if __name__=="__main__":
    app.run() # สั่งให้ app run !