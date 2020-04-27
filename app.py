from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import (ObjectProperty, NumericProperty, ReferenceListProperty)
from kivy.clock import Clock
from kivy.vector import Vector
from kivy.uix.image import Image
from kivy.config import Config
Config.set('graphics', 'width', '1299')
Config.set('graphics', 'height', '616')

import numpy as np
import cv2 

def init():
    global sand
    global width
    global height
    global sensor1
    global sensor2
    global sensor3

    width = 1299
    height = 616

    # Load the mask image, resize it to width x height and convert it to gray scale
    sand = cv2.imread('mask.jpeg',0)
    sand = np.squeeze(sand)/255

class Brain():


class Car(Image):
    velocity_x = NumericProperty(1.0)
    velocity_y = NumericProperty(1.0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)
    angle = NumericProperty(1)
    rotation = NumericProperty(2.0)

    def move(self,rotation=0):
        """ 
            - It was very problematic to move the widget itself so i am moving the Image instead
            - the rotate function is inherent to the Vector class and will rotate the direction at which the
            car moves and make sure the car only goes in the direction it points to. No backward motion
        """
        self.angle = (self.angle+rotation)%360
        self.rotation = rotation
        self.pos = Vector(*self.velocity).rotate(self.angle-45) + self.pos

class Ball1(Widget):
    pass

class Ball2(Widget):
    pass

class Ball3(Widget):
    pass


class Map(Widget):
    za_car = ObjectProperty(None)
    za_ball_1 = ObjectProperty(None)
    za_ball_2 = ObjectProperty(None)
    za_ball_3 = ObjectProperty(None)
    actions = [0, 5, -5]

    def update(self,_):
        global sand
        global height
        global width
        global sensor1, sensor2, sensor3

        # Make sure the car avoids going to the horizon


        self.size = Vector(width,height)
        prob = np.random.uniform(0,1) 
        if prob <= 0.2:
            rotation = self.actions[1]
        elif prob >= 0.8:
            rotation = self.actions[2]
        else:
            rotation = self.actions[0]
        self.za_car.move(rotation)


        # Setting the position of the ball
        self.za_ball_1.pos =  Vector(*self.za_car.pos) + Vector(40.0,0).rotate(self.za_car.angle)
        self.za_ball_2.pos =  Vector(*self.za_car.pos) + Vector(40.0,0).rotate((self.za_car.angle+30)%360)
        self.za_ball_3.pos =  Vector(*self.za_car.pos) + Vector(40.0,0).rotate((self.za_car.angle-30)%360)


        # Getting the sensor values
        box_range_x = np.arange(-10,10)
        box_range_y = np.arange(-10,10)
        sensor1 = sand[(self.za_ball_1.y + box_range_y).astype(np.int)*-1, (self.za_ball_1.x+box_range_x).astype(np.int)].sum()/400
        sensor2 = sand[(self.za_ball_2.y + box_range_y).astype(np.int)*-1, (self.za_ball_2.x+box_range_x).astype(np.int)].sum()/400
        sensor3 = sand[(self.za_ball_3.y + box_range_y).astype(np.int)*-1, (self.za_ball_3.x+box_range_x).astype(np.int)].sum()/400

        if self.za_car.x < 50.0:
            self.za_car.x = 50.0
            self.za_car.angle += 40

        if self.za_car.x > (width-50.0):
            self.za_car.x = width-50.0
            self.za_car.angle += 40

        if self.za_car.y < 50.0:
            self.za_car.y = 50.0
            self.za_car.angle += 40

        if self.za_car.y > (height - 50.0):
            self.za_car.y = height - 50.0
            self.za_car.angle += 40
            print(sensor1,sensor2,sensor3)
         

class MyApp(App):
    def build(self):
        init()
        game_map = Map()
        Clock.schedule_interval(game_map.update,1.0/60)
        return game_map

if __name__ == "__main__":
    MyApp().run()
