## PYBOTT BOILERPLATE V.2
tradingview --> Heroku --> binance with multiple profits taking

#### Req : สิ่งที่ต้องเตรียม
- Binance Future PortFolio 
    - hedgemode enable
    - cross enable
- Tradingview Pro for Webhook
- Heroku Account + hobby plan
- Binance API key & secret (Future Enable)

#### Setup : การติดตั้ง
- clone this repo
- remote to your heroku repo
- push to heroku
- setup user env config
- test_requests
- create tradingview webhook alert
- Finish !!!

#### maintainance : การดูแลรักษา
- หมั่นตรวจสอบ Position เมื่อมีการ Alert โดยการดู LOG ใน heroku
- ตรวจสอบความเรียบร้อยของ Subscription
- ระวังอย่าให้ API หลุดเป็นอันขาด หากมีปัญหาให้ติดต่อแอดมินเป็นคนแรก เพื่อความปลอดภัยของทรัพย์สินท่าน