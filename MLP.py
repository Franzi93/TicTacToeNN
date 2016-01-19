# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 16:33:00 2015

@author: Ralf Engelken, Franziska Neu
"""

import numpy as np

"""
Implementiert ein Multi-Layer-Perceptron
"""
class MLP:
    """
    Erstellt ein neues MLP mit den übergeben Parametern
    """
    def __init__(self, input_size, hidden_size, output_size, learning_rate, adaption_steps = 1000, adaption_rate = 1):
        self.input_size    = input_size     # Die learning-rate steuert die Anpassungsgeschwindigkeit der Gewichts-Matrix
        self.hidden_size   = hidden_size    # Anzahl der Input-Neurone
        self.output_size   = output_size    # Anzahl der Neurone im hidden layer
        self.learning_rate = learning_rate  # ANzahl der Neurone der output-Schicht
    
        self.adaption_steps = adaption_steps
        self.adaption_rate = adaption_rate
    
        self.new_init()
    
    """
    Reinitialisiert die Gewichtungs-Matrizen des MLP
    """
    def new_init (self):
        self.counter = 0
        
        #Zufällige Initialisierung der Gewichtsmatrix der Verbindungen input-hidden
        self.W_i = np.random.uniform(-1.0, 1.0, (self.input_size, self.hidden_size))
        
        #Zufällige Initialisierung der Gewichtsmatrix der Verbindungen hidden-output
        self.W_o = np.random.uniform(-1.0, 1.0, (self.hidden_size, self.output_size))
        
        # Erstellen vom Bias der Neurone
        self.bias_hidden = np.random.uniform(-1.0, 1.0, (self.hidden_size))
        self.bias_output = np.random.uniform(-1.0, 1.0, (self.output_size))

        self.hidden = None
        
        self.new_game()
        #self.W_i = np.random.uniform(-0.2, 0.2, (self.input_size, self.hidden_size))
        #self.W_o = np.random.uniform(-0.2, 0.2, (self.hidden_size, self.output_size))
        #self.bias_hidden = np.random.uniform(-0.2, 0.2, (self.hidden_size))
        #self.bias_output = np.random.uniform(-0.2, 0.2, (self.output_size))

    def new_game(self):
        self.first_action = True
        self.hidden_tic = self.hidden

    """
    berechnet die aktivierung nach sigmoid, return: array
    """
    def sigmoidAktivierung(self, gewichtsmatrix, aktivierung, bias):
        try:
            z_net = bias + np.dot(aktivierung, gewichtsmatrix)
            z = 1/(1.0+np.exp(-z_net))
        except Exception as e:
            print z_net
            print np.exp(-z_net)
            print z
            exit
        return z
    
    """
    Trainiert das MLP mit den übergebenen Ein- und Ausgangsdaten
    """        
    def train (self, data_input, data_target_value, print_data=False):
        output = self.get_action(data_input)

        fehler_output = (data_target_value - output)

        self.evaluate_action(data_input, fehler_output)

        if (print_data == True):
            #if (fehler_output < 0):
                #print "Eingabe:", data_input, "   Erwartet:", data_out[counter_daten],("   Ausgabe: %.16f" % output), ("   Ausgabe-Fehler: %.16f" % fehler_output)
            #print "Erwartet:", data_target_value,("   Ausgabe: %.16f" % output), ("   Ausgabe-Fehler: %.16f" % fehler_output)
            fehler_output_summe = 0
            for i in range(len(fehler_output)):
                fehler_output_summe += fehler_output[i]
            print fehler_output_summe
            #else:
                #print "Eingabe:", data_input, "   Erwartet:", data_out[counter_daten],("   Ausgabe: %.16f" % output), ("   Ausgabe-Fehler:  %.16f" % fehler_output)
            #    print "Erwartet:", data_target_value,("   Ausgabe: %.16f" % output), ("   Ausgabe-Fehler:  %.16f" % fehler_output)
            #print "Hidden:", hidden
            #print "Hidden-Fehler:", fehler_hidden
            #print "W_o:", W_o
            #print "W_i:", W_i

        return fehler_output
             
    """
    Ermittelt die Ausgangswerte zu den übergebenen Eingangswerten
    """
    def get_action (self, data_input):
        self.hidden = self.hidden_tic
        self.hidden_tic = self.sigmoidAktivierung(self.W_i, data_input, self.bias_hidden)
        
        data_output = np.dot(self.hidden_tic, self.W_o) + self.bias_output
            
        return data_output  
   
    """
    Trainiert das MLP mit den Eingangswerten und dem Fehler der Ausgangswerte
    """
    def evaluate_action (self, data_input, fehler_output):
        
        self.counter += 1
        steps = self.counter / self.adaption_steps
        learning_rate = self.learning_rate * (self.adaption_rate ** steps)
        
        fehler_hidden = self.hidden_tic * (1.0 - self.hidden_tic) * np.dot(self.W_o, fehler_output)

        hilfsm_Wo = np.outer(self.hidden_tic, fehler_output)
        self.W_o = self.W_o + (learning_rate * hilfsm_Wo)

        hilfsm_Wi = np.outer(data_input,fehler_hidden)
        self.W_i = self.W_i + (learning_rate * hilfsm_Wi)
        
    """
    Trainiert das MLP mit den Eingangswerten und dem Fehler der Ausgangswerte
    """
    def evaluate_action_RL (self, data_input, fehler_output):
        
        self.counter += 1
        steps = self.counter / self.adaption_steps
        learning_rate = self.learning_rate * (self.adaption_rate ** steps)
        
        fehler_hidden = self.hidden * (1.0 - self.hidden) * np.dot(self.W_o, fehler_output)

        hilfsm_Wo = np.outer(self.hidden, fehler_output)
        self.W_o = self.W_o + (learning_rate * hilfsm_Wo)

        hilfsm_Wi = np.outer(data_input,fehler_hidden)
        self.W_i = self.W_i + (learning_rate * hilfsm_Wi)