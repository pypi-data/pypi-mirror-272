from enum import Enum
from dataclasses import dataclass

@dataclass
class Effect:
    name: str
    max_speed: int|None
    std_palette: str|None
    blend: bool

class effects(Enum):
    fade = Effect(name='Fade', max_speed=1, std_palette='Rainbow', blend=True)
    moving_line = Effect(name='MovingLine', max_speed=1, std_palette='Rainbow', blend=True)
    brick_breaker = Effect(name='BrickBreaker', max_speed=None, std_palette='Rainbow', blend=True)
    ping_pong = Effect(name='PingPong', max_speed=8, std_palette='Rainbow', blend=False)
    radar = Effect(name='Radar', max_speed=1, std_palette='Rainbow', blend=True)
    checkerboard = Effect(name='Checkerboard', max_speed=1, std_palette='Rainbow', blend=True)
    fireworks = Effect(name='Fireworks', max_speed=1, std_palette='Rainbow', blend=True)
    plasma_cloud = Effect(name='PlasmaCloud', max_speed=3, std_palette='Rainbow', blend=True)
    ripple = Effect(name='Ripple', max_speed=3, std_palette='Rainbow', blend=True)
    snake = Effect(name='Snake', max_speed=3, std_palette='Rainbow', blend=False)
    pacifica = Effect(name='Pacifica', max_speed=3, std_palette='Ocean', blend=True)
    theater_chase = Effect(name='TheaterChase', max_speed=3, std_palette='Rainbow', blend=True)
    plasma = Effect(name='Plasma', max_speed=2, std_palette='Rainbow', blend=True)
    matrix = Effect(name='Matrix', max_speed=8, std_palette=None, blend=False)
    swirl_in = Effect(name='SwirlIn', max_speed=4, std_palette='Rainbow', blend=False)
    swirl_out = Effect(name='SwirlOut', max_speed=4, std_palette='Rainbow', blend=False)
    looking_eyes = Effect(name='LookingEyes', max_speed=None, std_palette=None, blend=False)
    twinkling_stars = Effect(name='TwinklingStars', max_speed=4, std_palette='Ocean', blend=False)
    color_waves = Effect(name='ColorWaves', max_speed=3, std_palette='Rainbow', blend=True)

class transistion_effects(Enum):
    random = 0
    slide = 1
    dim = 2
    zoom = 3
    rotate = 4
    pixelate = 5
    curtain = 6
    ripple = 7
    blink = 8
    reload = 9
    fade = 10

class overlay_effects(Enum):
    clear = "clear"
    snow = "snow"
    rain = "rain"
    drizzle = "drizzle"
    storm = "storm"
    thunder = "thunder"
    frost = "frost"

def main():
    pass

if __name__=="__main__":
    main()