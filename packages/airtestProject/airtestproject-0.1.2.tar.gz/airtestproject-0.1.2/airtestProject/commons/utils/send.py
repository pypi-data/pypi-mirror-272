import json

import requests

webhook = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=c7a70ace-36d2-4780-ab47-c0c449e5ae80'

data1 = {
        "msgtype": "template_card",
        "template_card": {
        "card_type":"news_notice",
            "main_title": {
                "title": "包",
                "desc": "试一下"
            },
            # "image_text_area": {
            #     "type": 1,
            #     "url": "http://10.15.162.65:8000/BC/BCuwa_2024-04-02-1257.apk",
            #     "image_url": r"http://10.15.162.65:8000//qrcode_test.png",
            # },
            "card_image": {
                "aspect_ratio": 1,
                "url": "http://10.15.162.65:8000/qrcode_test.png"
            },
            "card_action": {
                "type": 1,
                "url": "http://10.15.162.65:8000/BC/BCuwa_2024-04-02-1257.apk",
            }
        }
    }

data2 = {
    "msgtype": "news",
    "news": {
       "articles": [
           {
               "title": "？？？？",
               "url": "http://10.15.162.65:8000/BC/BCuwa_2024-04-02-1257.apk",
               "picurl": "http://10.15.162.65:8000//IMG_202404021217_145x145.png"
           }
        ]
    }
}

header = {
        "Content-Type": "application/json",
        "Charset": "UTF-8"
}
# date1 = json.dumps(data1)

info = requests.post(url=webhook, json=data1)
print(info.text)
