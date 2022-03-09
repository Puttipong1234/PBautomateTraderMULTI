import os
from dotenv import load_dotenv

load_dotenv()

BINANCE_API_KEY = "xxxxxxxxxxxxxxxx"
BINANCE_API_SECRET = "xxxxxxxxxxxxxxxx"

LINE_NOTIFY_API = "xxxxxxxxxxxxxxxx"

BINANCE_FUTURE_API_KEY = "xxxx"
BINANCE_FUTURE_API_SECRET = "xxxx"

# แก้ไขเวลา Deploy ขึ้น heroku ใช้ ENV variable เพื่อปกป้อง api key
# heroku config:set BINANCE_API_KEY=xxx
# heroku config:set BINANCE_API_SECRET=xxx
# heroku config:set LINE_NOTIFY_API=xxx
# heroku config:set BINANCE_FUTURE_API_KEY=xxx
# heroku config:set BINANCE_FUTURE_API_SECRET=xxx
# heroku config:set HTTP_PROXY=xxx
# heroku config:set HTTPS_PROXY=xxx

# git add .
# git commit -m "add"
# git push heroku master

BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET")
BINANCE_FUTURE_API_KEY = os.getenv("BINANCE_FUTURE_API_KEY")
BINANCE_FUTURE_API_SECRET = os.getenv("BINANCE_FUTURE_API_SECRET")
LINE_NOTIFY_API = os.getenv("LINE_NOTIFY_API")
TESTING = os.getenv("TESTING")

# BINANCE_API_KEY = "0813c8e8f0ff67b903f4a6ee5bda3bf33ecf93324575aa59b154d049465dfcb0"
# BINANCE_API_SECRET = "79cd1ee2e983d7b3ff99e968d3c08fbd55efe547ad00a33d694901929f4735e2"
# BINANCE_FUTURE_API_KEY = "0813c8e8f0ff67b903f4a6ee5bda3bf33ecf93324575aa59b154d049465dfcb0"
# BINANCE_FUTURE_API_SECRET = "79cd1ee2e983d7b3ff99e968d3c08fbd55efe547ad00a33d694901929f4735e2"
# LINE_NOTIFY_API = "xxx"