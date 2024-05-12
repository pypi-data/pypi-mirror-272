from dataclasses import dataclass
from enum import Enum
import os.path as path

import PIL.Image as pimg
import base64
from io import BytesIO


BASEPATH = "static/icons"

@dataclass
class Icon:
    name: str|None
    url: str|None
    description: str|None
    id: int|None

class Icons(Enum):
    lightning = Icon(
        name="lightning", 
        url=None,
        description='yellow lightning',
        id=95,
        )
    homer = Icon(
        name='Homer Simpson',
        url=path.join(BASEPATH,'105_homer_simpson.png'),
        description='Close-up of Homer Simpsons face',
        id=105,
    )
    beer_animantion = Icon(
        name="Animated beer mug",
        url=None,
        id=5838,
        description=None
    )    
    santa = Icon(
        name="Santa Claus",
        url=None,
        id=4928,
        description=None
    )
    christmas_tree = Icon(
        name="Christmas tree",
        url=path.join(BASEPATH,"786_christmas_tree.png"),
        description=None,
        id=786
    ) 
    germany = Icon(
        name="Flag Germany",
        url=path.join(BASEPATH,"512_germany.png"),
        description=None,
        id=512
    )    
    germany_wave = Icon(
        name="Flag Germany waving in the wind",
        url=None,
        description=None,
        id=4178
    )
    spring_flowers = Icon(
        name='Spring flowers',
        url=None,
        description=None,
        id=9764
    )    
    spring_flowers_animation = Icon(
        name='Animated spring flowers',
        url=None,
        description=None,
        id=41538
    )
    pizza_animation = Icon(
        name='Animated pizza',
        url=None,
        description=None,
        id=13878
    )


def load_icon_as_base64(url: str) -> str:
    print(url)
    img = pimg.open(url, mode='r')
    buffered = BytesIO()
    img.convert(mode='RGB', colors=256).save(buffered, format="JPEG", quality=100)
    return base64.b64encode(buffered.getvalue()).decode('utf-8')


def main():
    pass

if __name__=="__main__":
    main()