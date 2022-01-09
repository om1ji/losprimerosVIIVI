from requests import post
from time import sleep

host = input("Host: ")

url = ["UCMSVWxNp1lkEGpDClzm8Qvw"]
while True:
    for i in url:
        r = post(f'https://pubsubhubbub.appspot.com/subscribe?hub.callback={host}/webhook&hub.mode=subscribe&hub.topic=https://www.youtube.com/xml/feeds/videos.xml?channel_id={i}')
        print(r.status_code)
    print('Wait 6 days')
    sleep(518400)
