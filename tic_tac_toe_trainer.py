#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 16:33:00 2015

@author: Ralf Engelken, Franziska Neu
"""
import matplotlib.pyplot as plt
from World_Model import World_Model
import Bot_Random
from Bot_RL_MLP_SARSA import Bot_RL_MLP

#Game Parameters
size_x     = 3          #The x-dimension of the board
size_y     = 3          #The y-dimension of the board
size_win   = 3          #The number of stones in a row neccessary to win
gravity    = False      #True : only the x-position is used, the stones always fall down to the bottom-most empty field
initial_stones = 2     #the number of stones already on the field

#RL and MLP Parameters
rl_reward = [0.0, -1.0, 1.0]    #rewards for : Draw, Win, Loose
rl_beta = 2                     #bot_RL_MLP so ca. 1 - 5
mlp_hidden = 10                 #number of hidden neurons
mlp_learning_rate = 0.1         #learning-rate of the MLP

#Misc Parameters
runs          = 10000000      #the number of runs
log_interval  = 1000          #print status every x runs
save_interval = 1000
save_filename = "b" + str(initial_stones) + ".dat"
draw_graph    = False


world = World_Model (size_x, size_y, size_win, gravity, initial_stones = initial_stones)
sensor = world.get_sensor_info()
f = [0]*len(sensor)
for i in range(len(sensor)):
    f[i] = sensor[i]

#Choose Bots
bot_RL = Bot_RL_MLP(size_x, size_y, rl_beta, mlp_hidden, mlp_learning_rate, rl_reward, initial_field = f, player_ID = 1)
bot_train = Bot_Random.Bot_Random_Static(size_x, size_y)
#bot_train = Bot_Random.Bot_Random_Dynamic(size_x, size_y)

win    = [[],[],[]]
scale  = []
winner = [0,0,0]

for counter in range (runs):
    bot_RL.play_game(world, 1, bot_train)
    #bot_1.new_game()
    #bot_2.new_game()
    #Play a game
    #Make a move until Game ends
    #world.new_init(initial_stones = initial_stones)
    #while (world.get_winner() == -1):
    #    if (world.active_player == 1):
    #        (x, y) = bot_1.get_action(world)
    #        world.perform_action(x, y)            
    #        bot_1.evaluate_action(world)
    #    else:
    #        (x, y) = bot_2.get_action(world)
    #        world.perform_action(x, y)
    #        bot_2.evaluate_action(world)

    #Evaluate Game
    winner[int(world.get_winner())] += 1
    if ((counter % log_interval) == log_interval - 1):

        print 'W_i min :',bot_RL.mlp.W_i.min(), '     W_i max :', bot_RL.mlp.W_i.max()
        print 'W_o min :',bot_RL.mlp.W_o.min(), '     W_o max :', bot_RL.mlp.W_o.max()
    
        if (draw_graph == True):
            win[0].append(winner[0])        
            win[1].append(winner[1])
            win[2].append(winner[2])
            scale.append(counter)
            plt.plot(scale, win[0], label='Draw')
            plt.plot(scale, win[1], label='Win')
            plt.plot(scale, win[2], label='Lose')
            plt.legend(loc='lower left')
            plt.show()
        
        #bot_1.load_data("data_loose")
        
        print 'counter   :', counter+1, '     [draw, won, lost] :', winner
        winner = [0,0,0]
        
    if ((counter % save_interval) == save_interval - 1):
        bot_RL.save_data(save_filename)        
    
    #print 'counter   :', counter, '   steps :', steps, '     wins :', winner_1
    #print "-----", counter, "-----"
    #print world.get_winner()
    #world.print_world()
    #print 'winner :', world.get_winner(), '\n'