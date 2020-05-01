""" This module houses all the kivy related stuff """

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
    global width, height
    global sensor1, sensor2, sensor3
    global goal_x, goal_y
    global last_distance, last_reward
    global box_range_x, box_range_y

    width = 1299
    height = 616

    # Load the mask image, resize it to width x height and convert it to gray scale
    sand = cv2.imread('mask.jpeg',0)
    sand = np.squeeze(sand)/255

    goal_x = 1000
    goal_y = 400

    last_distance = (goal_x) ** 2 + (goal_y) ** 2
    last_reward = 0

    box_range_x = np.arange(-10,10)
    box_range_y = np.arange(-10,10)


class Car(Image):
    velocity_x = NumericProperty(2.0)
    velocity_y = NumericProperty(0.0)
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
        self.pos = Vector(*self.velocity).rotate(self.angle) + self.pos

class Ball1(Widget):
    pass

class Ball2(Widget):
    pass

class Ball3(Widget):
    pass

def get_random_action():
    prob = np.random.uniform(0,1)
    if prob <= 0.2:
        return 1
    elif prob >= 0.8:
        return 2
    else:
        return 0

class Map(Widget):
    za_car = ObjectProperty(None)
    za_ball_1 = ObjectProperty(None)
    za_ball_2 = ObjectProperty(None)
    za_ball_3 = ObjectProperty(None)
    actions = [0, 5, -5]

    def update(self,_):
        global sand
        global height, width
        global sensor1, sensor2, sensor3
        global goal_x, goal_y
        global distance, last_reward, last_distance
        global box_range_x, box_range_y

        xx = goal_x - self.za_car.x
        yy = goal_y - self.za_car.y
        
        orientation = Vector(*self.za_car.velocity).angle((xx,yy))/180.0

        
        # Getting the sensor values
        sensor1 = sand[(self.za_ball_1.y + box_range_y).astype(np.int)*-1, (self.za_ball_1.x+box_range_x).astype(np.int)].sum()/400
        sensor2 = sand[(self.za_ball_2.y + box_range_y).astype(np.int)*-1, (self.za_ball_2.x+box_range_x).astype(np.int)].sum()/400
        sensor3 = sand[(self.za_ball_3.y + box_range_y).astype(np.int)*-1, (self.za_ball_3.x+box_range_x).astype(np.int)].sum()/400

        last_signal = [sensor1, sensor2, sensor3, orientation, -orientation]

        # Here 
        # Update the ai 
        # get the action
        action = get_random_action()
        self.za_car.move(self.actions[action])
        # Move the car based on the action

        # Based on your action, get the absolute distance from your goal
        distance = (self.za_car.x - goal_x) ** 2 + (self.za_car.y-goal_y) ** 2

        # Now check if the car is on the road or not and then give reward based on it
        if sand[-int(self.za_car.center_y), int(self.za_car.center_x)] > 0:
            self.za_car.velocity = Vector(0.5,0)
            print(1,distance)
            last_reward = -1.0
        else:
            self.za_car.velocity = Vector(2.0,0)
            print(0,distance)
            last_reward = -0.1
            if distance < last_distance:
                last_reward = 0.1

       
        # Setting the position of the ball
        self.za_ball_1.pos =  Vector(*self.za_car.pos) + Vector(40.0,0).rotate(self.za_car.angle)
        self.za_ball_2.pos =  Vector(*self.za_car.pos) + Vector(40.0,0).rotate((self.za_car.angle+30)%360)
        self.za_ball_3.pos =  Vector(*self.za_car.pos) + Vector(40.0,0).rotate((self.za_car.angle-30)%360)



        if self.za_car.x < 50.0:
            self.za_car.x = 50.0
            self.za_car.angle += 40
            last_reward = -1

        if self.za_car.x > (width-50.0):
            self.za_car.x = width-50.0
            self.za_car.angle += 40
            last_reward = -1

        if self.za_car.y < 50.0:
            self.za_car.y = 50.0
            self.za_car.angle += 40
            last_reward = -1

        if self.za_car.y > (height - 50.0):
            self.za_car.y = height - 50.0
            self.za_car.angle += 40
            last_reward = -1
         

class MyApp(App):
    def build(self):
        init()
        game_map = Map()
        Clock.schedule_interval(game_map.update,1.0/60)
        return game_map

if __name__ == "__main__":
    MyApp().run()
