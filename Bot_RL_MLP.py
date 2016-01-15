# -*- coding: utf-8 -*-
"""
Created on Tue Dec 22 11:26:56 2015

@author: Ralf Engelken, Franziska Neu
"""

import numpy as np
import json_tricks
import time
from MLP import MLP
from Bot_Random import Bot


"""
Implements a Bot using Reinforced Learning in Combination with a MLP to learn playing games

The action is chosen using the world (get_action)
The learning takes place in evaluate_action, where the result of the action (world_new) is compared to the
expected result
"""
class Bot_RL_MLP (Bot):
    def __init__ (self, size_x, size_y, beta, hidden, learning_rate, reward):
        Bot.__init__(self)
        self.bot_name = "Bot_RL_MLP"

        self.mlp = MLP (size_x * size_y, hidden, size_x * size_y, learning_rate)

        self.reward = reward[:]

        #hoher Wert für beta (50?): exploitation
        #niedriger Wert für beta  : exploration
        self.beta = beta
        
    """
    Returns an action depending on the given world
    """
    def get_action(self, world):
        self.info = world.get_sensor_info()
        self.h = self.mlp.get_action(self.info)
        
        for i in range(len(self.h)):
            if (self.info[i] > 0):
                self.h[i] = -10

        #Workaround: Wenn nur noch 1 Zug möglich ist, automatisch setzen
        moves = world.get_moves()
        if (len(moves) == 1):
            self.act = moves[0]
        else:
            #Auswahl wiederholen bis ein gültiger Zug ausgewählt wurde        
            validation = False
            while (validation == False):
                self.act = self.rand_winner (self.h, self.beta)     # choose action
                #print self.info, self.act
                x = self.act % world.size_x
                y = self.act / world.size_y
                validation = world.check_action(x, y)

        #Umrechnen 1D -> 2D
        x = self.act % world.size_x
        y = self.act / world.size_y
        
        #print "--------------------------"
        #print self.h, "->", self.act, "->", x, ",", y
        #print "--------------------------"
        return (x, y)
        
    """
    Adapts the MLP considering the results (world_new) of its last action
    """
    def evaluate_action(self, world_new):
        #Erstellen des Aktions-Vektors        
        act_vec = np.zeros (self.mlp.input_size)
        act_vec[self.act] = 1.0

        #Berechnen der Q-Werte vor und nach der Aktion
        q0 = self.h[self.act]
        q1 = self.mlp.get_action(world_new.get_sensor_info())[self.act]

        #Berechnen der Belohnung auf dem neuen Feld
        r = self.get_reward(world_new.get_winner())         # read reward
        if  (r == self.get_reward(1)):                      # This is cleaner than defining
            target = r                                      # target as r + 0.9 * q1,
        else:                                               # because weights now converge.
            target = 0.9 * q1                               # gamma = 0.9
        delta = target - q0                                 # prediction error

        #Wichtig : nur das delta an der Position der Aktion wird als Fehler betrachtet, für alle anderen
        #Positionen ist der Fehler 0
        error = np.zeros (self.mlp.input_size)
        error[self.act] = delta
        
        #Wichtig : Das Lernen erfolgt mittels des Fehlers und der Welt VOR der Aktion        
        self.mlp.evaluate_action(self.info, error)

    """
    Selects an action
    """
    def rand_winner (self, S_from, beta):
        #for i in range (len(S_from)):
        #    if S_from[i] > 200:
        #        print S_from
        #        time.sleep(0.2)
        #print "--------------------\n",S_from
        #time.sleep(0.2)
        sum = 0.0
        p_i = 0.0
        rnd = np.random.random()
        d_r = len (S_from)
        sel = 0
    
        try:
            for i in range (d_r):
                sum += np.exp (beta * min(S_from[i],200))
            
            #if field is empty, set reward to 1 for all fields
            #to get a probablity higher than 0
            if (sum == 0):
                sum = d_r
                S_from = [1]*d_r
                
            for i in range (d_r):
                p_i += np.exp (beta * min(S_from[i],200)) / sum
        
                if  p_i > rnd:
                    sel = i
                    rnd = 1.1 # out of reach, so the next will not be turned ON
                    
        except Exception:
            print beta, S_from[i], S_from, sum
        return sel        
        
    """
    Calculates the reward for the actual board setup
    """
    def get_reward (self, winner):
        if  ((winner >= 0) and (winner <= 2)):
            return self.reward[int(winner)]
        else:
            return 0.0
            
    """
    Loads 
    """
    #def load_data(self, filename):
    #    fo = open(filename , "r")
    #    #self.w_mot = json_tricks.load(fo.read())["w_mot"]
    #    data = json_tricks.load(fo.read())
    #    fo.close()            
    #    
    #    return data
         
    """
    Saves
    """
    #def save_data(self, filename):
    #    data = {"bot" : "Bot_RL_MLP", 
    #            "version" : 1,
    #            "mlp" : self.mlp}
    #    fo = open(filename , "w")
    #    fo.write(json_tricks.dumps(data))
    #    fo.close()