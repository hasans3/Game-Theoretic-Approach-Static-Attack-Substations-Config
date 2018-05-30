# -*- coding: utf-8 -*-
"""
Created on Tue Oct 04 11:01:35 2016

@author: saqibhasan

This is the function to calcaulate the load loss given a contingency.
It is used as a supporting method in cascade_algorithm.py, cascade_algorithm_reduced_outages.py

"""

# -----------------------------------------------------------------------------------------------------------------------------------
# INPUTS
# -----------------------------------------------------------------------------------------------------------------------------------
# This method takes the following arguments as inputs:
# load_file_name: Represents the information about the loading points in the system and their details.
# load_loss: Represents a list of names of the loads that are removed from the system model.
# -----------------------------------------------------------------------------------------------------------------------------------
# OUTPUTS
# -----------------------------------------------------------------------------------------------------------------------------------
# This method takes the following outputs:
# Total_system_load: Represents the total system load.
# amount_load_loss: Represents the load loss/damage.
# -----------------------------------------------------------------------------------------------------------------------------------


def load_maptest14bus(load_file_name, load_loss):

    import math # Importing the library methods
# -----------------------------------------------------------------------------------------------------------------------------------
# Initialization the method variables
# -----------------------------------------------------------------------------------------------------------------------------------
    Total_system_load = 0.0;
    load_loss_values = [];
    amount_load_loss= 0.0;
# -----------------------------------------------------------------------------------------------------------------------------------
# Opens and read the text file and convert the content into a dictionary
# -----------------------------------------------------------------------------------------------------------------------------------           
    file_data = open(load_file_name, 'r') # Opens the file in the read mode
    data = file_data.readline();
    keyset1 = eval(data);
    file_data.close() # Closes the file
    load_loss1 = load_loss;
# -----------------------------------------------------------------------------------------------------------------------------------
# Calculating the total system load
# -----------------------------------------------------------------------------------------------------------------------------------           
    values = keyset1.values();
    for i in range(0 , len(values)):
        c = 0.0;
        for j in range(0,2):
            a = values[i][j];
            b = a*a;
            c = c+b;
        d = math.sqrt(c);
        Total_system_load = Total_system_load + d;
# -----------------------------------------------------------------------------------------------------------------------------------
# Getting the values of the keys in the load_loss list  
# -----------------------------------------------------------------------------------------------------------------------------------           
    load_loss_size = len(load_loss1);
    for i in range(0, load_loss_size):
        load_loss_values.append(keyset1[load_loss1[i]]);
# -----------------------------------------------------------------------------------------------------------------------------------
# Calculating the total load loss
# -----------------------------------------------------------------------------------------------------------------------------------           
    for i in range(0, len(load_loss_values)):
        c = 0.0;
        for j in range(0,2):
            a = load_loss_values[i][j];
            b = a*a;
            c = c+b;
        d = math.sqrt(c);
        amount_load_loss = amount_load_loss + d;
#        print amount_load_loss
    return (Total_system_load, amount_load_loss);
    
#load_maptest14bus("G:\saqib\open DSS\OpenDSS_Python_Interface\Load_data_with_reactive_power.txt", load_loss);