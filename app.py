from flask import Flask , request
from trade import CCXT_OPEN_LONG , CCXT_OPEN_SHORT , CCXT_TPSL_LONG , CCXT_TPSL_SHORT , Checkuser

app = Flask(__name__)

@app.route("/") # add path url
def hello_world():
    return "Hello, World!"

@app.route("/webhook")
def webhook():
    return "This is url for webhook!"

@app.route("/setup")
def setup():
    res = Checkuser()
    return str(res) , 200

@app.route("/signals",methods=['POST'])
def signals():
    print("Someone Post Signals to me !")
    import json
    signal = request.data.decode("utf-8")
    signal = json.loads(signal) # เปลี่ยนจาก json ให้เป็น dictionary

    trade_side = str(signal["ACTION"])
    
    trade_side = trade_side.split(" ")[0] + " " + trade_side.split(" ")[1] # TPSL + LONG
    partial_size = 100
    if len(str(signal["ACTION"]).split(" ")) == 3:
        partial_size = float(str(signal["ACTION"]).split(" ")[2]) # 100 25 .....33.33
    
    
    amount_coin = float(signal["AMOUNT_COIN"])
    amount_usdt = float(signal["AMOUNT_USDT"])
    leverage = signal["LEV"]
    symbol = signal["SYMBOL"]
    password = signal["PASSWORD"]
    factor = float(signal["FACTOR"])
    
    if password != os.getenv("PASSWORD"):
        print("WRONG PASSWORD")
        return "403"

    
    print("ได้รับสัญญาณการซื้อขาย ดังนี้.....")
    print("trade_side : " ,trade_side)
    print("partial_size : ",partial_size)
    print("amount_coin : ",amount_coin)
    print("leverage : ",leverage)
    print("symbol : ",symbol)
    print("บอทเริ่มทำคำสั่งซื้อขายอัตโนมัติ ไปที่ ไบแนน.....")

    message = f"🤖🤖🤖🤖🤖🤖🤖\nได้รับสัญญาณการซื้อขาย \n-รูปแบบการเทรด {trade_side} {symbol}\n-จำนวนที่เปิด {amount_coin} \n-กลยุทธ์ {leverage}\n🤖🤖🤖🤖🤖🤖🤖"
    # Line notify Process
    from line_notify import LineNotify
    Access_Token = os.getenv("LINE_NOTIFY_API") # generate line notify

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
    if trade_side == "OPEN LONG" and "PB" in leverage:
        # OPEN_LONG(symbol=symbol, amount_usdt=AMOUT_USDT, leverage=leverage)
        message = message + CCXT_OPEN_LONG(symbol, amount_coin, factor)
    
    # tpsl long
    elif trade_side == "TPSL LONG" and "PB" in leverage:
        # TPSL_LONG(symbol=symbol)
        amount_coin = (partial_size/100) * amount_coin
        message = message + CCXT_TPSL_LONG(symbol, amount_coin, factor)
    
    # open short
    elif trade_side == "OPEN SHORT" and "PB" in leverage:
        # OPEN_SHORT(symbol=symbol, amount_usdt=AMOUT_USDT, leverage=leverage)
        message = message + CCXT_OPEN_SHORT(symbol, amount_coin, factor)
        
    # tpsl short
    elif trade_side == "TPSL SHORT" and "PB" in leverage:
        # TPSL_SHORT(symbol=symbol)
        amount_coin = (partial_size/100) * amount_coin
        message = message + CCXT_TPSL_SHORT(symbol, amount_coin, factor)
    
    notify = LineNotify(Access_Token)
    notify.send(message) # ส่งไปที่ห้องแชท
    
    return "200"

if __name__=="__main__":
    app.run() # สั่งให้ app run !