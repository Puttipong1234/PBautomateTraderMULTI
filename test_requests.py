import requests
import json

url = 'http://127.0.0.1:5000/signals'
heroku_url = "https://my-bot-trade-only-eu.herokuapp.com/signals" # webhook
ข้อมูลตัวอย่าง = {
            'ACTION': 'OPEN SHORT', # << USE
            'AMOUNT_COIN' : '0.1', # << USE
            'AMOUNT_USDT' : '30.00',
            'LEV' : '[PB-BTC-06]', 
            'SYMBOL' : 'BTCBUSD', # << USE
            'PASSWORD': "1100801127618", # << USE
            'FACTOR' : "10" # << USE....
            }

ข้อมูลตัวอย่าง = json.dumps(ข้อมูลตัวอย่าง)

x = requests.post(heroku_url, data = ข้อมูลตัวอย่าง)
# x = requests.post(heroku_url, data = ข้อมูลตัวอย่าง)

print(x.text)