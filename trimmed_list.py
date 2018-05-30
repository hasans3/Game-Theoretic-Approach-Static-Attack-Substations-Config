# -*- coding: utf-8 -*-
"""
Created on Fri Jun 16 12:25:30 2017

@author: saqibhasan

It acts as a support function to the static_attack_subs_v2_test.py.
"""

# -----------------------------------------------------------------------------------------------------------------------------------
# INPUTS
# -----------------------------------------------------------------------------------------------------------------------------------
# This method takes the following arguments as inputs:
# comp_filename: Represents the substation and protection assembly configuration of the system model.
# start_range, contingency_range: These parameters are not used inside this method but are present because the 
# same function is used as a contingency generator in another framework. User's can ignore these arguments. 
# However, the default value is 0, 1 respectively.
# selected_item: Represents a set of substations.
# -----------------------------------------------------------------------------------------------------------------------------------
# OUTPUTS
# -----------------------------------------------------------------------------------------------------------------------------------
# The method returns a dictionary of substations and transmission lines that needs to be attacked.
# -----------------------------------------------------------------------------------------------------------------------------------

def maptest14bus_test_system(comp_filename, start_range, contingency_range, selected_item):
    
    from  more_itertools import unique_everseen # import methods from the library
# -----------------------------------------------------------------------------------------------------------------------------------
# Initialization the method variables
# -----------------------------------------------------------------------------------------------------------------------------------
    valueset = [];
    sub_items = {};
    temp_valueset = {};
    temp_sub_item_values = [];
# -----------------------------------------------------------------------------------------------------------------------------------
# Opens and read the text file and convert the content into a dictionary
# -----------------------------------------------------------------------------------------------------------------------------------   
    data_file = open(comp_filename, 'r');  # opens the file in read mode
    line_data = data_file.readline();
    valueset = eval(line_data); # stores the information in the dictionary
    data_file.close() # closes the file
#    print valueset
# -----------------------------------------------------------------------------------------------------------------------------------
# Removes the set of selected substations from the dictionary
# ----------------------------------------------------------------------------------------------------------------------------------- 
    for t in range(0, len(selected_item)):
        if selected_item[t] in valueset:
            temp_sub_item_values = temp_sub_item_values + valueset[selected_item[t]]; # stores the values of the selected keys in the list
            sub_items[selected_item] = temp_sub_item_values;  
            del valueset[selected_item[t]];
# -----------------------------------------------------------------------------------------------------------------------------------
# Creates a new dictionary
# ----------------------------------------------------------------------------------------------------------------------------------- 
    for item in valueset:
        valueset_key_values = valueset[item];
        sub_items_values = sub_items[selected_item];
        temp_valueset[tuple([item]) + tuple(selected_item)] = list(unique_everseen(valueset_key_values + sub_items_values)); # creating new key, value pairs
#    print temp_valueset
    return temp_valueset
    
#maptest14bus_test_system("G:\saqib\open DSS\OpenDSS_Python_Interface\ieee_14_bus_data\component_data_subs.txt", 1, 2, ('S4','S7'));