from requests import post

host = input("Host: ")

channels = ["UCMSVWxNp1lkEGpDClzm8Qvw"]

for i in channels:
    print(get(f'https://pubsubhubbub.appspot.com/subscribe?hub.callback={host}&webhook&hub.mode=subscribe&hub.topic=https://www.youtube.com/xml/feeds/videos.xml?channel_id={i}'))
