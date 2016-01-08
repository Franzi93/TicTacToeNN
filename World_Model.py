# -*- coding: utf-8 -*-
"""
Created on Tue Dec 22 11:16:29 2015

@author: Ralf Engelken, Franziska Neu
"""

import numpy as np

"""
Implements a tic-tac-toe game0
"""
class World_Model:
    stone_order = [[2,2],[1,2],[2,1],[1,1],[0,0],[0,1],[1,0],[0,2],[2,0]]
    
    """
    Initialize a new world of size size_x * size_y
    """
    def __init__(self, size_x = 3, size_y = 3, size_win = 3, gravity = False, initial_stones = 0):
        # init input position
        self.size_x = size_x        #The x-dimension of the board
        self.size_y = size_y        #The y-dimension of the board
        self.size_win = size_win    #The number of stones in a row neccessary to win
        self.gravity = gravity      #True : only the x-position is used, the stones always fall down to the bottom-most emtpy field
                                    #False: the stone is positioned on the given x-y-position
        
        self.new_init(initial_stones)
        self.print_world()

    """
    Reset the world and place the given number of stones following a fixed pattern
    """
    def new_init(self, initial_stones = 0):
        self.field = np.zeros(self.size_x * self.size_y)     #field array holds positions of placed stones
        self.active_player = 1                               #1 or 2
        
        #Place the given number of stones
        for i in range(initial_stones):
            self.perform_action(self.stone_order[i][0], self.stone_order[i][1])
       
    """
    Place a stone on position pos_x, pos_y
    """
    def perform_action(self, pos_x, pos_y):
        #4-wins mode
        if (self.gravity == True):
            if (pos_x >= 0 and pos_x < self.size_x):
                pos_y = 0
                pos = self.__2D_to_1D (pos_x,pos_y)
                if (self.field[pos] == 0):
                    while ((pos_y < self.size_y - 1) and (self.field[self.__2D_to_1D (pos_x, pos_y + 1)] == 0)):
                        pos_y += 1
                    
                    pos = self.__2D_to_1D (pos_x,pos_y)
                    self.field[pos] = self.active_player
                    self.active_player = 3 - self.active_player
                else:
                    pass#print 'column is full'
            else:
                pass#print 'illegal position'
        #Tic-Tac-Toe mode
        else:
            if (pos_x >= 0 and pos_x < self.size_x and pos_y >= 0 and pos_y < self.size_y):
                pos = self.__2D_to_1D (pos_x,pos_y)
                if (self.field[pos] == 0):
                    self.field[pos] = self.active_player
                    self.active_player = 3 - self.active_player
                else:
                    pass#print 'field is not empty'
            else:
                pass#print 'illegal position'

    """
    Checks if the given action is valid
    """
    def check_action(self, pos_x, pos_y):
        erg = (self.field[self.__2D_to_1D(pos_x, pos_y)] == 0)
        #print "(", pos_x, ",", pos_y, ")",f, erg
        return erg

    """
    Check for a winner
    returns -1   : no winner
            0    : draw
            1,2  : player X won the game
    """
    def get_winner(self):
        #check if a player has 3 in a row; return player-ID or 0
        result = -1
        counter = 0
        x = 0
        y = 0
        
        #Iterate over all fields
        while ((result == -1) and (y < self.size_y)):
            field = self.field[self.__2D_to_1D(x,y)]
            #Check if field contains a stone            
            if (field > 0):
                counter += 1
                
                #Check if a horizontal winning condition is met (x,y) to (x+1,y) ...
                if (x <= self.size_x - self.size_win):
                    max = 1
                    for i in range(1, self.size_win):
                        if (field == self.field[self.__2D_to_1D(x+i,y)]):
                            max += 1
                    if (max == self.size_win):
                        result = field
    
                #Check if a vertical winning condition is met (x,y) to (x,y+1) ...
                if (y <= self.size_y - self.size_win):
                    max = 1
                    for i in range(1, self.size_win):
                        if (field == self.field[self.__2D_to_1D(x,y+i)]):
                            max += 1
                    if (max == self.size_win):
                        result = field  
                        
                #Check if a diagonal winning condition is met (x,y) to (x+1,y+1) ...
                if ((x <= self.size_x - self.size_win) and (y <= self.size_y - self.size_win)):
                    max = 1
                    for i in range(1, self.size_win):
                        if (field == self.field[self.__2D_to_1D(x+i,y+i)]):
                            max += 1
                    if (max == self.size_win):
                        result = field
                        
                #Check if a diagonal winning condition is met (x,y) to (x+1,y-1) ...
                if ((x <= self.size_x - self.size_win) and (y >= self.size_win - 1)):
                    max = 1
                    for i in range(1, self.size_win):
                        if (field == self.field[self.__2D_to_1D(x+i,y-i)]):
                            max += 1
                    if (max == self.size_win):
                        result = field
                        
            #Proceed to next field    
            x += 1            
            if (x >= self.size_x):
                x = 0
                y += 1            
            
        #Check if all fields are occupied without a winner
        if ((result == -1) and (counter == len(self.field))):
            result = 0

        return result

    """
    Returns the actual board setup
    """            
    def get_sensor_info(self):
        return self.field[:]
        
    """
    Returns the possible moves in 1D-coordinates
    """
    def get_moves(self):
        moves = []
        for i in range(len(self.field)):
            if (self.field[i] == 0):
                moves.append(i)
                
        return moves
        
    """
    Prints the actual board to the screen
    """
    def print_world(self):
        for y in range(self.size_y):
            s = ''
            for x in range(self.size_x):
                if (x < self.size_x - 1):
                    s += ' ' + str(self.field[self.__2D_to_1D(x,y)]) + ' |'
                else:
                    s += ' ' + str(self.field[self.__2D_to_1D(x,y)])
            print s
        
    """
    Converts the x,y-position in a 2D-array to the position in a corresponding 1D-array
    """
    def __2D_to_1D (self, x, y):
        return (y * self.size_x + x)