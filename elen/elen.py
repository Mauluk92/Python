from kivy.app import App
from kivy.uix.button import Label
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import NumericProperty,ReferenceListProperty,ObjectProperty
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.graphics import *
import threading 
import pyttsx3 
from kivy.properties import StringProperty
from functools import partial

class MyTestLayout(FloatLayout):
    # Rose Properties 
    
    ## Cromatic Properties
    rgba1_crown = ObjectProperty([1,1,1,1]) # FIRST WHEEL
    rgba2_crown = ObjectProperty([1,1,1,1]) # THIRD WHEEL  
    rgba3_crown = ObjectProperty([1,1,1,1]) # THIRD WHEEL
    rgba4_crown = ObjectProperty([1,1,1,1]) # FIRST WHEEL 
    rgba5_crown = ObjectProperty([1,1,1,1]) # THIRD WHEEL
    rgba6_crown = ObjectProperty([1,1,1,1]) # THIRD WHEEL 
    rgba7_crown = ObjectProperty([1,1,1,1]) # THIRD WHEEL 
    rgba8_crown = ObjectProperty([1,1,1,1]) # FIRST WHEEL
    rgba9_crown = ObjectProperty([1,1,1,1]) # SECOND WHEEL 
    rgba10_crown = ObjectProperty([1,1,1,1])# SECOND WHEEL
    rgba11_crown = ObjectProperty([1,1,1,1])# THIRD WHEEL 
    
    bud_color = ObjectProperty([0,0,0,1])
    rose_color_background = ObjectProperty([0,0,0,0])
    ## Cinematic Properties
    ### Angles 
    angle1= NumericProperty(0)   # BUD 
    angle2 = NumericProperty(0)  # FIRST WHEEL 
    angle3 = NumericProperty(0)  # THIRD WHEEL
    angle4 = NumericProperty(0)  # THIRD WHEEL 
    angle5 = NumericProperty(0)  # FIRST WHEEL 
    angle6 = NumericProperty(0)  # THIRD WHEEL 
    angle7 = NumericProperty(0)  # THIRD WHEEL 
    angle8 = NumericProperty(0)  # THIRD WHEEL 
    angle9 = NumericProperty(0)  # FIRST WHEEL 
    angle10 = NumericProperty(0) # SECOND WHEEL
    angle11 = NumericProperty(0) # SECOND WHEEL
    angle12 = NumericProperty(0) # THIRD WHEEL 
    ### Scaling Factors
    scaling_core = NumericProperty(1)
    scaling = NumericProperty(1)
    scaling_background = NumericProperty(1)
    ### Radial Distance from bud 
    radius_external = NumericProperty(140) #External wheel of petals: distance
    radius_middle = NumericProperty(120)   #Middle wheel of petals: distance
    radius_inside = NumericProperty(100)   #Internal wheel of petals: distance 
    # Elen Properties 
    ## Voice and Engine 
    engine = pyttsx3.init()
    voice = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_IT-IT_ELSA_11.0"
    engine.setProperty('voice', voice)
    ## Writing Board Properties 
    output = StringProperty("")
    output_color= ObjectProperty([1,1,1,1])
    ### Cursor
    cursor_color = ObjectProperty([1,1,1,1])
    cursor_position_x = NumericProperty(0)
    
   
    
    
    
    def __init__(self, **kwarg):
        super(MyTestLayout, self).__init__(**kwarg)
        self.on_start()
        Clock.schedule_interval(self.blink_pointer, 0.5)
        Clock.schedule_once(self.animate_while_speaking, 11)
    def color_crown(self, *largs):
        rgba_silver_wave = [0.192,0.192,0.192,1]
        # Primo giro di petali 
        anim = Animation(rgba1_crown = rgba_silver_wave, duration= 1) + Animation(rgba1_crown = [1,1,1,1], duration = 0.3)
        anim&= Animation(rgba4_crown = rgba_silver_wave, duration=1)+ Animation(rgba4_crown = [1,1,1,1], duration = 0.3)
        anim&= Animation(rgba8_crown = rgba_silver_wave, duration=1)+Animation(rgba8_crown = [1,1,1,1], duration = 0.3)
        # Secondo giro di petali 
       
        anim&= Animation(rgba9_crown = rgba_silver_wave, duration=1)+Animation(rgba9_crown = [1,1,1,1], duration = 0.45)
        anim&= Animation(rgba10_crown = rgba_silver_wave, duration=1)+Animation(rgba10_crown = [1,1,1,1], duration = 0.45)
        # Terzo giro di petali 
        anim&= Animation(rgba5_crown = rgba_silver_wave, duration=1)+Animation(rgba5_crown = [1,1,1,1], duration = 0.5)
        anim&= Animation(rgba2_crown = rgba_silver_wave, duration=1)+Animation(rgba2_crown = [1,1,1,1], duration = 0.5)
        anim&= Animation(rgba3_crown = rgba_silver_wave, duration=1)+Animation(rgba3_crown = [1,1,1,1], duration = 0.5)
        anim&= Animation(rgba6_crown = rgba_silver_wave, duration=1)+Animation(rgba6_crown = [1,1,1,1], duration = 0.5)
        anim&= Animation(rgba7_crown = rgba_silver_wave, duration=1)+Animation(rgba7_crown = [1,1,1,1], duration = 0.5)
        anim&= Animation(rgba11_crown = rgba_silver_wave, duration=1)+Animation(rgba11_crown = [1,1,1,1], duration = 0.5)
        anim.start(self)
    def saluto(self, *largs):
        
        self.text_and_speech("Ciao! Sono Elaine!")
        
    def beating_heart(self,*largs):
        anim = Animation(scaling_core = 0.5, scaling= 1.1, scaling_background=1.1,  duration=0.7, t='in_elastic' )
        anim += Animation(scaling_core = 1, scaling= 1, scaling_background= 1, duration= 0.5, t='out_elastic')
        anim&= Animation(radius_external= 8, radius_middle= 7, radius_inside= 1, duration=0.5, t='in_elastic') + Animation(radius_external=0, radius_middle = 0, radius_inside= 0 ,duration=0.5, t='out_elastic')
        anim.start(self)
    def speak_output(self,output_writing, *largs):
        self.engine.say(output_writing)
        self.engine.runAndWait()
    def text_and_speech(self, output_writing, *largs):
       
        self.write_at_interval(output_writing)
        
       
        Clock.schedule_once(self.rose_fade_out,3.5)
        
    def rose_fade_out(self, *largs):
        anim2 = Animation(scaling_core = 1, scaling= 1, scaling_background= 1, rose_color_background=[0,0,0,0])
        anim2.start(self)
    def animate_while_speaking(self, *largs):
       Clock.schedule_interval(self.beating_heart, 1)
       thread_voice= threading.Thread(target=self.speak_output, args=( "Ciao sono Elaine",), daemon=True)
       thread_voice.start()
       self.saluto()
    def blink_pointer(self,*largs):
        if self.cursor_color ==[1,1,1,1]:
            self.cursor_color = [1,1,1,0]
        else:
            self.cursor_color = [1,1,1,1]
    def write_at_interval(self, output_writing, *largs):
        if output_writing:
            self.output += output_writing[0]
            self.cursor_position_x += 6
            Clock.schedule_once(partial(self.write_at_interval, output_writing[1:]), 0.05)
        else:
            return False
    def on_start(self):
        fade = Animation (bud_color = [1,1,1,1], duration = 0.5, t='in_expo')
        anim = Animation(angle2 = -360, duration= 3)
        anim &= Animation(angle3 = 360, duration=3.5)
        anim &= Animation(angle4 = -360, duration= 3.5)
        anim &= Animation(angle5 = 360, duration = 4)
        anim &= Animation(angle6 = -360, duration=4)
        anim &= Animation(angle7 = 360, duration=4.5)
        anim &= Animation(angle8 = -360, duration=4.5)
        anim &= Animation(angle9 = 360, duration=5)
        anim &= Animation(angle10 = -360, duration=5)
        anim &= Animation(angle11 = 360, duration=5.5)
        anim &= Animation(angle12 = -360, duration=5.5)
        anim &= Animation( radius_inside= 0, radius_middle=0, radius_external=0, duration= 2.5)
        anim+= Animation(angle1= 20, angle2= -340, angle3=+380, angle4=-340, angle5=380, angle6=-340, angle7=+380, angle8 = -340, angle9 = +380, angle10= -340, angle11=380, angle12=-340, t='in_elastic')
        anim+= Animation(angle1=-20, angle2= -380, angle3=340, angle4=-380, angle5=340, angle6=-380, angle7=340, angle8 = -380, angle9=340, angle10=-380, angle11=340, angle12=-380, t='out_elastic')
        anim+= Animation(angle1= 0, angle2= -360, angle3=360, angle4=-360, angle5=360, angle6=-360, angle7=360, angle8=-360, angle9=360, angle10=-360, angle11=360, angle12=-360, t='in_elastic') 
        anim.start(self)
        fade.start(self)
class MyLayoutApp(App):
    def build(self):
        return MyTestLayout()
 
if __name__ == "__main__":
    end_utterance = False 
    
    
    MyLayoutApp().run()
    

