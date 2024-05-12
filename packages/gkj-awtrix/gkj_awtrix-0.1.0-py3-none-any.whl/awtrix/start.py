import awtrix.icons as ic
import awtrix.device as dev
import awtrix.display as display
import awtrix.effects as ef


def hello():
    print("Hello")
    
    display.icon_text(text="SPARGELMARKT", icon=ic.Icons.spring_flowers_animation.value, duration = 20, name='spargelmarkt')
    display.icon_text( 
                      text="GERMANY 10 POINTS", 
                      icon=ic.Icons.germany_wave.value, 
                      duration = 20, 
                      use_icon_file=False,
                      effect_in=ef.effects.brick_breaker,
                      effect_out=ef.effects.ripple,
                      name='esc'
                      )
    display.icon_text( 
                      text="VIEL SPASS BEIM PINO", 
                      icon=ic.Icons.pizza_animation.value, 
                      duration = 20, 
                      use_icon_file=False,
                      effect_in=ef.effects.ping_pong,
                      effect_out=ef.effects.plasma_cloud,
                      lifetime = 7200,
                      name='pizza_pino'
                      )



def main():
    pass

if __name__=="__main__":
    main()