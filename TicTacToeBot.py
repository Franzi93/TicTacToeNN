#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 16:33:00 2015

@author: Ralf Engelken, Franziska Neu
"""

from World_Model import World_Model
import Bot_Random
from Bot_RL_MLP import Bot_RL_MLP
import numpy as np

class TicTacToeBot:
    
    def __init__(self):
        #Game Parameters
        self.size_x     = 3          #The x-dimension of the board
        self.size_y     = 3          #The y-dimension of the board
        self.size_win   = 3          #The number of stones in a row neccessary to win
        self.gravity    = False      #True : only the x-position is used, the stones always fall down to the bottom-most empty field
        self.initial_stones = 2      #the number of stones already on the field
        
        #RL and MLP Parameters
        self.rl_reward = [0.0, 1.0, -1.0]    #rewards for : Draw, Win, Loose
        self.rl_beta = 3                     #bot_RL_MLP so ca. 1 - 5
        self.mlp_hidden = 10                 #number of hidden neurons
        self.mlp_learning_rate = 0.1         #learning-rate of the MLP
        
        #Choose Bots
        self.bot_1 = Bot_RL_MLP(self.size_x, self.size_y, self.rl_beta, self.mlp_hidden, self.mlp_learning_rate, self.rl_reward)
        
        self.world = World_Model (self.size_x, self.size_y, self.size_win, self.gravity, initial_stones = self.initial_stones)
        
    def train(self, runs):
        bot_2 = Bot_Random.Bot_Random_Static(3, 3)
        
        for counter in range (runs):
            #Play a game
            self.world.new_init(initial_stones = self.initial_stones)
            
            #Make a move until Game ends
            while (self.world.get_winner() == -1):
                if (self.world.active_player == 1):
                    (x, y) = self.bot_1.get_action(self.world)
                    self.world.perform_action(x, y)            
                    self.bot_1.evaluate_action(self.world)
                else:
                    (x, y) = bot_2.get_action(self.world)
                    self.world.perform_action(x, y)
                    bot_2.evaluate_action(self.world)

    def get_action(self, sensor_info):
        field = np.zeros(9)
        for i in range(len(sensor_info)):
            field[i] = sensor_info[i]
        self.world.field = field
        (x, y) = self.bot_1.get_action(self.world)
        return (x, y)