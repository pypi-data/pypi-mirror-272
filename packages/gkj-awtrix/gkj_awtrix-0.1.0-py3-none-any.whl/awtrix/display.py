import awtrix.effects as ef
import awtrix.icons as ic
import awtrix.device as dev
import requests


def icon_text(
        text: str, 
        icon: ic.Icon, 
        duration: int=5, 
        repeat=1, 
        use_icon_file: bool=False,
        effect_in: ef.effects = ef.effects.looking_eyes,
        effect_out: ef.effects = ef.effects.ping_pong,
        lifetime: int|None = None,
        name:str = 'test'
        ):
    url=dev.AWTRIX_BASE_URL+'/api/custom?name='+name
    if use_icon_file:
        ico = ic.load_icon_as_base64(url=icon.url)
    else:
        ico = icon.id
    if not lifetime:
        lifetime=1E32
    myobj = [
        {
        'effect':effect_in.value.name,
        'duration': 3,
        'lifetime': lifetime,
        },    
        {
        'text': text, 
        'duration': duration, 
        'stack': True, 
        'icon': ico, 
        'repeat': repeat, 
        'scrollSpeed': 30,
        'textCase': 2,
        'overlay':'',
        'stack': True,
        'lifetime': lifetime
        },
        {
        'effect':effect_out.value.name,
        'duration': 3,
        'lifetime': lifetime,
        },    
    ]
    requests.post(url=url, json=myobj)



def hello_world(url: str) -> None:
    myobj = {'text': 'Hello', 'duration': 5, 'blinkText': 150, 'stack': True}
    myobj2 = {'text': 'World!', 'duration': 5, 'blinkText': 150, 'stack': True}
    
    requests.post(url=url, json=myobj)
    requests.post(url=url, json=myobj2)


def count_down_to_extinction(url: str) -> None:
    text_tpl = ('Count', 'down', 'to', 'ex-', 'tinction', '5', '4', '3', '2', '1', '0', '', '---')

    for ix, i in enumerate(range(0,101,10)):
        centered=lambda x : len(x)<3 
        myobj = {
            'text': text_tpl[ix],
            # 'fadeText': 100,
            'center': centered(text_tpl[ix]),
            'color': '#FF0000',
            'progress': i, 
            'progressC': [int(i*2.55), 255-int(i*2.55), 0], 
            'progressBC': [int(i*2.55), int(i*2.55), 255-int(i*2.55)], 
            'duration': 1, 
            'stack': True
        }
        requests.post(url=url, json=myobj)
        time.sleep(0.9)







def main():
    pass

if __name__=="__main__":
    main()