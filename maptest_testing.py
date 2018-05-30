# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 16:21:26 2017

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
# The method returns a dictionary with the appropriate configuration information of the system model.
# The keys represent the substations and the values represent the associated transmission lines with the respective substations.
# -----------------------------------------------------------------------------------------------------------------------------------

def maptest14bus_test_system(comp_filename, start_range, contingency_range):
    
    valueset =[]; # Variable initialization
# -----------------------------------------------------------------------------------------------------------------------------------
# Opens and read the text file and convert the content into a dictionary
# ----------------------------------------------------------------------------------------------------------------------------------- 
    data_file = open(comp_filename, 'r'); # opens the file in read mode
    line_data = data_file.readline(); 
    valueset = eval(line_data); # stores the information in the dictionary
    data_file.close() # closes the file
#    print valueset
    return valueset;

    
#maptest14bus_test_system("G:\saqib\open DSS\OpenDSS_Python_Interface\ieee_14_bus_data\component_data_subs.txt",1,2);