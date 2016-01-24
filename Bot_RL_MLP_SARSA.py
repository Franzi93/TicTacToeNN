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
    def __init__ (self, size_x = 3, size_y = 3, beta = 1, hidden = 20, learning_rate = 0.1, reward = [0, 1.0, -1.0], initial_field = [0], player_ID = 1):
        Bot.__init__(self)
        
        self.initial_field = initial_field
        self.player_ID = player_ID

        self.bot_name = "Bot_RL_MLP"
        self.version = 2.0
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
        
    """
    Loads
    """
    def load_data(self, filename):
        fo = open(filename , "r")
        data = json.loads(fo.read())
        fo.close()

        if (data["bot"] == self.bot_name):
            if (data["version"] <= self.version):
                self.player_ID    = data["player_ID"]
                self.initial_field = data["initial_field"]
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

                "player_ID"    : self.player_ID,
                "initial_field" : self.initial_field,
                "counter"      : self.counter,
                "optimization" : self.optimization,
                "reward"       : self.reward,
                "first_action" : self.first_action,
                "beta"         : self.beta,
                "MLP"          : self.mlp.get_data()}

        fo = open(filename , "w")
        fo.write(json.dumps(data))
        fo.close()        
        
    def play_game(self, world, player, train_bot):
        world.new_init()
        self.mlp.new_game()

        I = world.get_sensor_info()
        #h = np.dot (w_mot, I)
        hidden, h = self.mlp.get_action(I)
        act = self.rand_winner (h, self.beta)                         # choose action
        act_vec = np.zeros (self.mlp.output_size)
        act_vec[act] = 1.0
        
        #val = numpy.dot (w_mot[act], I)                     # value before action
        #val is q0 ***
        val = h[act]                                         # value before action

        r = 0
   
        #while r == 0:
        while (world.get_winner() < 0):
            if (world.active_player != player):
                (x, y) = train_bot.get_action(world)
                world.perform_action(x, y)  
            else:
                x = act % world.size_x
                y = act / world.size_y
                world.perform_action(x, y)                      # do selected action
                
                if (world.get_winner() < 0):
                    (x, y) = train_bot.get_action(world)
                    world.perform_action(x, y)
                    
                r = self.get_reward(world.get_winner())         # read reward
                I_tic = world.get_sensor_info()                 # read new state
        
                #numpy.dot (w_mot, I_tic)
                hidden_tic, h_tic = self.mlp.get_action(I_tic)
                act_tic = self.rand_winner (h_tic, self.beta)                 # choose next action
        
                act_vec = np.zeros (self.mlp.output_size)
                act_vec[act] = 1.0
        
                #val_tic = numpy.dot (w_mot[act_tic], I_tic)     # value after action
                #val_tic is q1 ***
                val_tic = h_tic[act_tic]    
        
                if  r == 1.0:                                   # This is cleaner than defining
                    target = r                                  # target as r + 0.9 * val_tic,
                else:                                           # because weights now converge.
                    target = 0.9 * val_tic                      # gamma = 0.9
                delta = target - val                            # prediction error
        
                #w_mot += 0.5 * delta * numpy.outer (act_vec, I)
                error = np.zeros (self.mlp.output_size)
                error[act] = delta
                #print error
                
                #Lernen ***
                self.mlp.evaluate_action_RL(h, hidden, error)
        
                I = I_tic
                val = val_tic
                act = act_tic 
                hidden = hidden_tic

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