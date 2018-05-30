# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 15:27:21 2017

@author: saqibhasan

It acts as a support function to the static_attack_subs_support.py.
"""

# -----------------------------------------------------------------------------------------------------------------------------------
# INPUTS
# -----------------------------------------------------------------------------------------------------------------------------------
# This method takes the following arguments as inputs:
# comp_filename: Represents the substation and protection assembly configuration of the system model.
# start_range, contingency_range: These parameters are not used inside this method but are present because the 
# same function is used as a contingency generator in another framework. User's can ignore these arguments. 
# However, the default value is 0, 1 respectively.
# max_load_loss_contingency: Represents a list of transmission lines.
# -----------------------------------------------------------------------------------------------------------------------------------
# OUTPUTS
# -----------------------------------------------------------------------------------------------------------------------------------
# The method returns a list of transmission lines that needs to be attacked in the form of contingencies.
# -----------------------------------------------------------------------------------------------------------------------------------

def maptest14bus_test_system(comp_filename, start_range, contingency_range, max_load_loss_contingency):
    from compiler.ast import flatten  # Importing methods from the library 
# -----------------------------------------------------------------------------------------------------------------------------------
# Initialization the method variables
# -----------------------------------------------------------------------------------------------------------------------------------
    CMB = [];
    CMB_new = [];
    temp_valueset = [];
    new_valueset = []
    valueset_new = []
# -----------------------------------------------------------------------------------------------------------------------------------
# Create a list of transmission lines to be attacked using the information from the max_load_loss_contingency list
# -----------------------------------------------------------------------------------------------------------------------------------
    valueset = comp_filename;
    valueset_new = list(flatten(valueset)) 
    iter_max_load_loss_outage = max_load_loss_contingency
    max_load_loss_outage = iter_max_load_loss_outage
    max_load_loss_outage = list(flatten(max_load_loss_outage))
    for elem in range(0, len(max_load_loss_outage)):
#        print max_load_loss_outage[elem]
        valueset_new.remove(max_load_loss_outage[elem]) # Removes the transmission lines from the original list.
    new_valueset = [valueset_new[i:i+1] for i in range(0, len(valueset_new), 1)]
# -----------------------------------------------------------------------------------------------------------------------------------
# Creating a new list of transmission lines contingencies
# -----------------------------------------------------------------------------------------------------------------------------------
    for i in range(0, len(new_valueset)):
        temp_valueset = new_valueset[i];
        temp_iter_max_load_loss_outage = iter_max_load_loss_outage[0];
        iter_temp_comb = temp_valueset + temp_iter_max_load_loss_outage; # Adding each transmission line with the list of transmission lines passed as Input to the method.
        CMB.append(iter_temp_comb)
    CMB_new.append(CMB)
#    print CMB_new
    return CMB_new
    
    

#maptest14bus_test_system("G:\saqib\open DSS\OpenDSS_Python_Interface\ieee_14_bus_data\component_data.txt",0,1);
#maptest14bus_test_system("G:\saqib\open DSS\OpenDSS_Python_Interface\ieee_9_bus_data\component_data_heuristics.txt",1,2);
