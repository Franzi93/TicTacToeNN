# -*- coding: utf-8 -*-
"""
Created on Tue Dec 22 11:26:56 2015

@author: Ralf Engelken, Franziska Neu
"""

import numpy as np
from MLP import MLP
from Bot_Random import Bot
import json
import time

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
        self.version = 1
        self.counter = 0
        self.optimization = []
        self.reward = reward[:]
        self.first_action = True
        self.beta = beta
        #hoher Wert für beta (50?): exploitation
        #niedriger Wert für beta  : exploration

        self.mlp = MLP (size_x * size_y, hidden, size_x * size_y, learning_rate)

        self.new_game()

    """
    Initializes a new game    
    """
    def new_game(self):
        self.first_action = True
        self.counter += 1
        self.mlp.new_game()
        #self.info = world.get_sensor_info()
        #self.h = self.mlp.get_action_without_activation(self.info)
        
        #self.act = self.rand_winner (self.h, self.beta)
        #act_vec = numpy.zeros (size_mot)
        #act_vec[act] = 1.0
        #self.q0 = self.h[self.act]
        
    """
    Loads
    """
    def load_data(self, filename):
        fo = open(filename , "r")
        data = json.loads(fo.read())
        fo.close()

        if (data["bot"] == self.bot_name):
            if (data["version"] <= self.version):
                self.counter      = data["counter"]
                self.optimization = data["optimization"]
                self.reward       = data["reward"]
                self.first_action = data["first_action"]
                self.beta         = data["beta"]
                self.mlp.set_data(data["MLP"])
            else:
                raise ValueError('dataset is not usable by Bot : different Bot identifier') 
        else:
            raise ValueError('dataset is not usable by this Bot version : dataset version is higher than Bot version') 

        return data
        
    """
    Saves
    """
    def save_data(self, filename):
        data = {"bot"          : self.bot_name,
                "version"      : self.version,

                "counter"      : self.counter,
                "optimization" : self.optimization,
                "reward"       : self.reward,
                "first_action" : self.first_action,
                "beta"         : self.beta,
                "MLP"          : self.mlp.get_data()}

        fo = open(filename , "w")
        fo.write(json.dumps(data))
        fo.close()        
        
    """
    Returns an action depending on the given world
    """
    def get_action(self, world_old):
        self.info_tic = world_old.get_sensor_info()
        self.h_tic = self.mlp.get_action(self.info_tic)
        
        #for i in range(len(self.h_tic)):
        #    if (self.info_tic[i] > 0):
        #        self.h_tic[i] = -100000

        #Workaround: Wenn nur noch 1 Zug möglich ist, automatisch setzen
        moves = world_old.get_moves()
        if (len(moves) == 1):
            self.act_tic = moves[0]
        else:
            #Auswahl wiederholen bis ein gültiger Zug ausgewählt wurde        
            validation = False
            while (validation == False):
                new_h_tic = []
                for i in range(len(self.h_tic)):
                    if (i in moves):
                        new_h_tic.append(self.h_tic[i])
                
                self.act_tic = moves[self.rand_winner (new_h_tic, self.beta)]     # choose action
                #print self.info, self.act
                #print "----------\n",self.h_tic, "\n",moves, "\n",new_h_tic, "\n",self.act_tic
                x = self.act_tic % world_old.size_x
                y = self.act_tic / world_old.size_y
                validation = world_old.check_action(x, y)

        #Umrechnen 1D -> 2D
        x = self.act_tic % world_old.size_x
        y = self.act_tic / world_old.size_y
        
        #print "--------------------------"
        #print self.h, "->", self.act, "->", x, ",", y
        #print "--------------------------"
        return (x, y)
        
    """
    Adapts the MLP considering the results (world_new) of its last action
    """
    def evaluate_action(self, world_new):
        if (self.first_action == False):
            r = self.get_reward(world_new.get_winner())         # read reward

            #Erstellen des Aktions-Vektors        
            act_vec = np.zeros (self.mlp.input_size)
            act_vec[self.act_tic] = 1.0
    
            #Berechnen der Q-Werte vor und nach der Aktion
            q0 = self.h[self.act]
            q1 = self.mlp.get_action(world_new.get_sensor_info())[self.act_tic]
    
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
            self.mlp.evaluate_action_RL(self.info, error)
            
            #print q0, q1, delta
        
        self.info = self.info_tic
        self.h = self.h_tic
        self.act = self.act_tic
        self.first_action = False

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