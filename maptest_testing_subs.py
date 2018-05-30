# -*- coding: utf-8 -*-
"""
Created on Tue Jun 06 15:45:48 2017

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
# -----------------------------------------------------------------------------------------------------------------------------------
# OUTPUTS
# -----------------------------------------------------------------------------------------------------------------------------------
# The method returns a list of transmission lines that needs to be attacked.
# -----------------------------------------------------------------------------------------------------------------------------------

def maptest14bus_test_system(comp_filename, start_range, contingency_range):
    
    import itertools # Importing supporting methods from library
# -----------------------------------------------------------------------------------------------------------------------------------
# Initialization the method variables
# -----------------------------------------------------------------------------------------------------------------------------------
    cmb = [];
    valueset =[];
# -----------------------------------------------------------------------------------------------------------------------------------
    valueset = comp_filename;
# -----------------------------------------------------------------------------------------------------------------------------------
# Generates the list as per the appropriate input format for the calling method
# -----------------------------------------------------------------------------------------------------------------------------------
    for i in range(start_range, contingency_range):
        comb=[];
        for j in itertools.combinations(valueset, i+1):
            comb.append(list(j));
            #print comb
        cmb.append(comb);
#    print cmb
    return cmb;

    
#maptest14bus_test_system("G:\saqib\open DSS\OpenDSS_Python_Interface\ieee_14_bus_data\component_data_subs.txt",1,2);