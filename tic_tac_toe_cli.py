#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 16:33:00 2015

@author: Ralf Engelken, Franziska Neu
"""

from World_Model import World_Model
import Bot_Random
from Bot_RL_MLP import Bot_RL_MLP

#Game Parameters
size_x     = 3          #The x-dimension of the board
size_y     = 3          #The y-dimension of the board
size_win   = 3          #The number of stones in a row neccessary to win
gravity    = False      #True : only the x-position is used, the stones always fall down to the bottom-most empty field
initial_stones = 1      #the number of stones already on the field

#RL and MLP Parameters
rl_reward = [0.0, 1.0, -1.0]    #rewards for : Draw, Win, Loose
rl_beta = 1                     #bot_RL_MLP so ca. 1 - 5
mlp_hidden = 10                 #number of hidden neurons
mlp_learning_rate = 0.3         #learning-rate of the MLP

#Misc Parameters
runs = 100000               #the number of runs
display_progress = 1000     #print status every x runs

#Choose Bots
bot_1 = Bot_RL_MLP(size_x, size_y, rl_beta, mlp_hidden, mlp_learning_rate, rl_reward)
bot_2 = Bot_Random.Bot_Random_Static(size_x, size_y)
#bot_2 = Bot_Random.Bot_Random_Dynamic(size_x, size_y)



world = World_Model (size_x, size_y, size_win, gravity, initial_stones = initial_stones)

print 'W_i min :',bot_1.mlp.W_i.min(), '     W_i max :', bot_1.mlp.W_i.min()
print 'W_o min :',bot_1.mlp.W_o.min(), '     W_o max :', bot_1.mlp.W_o.min()
        
winner = [0,0,0]
for counter in range (runs):
    
    #Play a game
    #Make a move until Game ends
    world.new_init(initial_stones = initial_stones)
    while (world.get_winner() == -1):
        if (world.active_player == 1):
            (x, y) = bot_1.get_action(world)
            world.perform_action(x, y)            
            bot_1.evaluate_action(world)
        else:
            (x, y) = bot_2.get_action(world)
            world.perform_action(x, y)
            bot_2.evaluate_action(world)

    #Evaluate Game
    winner[int(world.get_winner())] += 1
    if ((counter % display_progress) == display_progress - 1):
        print 'counter   :', counter+1, '     [draw, won, lost] :', winner
        print 'W_i min :',bot_1.mlp.W_i.min(), '     W_i max :', bot_1.mlp.W_i.min()
        print 'W_i min :',bot_1.mlp.W_o.min(), '     W_i max :', bot_1.mlp.W_o.min()
        winner = [0,0,0]
    
    #print 'counter   :', counter, '   steps :', steps, '     wins :', winner_1
    #print "-----", counter, "-----"
    #print world.get_winner()
    #world.print_world()
    #print 'winner :', world.get_winner(), '\n'

bot_1.save_data("data")