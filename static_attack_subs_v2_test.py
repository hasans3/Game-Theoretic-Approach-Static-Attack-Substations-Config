# -*- coding: utf-8 -*-
"""
Created on Fri Jun 16 11:10:02 2017

@author: saqibhasan

This function serves as the main method for the static attack scenario. It is used to identify the transmission lines and its associated 
protection assembly that cause the worst case load loss. It includes the substation configuration. 

"""
# -----------------------------------------------------------------------------------------------------------------------------------
# INPUTS
# -----------------------------------------------------------------------------------------------------------------------------------
# This method takes the following arguments as inputs:
# filepath: Represents the system model.
# comp_filename: Represents the substation and protection assembly configuration of the system model.
# load_file_name: Represents the information about the loading points in the system and their details.
# p_budget, s_budget: Represents the budget associated with the protection assembly and substations respectively.
# start_range, contingency_range, blackout_criterion, system_name: These parameters are not used inside this method
# but are present. User's can ignore these arguments.
# -----------------------------------------------------------------------------------------------------------------------------------
# OUTPUTS
# -----------------------------------------------------------------------------------------------------------------------------------
# This method produces the following outputs:
# worst_case_outage: Stores the transmission lines that cause maximum load loss.
# temp_max_loadloss: Stores the maximum load loss as a result of contingencies.
# worst_case_sub: Stores the maximum load loss causing substations. 
# -----------------------------------------------------------------------------------------------------------------------------------

def greedy_hueristics(filepath, comp_filename, load_file_name, start_range, contingency_range, blackout_criterion, system_name, p_budget, s_budget):
# -----------------------------------------------------------------------------------------------------------------------------------
# Importing supporting methods
# -----------------------------------------------------------------------------------------------------------------------------------
    import time
    import maptest_testing
    import maptest_testing_subs
    import static_attack_subs_support
#    import maptest_testing_trimmed
    import trimmed_list
# -----------------------------------------------------------------------------------------------------------------------------------
# Initializing the method variables
# -----------------------------------------------------------------------------------------------------------------------------------
    tot_exe_time_start = time.time() # Starting the timer
    temp_max_loadloss = 0;
    worst_case_outage = [];
    worst_case_sub = [];
    loadloss_gain = 0;
# -----------------------------------------------------------------------------------------------------------------------------------
    for sub_budget in range(0, s_budget): # This loop runs for the value of s_budget and identifies the substations that maximizes the system damage
# -----------------------------------------------------------------------------------------------------------------------------------
# Attack Space generation
# ----------------------------------------------------------------------------------------------------------------------------------- 
        if (worst_case_sub == []):
            subs_config_dict = maptest_testing.maptest14bus_test_system(comp_filename, start_range, contingency_range);   			 # Depending upon the value of worst_case_sub, appropriate method is called. The inputs to both these methods maptest_testing,
        else:          																												 # trimmed_list are the comp_filename. Both of them returns a dictionary with substations as the keys and transmission lines 
            subs_config_dict = trimmed_list.maptest14bus_test_system(comp_filename, start_range, contingency_range, worst_case_sub); # associated with the respective protection assemblies as values which are then further used as attack points.
        subs_config_dict_keys = subs_config_dict.keys();
# -----------------------------------------------------------------------------------------------------------------------------------
# Finding the maximum load loss causing trasmission lines/protection assemblies
# -----------------------------------------------------------------------------------------------------------------------------------
        for i in range (0, len(subs_config_dict)):
            print subs_config_dict_keys[i];
            temp_comp_list = subs_config_dict[subs_config_dict_keys[i]]; # Identifies the transmission lines that are present in the respective substations
            print temp_comp_list
            temp_subs_elements = maptest_testing_subs.maptest14bus_test_system(temp_comp_list, start_range, contingency_range); # Converts temp_comp_list into the required input format for the static_attack_subs_support method using maptest_testing_subs
            max_load_loss_outage, max_loadloss = static_attack_subs_support.greedy_hueristics(filepath, temp_subs_elements, load_file_name, start_range, contingency_range, blackout_criterion, system_name, p_budget);  # Calls the method static_attack_subs_support for computing the worst case load loss caused by the transmission lines/protection assemblies 
# -----------------------------------------------------------------------------------------------------------------------------------
# Updating the solution																													
# -----------------------------------------------------------------------------------------------------------------------------------																									 # as per the budget constraints. The method returns the maximum load loss max_loadloss and corresponding transmission line max_load_loss_outage. 
            if (max_loadloss > temp_max_loadloss): # Checks if the current system damage is more than any previous damage
                temp_max_loadloss = max_loadloss;  
                worst_case_outage = max_load_loss_outage; 
                worst_case_sub = subs_config_dict_keys[i];
                if sub_budget == 0:
                    worst_case_sub = tuple([worst_case_sub]);
                else:
                    worst_case_sub = worst_case_sub;
#            print worst_case_sub;
        if ((loadloss_gain - temp_max_loadloss) == 0): # Checks if there is a change in the solution for consecutive iterations. If not, the algorithm is terminated
            break;
        else:
            loadloss_gain = temp_max_loadloss; 
    tot_exe_time_end = time.time() # Stopping the timer
    tot_exe_time = (tot_exe_time_end - tot_exe_time_start) # Computes the actual run time of the algorithm
# -----------------------------------------------------------------------------------------------------------------------------------
# Prints the outputs on the console
# -----------------------------------------------------------------------------------------------------------------------------------
    print '@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@'
    print 'Worst case outage: %s' %worst_case_outage
    print 'Worst case loadloss: %s' %temp_max_loadloss
    print 'Worst case substation: {0}'.format(worst_case_sub)
    print 'Total execution time in seconds: %s' %tot_exe_time
    print '@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@'
# -----------------------------------------------------------------------------------------------------------------------------------

# -----------------------------------------------------------------------------------------------------------------------------------
# Method call with different system models
# -----------------------------------------------------------------------------------------------------------------------------------
#greedy_hueristics("'G:\saqib\open DSS\opendss_matlab_interface\ieee9bus_system.dss'", "G:\saqib\open DSS\OpenDSS_Python_Interface\ieee_9_bus_data\component_data_heuristics.txt", "G:\saqib\open DSS\OpenDSS_Python_Interface\ieee_9_bus_data\Load_data_with_reactive_load.txt", 0, 1, 40, 'wscc9bus_system_test_N-1.xml', 2);
#greedy_hueristics("'G:\saqib\open DSS\OpenDSS_Python_Interface\ieee_14_bus_data\ieee14bus_system_with_txr.dss'", "G:\saqib\open DSS\OpenDSS_Python_Interface\ieee_14_bus_data\component_data_subs.txt", "G:\saqib\open DSS\OpenDSS_Python_Interface\Load_data_with_reactive_power.txt", 0, 1, 40, 'ieee14bus_system_N-1.xml', 5, 5);
greedy_hueristics("'G:\saqib\open DSS\OpenDSS_Python_Interface\ieee39bus_system\ieee39bus_system_with_1kv_base.dss'", "G:\saqib\open DSS\OpenDSS_Python_Interface\ieee39bus_system\component_data_subs.txt", "G:\saqib\open DSS\OpenDSS_Python_Interface\ieee39bus_system\Load_data1.txt", 0, 1, 40, 'ieee39bus_system_test_N-3.xml', 4, 4);
#greedy_hueristics("'G:\saqib\open DSS\OpenDSS_Python_Interface\ieee_57_bus_system\ieee57bussystem1.dss'", "G:\saqib\open DSS\OpenDSS_Python_Interface\ieee_57_bus_system\component_data_subs.txt", "G:\saqib\open DSS\OpenDSS_Python_Interface\ieee_57_bus_system\Load_data.txt", 0, 1, 40, 'ieee57bus_system_N-1.xml', 5, 7);    
#greedy_hueristics("'G:\saqib\open DSS\OpenDSS_Python_Interface\ieee_14_bus_data\ieee14bus_system_with_txr.dss'", "G:\saqib\open DSS\OpenDSS_Python_Interface\ieee_14_bus_data\component_data_test.txt", "G:\saqib\open DSS\OpenDSS_Python_Interface\Load_data_with_reactive_power.txt", 0, 1, 40, 'ieee14bus_system_N-1.xml', 2);
#greedy_hueristics("'G:\saqib\open DSS\OpenDSS_Python_Interface\ieee39bus_system\ieee39bus_system_with_1kv_base.dss'", "G:\saqib\open DSS\OpenDSS_Python_Interface\ieee39bus_system\component_data_test.txt", "G:\saqib\open DSS\OpenDSS_Python_Interface\ieee39bus_system\Load_data1.txt", 0, 1, 40, 'ieee39bus_system_test_N-3.xml', 2);
# -----------------------------------------------------------------------------------------------------------------------------------
