# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 14:22:18 2017

@author: saqibhasan

This method is used to identify the transmission lines and its associated protection assembly that cause the worst load loss. It
acts as a support function to the static_attack_subs_v2_test.py.
"""

# -----------------------------------------------------------------------------------------------------------------------------------
# INPUTS
# -----------------------------------------------------------------------------------------------------------------------------------
# This method takes the following arguments as inputs:
# filepath: Represents the system model.
# comp_filename: Represents the substation and protection assembly configuration of the system model.
# load_file_name: Represents the information about the loading points in the system and their details.
# l_budget: Represents the budget associated with the protection assemblies.
# start_range, contingency_range, blackout_criterion, system_name: These parameters are not used inside this method
# but are present. User's can ignore these arguments.
# -----------------------------------------------------------------------------------------------------------------------------------
# OUTPUTS
# -----------------------------------------------------------------------------------------------------------------------------------
# This method produces the following outputs:
# worst_case_outage: Stores the transmission lines that cause maximum load loss.
# temp_max_loadloss: Stores the maximum load loss as a result of contingencies. 
# -----------------------------------------------------------------------------------------------------------------------------------

def greedy_hueristics(filepath, comp_filename, load_file_name, start_range, contingency_range, blackout_criterion, system_name, l_budget):
# -----------------------------------------------------------------------------------------------------------------------------------
# Importing supporting methods
# -----------------------------------------------------------------------------------------------------------------------------------    
    import cascade_algorithm
    import maptest_new_outage_list
    import cascade_algorithm_reduced_outages
    import time
# -----------------------------------------------------------------------------------------------------------------------------------
# Initializing the method variables
# -----------------------------------------------------------------------------------------------------------------------------------
    tot_exe_time_start = time.time() # Starting the timer
    temp_max_loadloss = 0;
    worst_case_outage = [];
# -----------------------------------------------------------------------------------------------------------------------------------
# Finding the maximum loadloss/damage causing transmission lines, also known as outages.
# -----------------------------------------------------------------------------------------------------------------------------------
    max_load_loss_outage, max_loadloss = cascade_algorithm.DSS_Python_Interface1(filepath, comp_filename, load_file_name, start_range, contingency_range, blackout_criterion, system_name); # Returns the maximum load loss causing contingency. Identifies the first transmission line to attack.
#    print max_load_loss_outage
    temp_max_loadloss = max_loadloss; 
    worst_case_outage = max_load_loss_outage;  
    for k in range(0, (l_budget-1)): # Loop runs for identifying the most damaging attack combination
        new_outage_list = maptest_new_outage_list.maptest14bus_test_system(comp_filename, start_range, contingency_range, max_load_loss_outage); # Returns the updated list of contingencies to be simulated based on the first identified maximum load loss causing outage.
#        print new_outage_list
        max_load_loss_outage, max_loadloss = cascade_algorithm_reduced_outages.DSS_Python_Interface1(filepath, comp_filename, load_file_name, start_range, contingency_range, blackout_criterion, system_name, new_outage_list); # Identifies the worst case load loss causing contingencies.
# -----------------------------------------------------------------------------------------------------------------------------------
# Updating the solution																													
# -----------------------------------------------------------------------------------------------------------------------------------																									 
        if (max_loadloss > temp_max_loadloss): # Checks if the current system damage is more than any previous damage
            temp_max_loadloss = max_loadloss;
            worst_case_outage = max_load_loss_outage;
    tot_exe_time_end = time.time() # Stop the timer
    tot_exe_time = (tot_exe_time_end - tot_exe_time_start) # Compute the actual run time of the algorithm
# -----------------------------------------------------------------------------------------------------------------------------------
# Prints the outputs on the console
# -----------------------------------------------------------------------------------------------------------------------------------
    print '@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@'
    print 'Worst case outage: %s' %worst_case_outage
    print 'Worst case loadloss: %s' %temp_max_loadloss
    print 'Total execution time in seconds: %s' %tot_exe_time
    print '@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@'
    return worst_case_outage, temp_max_loadloss
# -----------------------------------------------------------------------------------------------------------------------------------
    
#greedy_hueristics("'G:\saqib\open DSS\opendss_matlab_interface\ieee9bus_system.dss'", "G:\saqib\open DSS\OpenDSS_Python_Interface\ieee_9_bus_data\component_data_heuristics.txt", "G:\saqib\open DSS\OpenDSS_Python_Interface\ieee_9_bus_data\Load_data_with_reactive_load.txt", 0, 1, 40, 'wscc9bus_system_test_N-1.xml', 2);
#greedy_hueristics("'G:\saqib\open DSS\OpenDSS_Python_Interface\ieee_14_bus_data\ieee14bus_system_with_txr.dss'", "G:\saqib\open DSS\OpenDSS_Python_Interface\ieee_14_bus_data\component_data.txt", "G:\saqib\open DSS\OpenDSS_Python_Interface\Load_data_with_reactive_power.txt", 0, 1, 40, 'ieee14bus_system_N-1.xml', 2);
#greedy_hueristics("'G:\saqib\open DSS\OpenDSS_Python_Interface\ieee39bus_system\ieee39bus_system_with_1kv_base.dss'", "G:\saqib\open DSS\OpenDSS_Python_Interface\ieee39bus_system\component_data.txt", "G:\saqib\open DSS\OpenDSS_Python_Interface\ieee39bus_system\Load_data1.txt", 0, 1, 40, 'ieee39bus_system_test_N-3.xml', 3);
#greedy_hueristics("'G:\saqib\open DSS\OpenDSS_Python_Interface\ieee_57_bus_system\ieee57bussystem1.dss'", "G:\saqib\open DSS\OpenDSS_Python_Interface\ieee_57_bus_system\component_data.txt", "G:\saqib\open DSS\OpenDSS_Python_Interface\ieee_57_bus_system\Load_data.txt", 0, 1, 40, 'ieee57bus_system_N-1.xml', 4);    
#greedy_hueristics("'G:\saqib\open DSS\OpenDSS_Python_Interface\ieee_14_bus_data\ieee14bus_system_with_txr.dss'", "G:\saqib\open DSS\OpenDSS_Python_Interface\ieee_14_bus_data\component_data_test.txt", "G:\saqib\open DSS\OpenDSS_Python_Interface\Load_data_with_reactive_power.txt", 0, 1, 40, 'ieee14bus_system_N-1.xml', 2);
#greedy_hueristics("'G:\saqib\open DSS\OpenDSS_Python_Interface\ieee39bus_system\ieee39bus_system_with_1kv_base.dss'", "G:\saqib\open DSS\OpenDSS_Python_Interface\ieee39bus_system\component_data_test.txt", "G:\saqib\open DSS\OpenDSS_Python_Interface\ieee39bus_system\Load_data1.txt", 0, 1, 40, 'ieee39bus_system_test_N-3.xml', 2);
