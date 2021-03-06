# -*- coding: utf-8 -*-
"""
Created on Tue Dec 22 11:43:54 2015

@author: Ralf Engelken, Franziska Neu
"""

import random

class Bot:
    info = None
    
    def __init__(self):
        self.bot_name = "Bot"
        pass
    
    def new_game(self):
        pass
    
    def get_action(self, world):
        x = 0
        y = 0
            
        return (x, y)
        
    def evaluate_action(self, world_new):
        pass
    
    """
    Loads 
    """
    def load_data(self, filename):
        raise NotImplementedError
         
    """
    Saves
    """
    def save_data(self, filename):
        raise NotImplementedError
      
"""
On Generatino, this bot generates a random order in which he places stones on the field.
Afterwards, he always places a stone on the first free field in this order
"""
class Bot_Random_Static (Bot):
    def __init__(self, size_x, size_y):
        Bot.__init__(self)   
        self.bot_name = "Bot_Random_Static"
        
        #Generate random order 
        self.order = []
        for i in range(size_x * size_y):
            self.order.append(i)
        random.shuffle(self.order)
        
    def get_action(self, world):
        i = 0
        act = self.order[i]
        x = act % world.size_x
        y = act / world.size_y  
        
        while (world.check_action(x, y) == False):
            i += 1
            act = self.order[i]
            x = act % world.size_x
            y = act / world.size_y  
            
        x = act % world.size_x
        y = act / world.size_y   
        return (x, y)      
      
"""
This bot always places a stone on a random field 
"""
class Bot_Random_Dynamic (Bot):
    def __init__(self, size_x, size_y):
        Bot.__init__(self)
        self.bot_name = "Bot_Random_Dynamic"
    
    def get_action(self, world):
        if (world.get_sensor_info() == None):
            x = 0
            y = 0
        else:
            x = random.randint(0, world.size_x - 1)
            y = random.randint(0, world.size_y - 1)
            
        return (x, y)