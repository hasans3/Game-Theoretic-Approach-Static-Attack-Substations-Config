# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 16:13:27 2017

@author: saqibhasan

This code is used to identify the transmission lines and its associated protection assembly that cause the worst load loss by using 
greedy hueristics. It includes the substation configuration. It is an extended version of greedy_algorithm.py

"""

def greedy_hueristics(filepath, comp_filename, load_file_name, start_range, contingency_range, blackout_criterion, system_name, p_budget, s_budget):
    import time
    import maptest_testing
    import maptest_testing_subs
    import static_attack_subs_support
#    import maptest_testing_trimmed
    import trimmed_list
    tot_exe_time_start = time.time()
    temp_max_loadloss = 0;
    worst_case_outage = [];
    worst_case_sub = [];
    loadloss_gain = 0;
    for sub_budget in range(0, s_budget):
        if (worst_case_sub == []):
            subs_config_dict = maptest_testing.maptest14bus_test_system(comp_filename, start_range, contingency_range);
        else:
            subs_config_dict = trimmed_list.maptest14bus_test_system(comp_filename, start_range, contingency_range, worst_case_sub);
        subs_config_dict_keys = subs_config_dict.keys();
        for i in range (0, len(subs_config_dict)):
            print subs_config_dict_keys[i];
            temp_comp_list = subs_config_dict[subs_config_dict_keys[i]];
            print temp_comp_list
            temp_subs_elements = maptest_testing_subs.maptest14bus_test_system(temp_comp_list, start_range, contingency_range);
            max_load_loss_outage, max_loadloss = static_attack_subs_support.greedy_hueristics(filepath, temp_subs_elements, load_file_name, start_range, contingency_range, blackout_criterion, system_name, p_budget);  
            if (max_loadloss > temp_max_loadloss):
                temp_max_loadloss = max_loadloss;
                worst_case_outage = max_load_loss_outage;
                worst_case_sub = subs_config_dict_keys[i];
                if sub_budget == 0:
                    worst_case_sub = tuple([worst_case_sub]);
                else:
                    worst_case_sub = worst_case_sub;
#            print worst_case_sub;
        if ((loadloss_gain - temp_max_loadloss) == 0):
            break;
        else:
            loadloss_gain = temp_max_loadloss;
    tot_exe_time_end = time.time()
    tot_exe_time = (tot_exe_time_end - tot_exe_time_start)
    print '@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@'
    print 'Worst case outage: %s' %worst_case_outage
    print 'Worst case loadloss: %s' %temp_max_loadloss
    print 'Worst case substation: {0}'.format(worst_case_sub)
    print 'Total execution time in seconds: %s' %tot_exe_time
    print '@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@'
    return worst_case_outage, temp_max_loadloss, worst_case_sub

#greedy_hueristics("'G:\saqib\open DSS\opendss_matlab_interface\ieee9bus_system.dss'", "G:\saqib\open DSS\OpenDSS_Python_Interface\ieee_9_bus_data\component_data_heuristics.txt", "G:\saqib\open DSS\OpenDSS_Python_Interface\ieee_9_bus_data\Load_data_with_reactive_load.txt", 0, 1, 40, 'wscc9bus_system_test_N-1.xml', 2);
#greedy_hueristics("'G:\saqib\open DSS\OpenDSS_Python_Interface\ieee_14_bus_data\ieee14bus_system_with_txr.dss'", "G:\saqib\open DSS\OpenDSS_Python_Interface\ieee_14_bus_data\component_data_subs.txt", "G:\saqib\open DSS\OpenDSS_Python_Interface\Load_data_with_reactive_power.txt", 0, 1, 40, 'ieee14bus_system_N-1.xml', 2, 2);
#greedy_hueristics("'G:\saqib\open DSS\OpenDSS_Python_Interface\ieee39bus_system\ieee39bus_system_with_1kv_base.dss'", "G:\saqib\open DSS\OpenDSS_Python_Interface\ieee39bus_system\component_data_subs.txt", "G:\saqib\open DSS\OpenDSS_Python_Interface\ieee39bus_system\Load_data1.txt", 0, 1, 40, 'ieee39bus_system_test_N-3.xml', 2, 2);
#greedy_hueristics("'G:\saqib\open DSS\OpenDSS_Python_Interface\ieee_57_bus_system\ieee57bussystem1.dss'", "G:\saqib\open DSS\OpenDSS_Python_Interface\ieee_57_bus_system\component_data.txt", "G:\saqib\open DSS\OpenDSS_Python_Interface\ieee_57_bus_system\Load_data.txt", 0, 1, 40, 'ieee57bus_system_N-1.xml', 4);    
#greedy_hueristics("'G:\saqib\open DSS\OpenDSS_Python_Interface\ieee_14_bus_data\ieee14bus_system_with_txr.dss'", "G:\saqib\open DSS\OpenDSS_Python_Interface\ieee_14_bus_data\component_data_test.txt", "G:\saqib\open DSS\OpenDSS_Python_Interface\Load_data_with_reactive_power.txt", 0, 1, 40, 'ieee14bus_system_N-1.xml', 2);
#greedy_hueristics("'G:\saqib\open DSS\OpenDSS_Python_Interface\ieee39bus_system\ieee39bus_system_with_1kv_base.dss'", "G:\saqib\open DSS\OpenDSS_Python_Interface\ieee39bus_system\component_data_test.txt", "G:\saqib\open DSS\OpenDSS_Python_Interface\ieee39bus_system\Load_data1.txt", 0, 1, 40, 'ieee39bus_system_test_N-3.xml', 2);
