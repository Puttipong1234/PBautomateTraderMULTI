import requests
import json

url = 'http://127.0.0.1:5000/signals'
heroku_url = "https://my-bot-trade-only.herokuapp.com/signals" # webhook
ข้อมูลตัวอย่าง = {
            'ACTION': 'OPEN LONG',
            'AMOUNT_COIN' : '100.00',
            'AMOUNT_USDT' : '30.00',
            'LEV' : '15',
            'SYMBOL' : 'ETHUSDT',
            'PASSWORD': "1100801127618"
            }

ข้อมูลตัวอย่าง = json.dumps(ข้อมูลตัวอย่าง)

# x = requests.post(url, data = ข้อมูลตัวอย่าง)
x = requests.post(heroku_url, data = ข้อมูลตัวอย่าง)

print(x.text)