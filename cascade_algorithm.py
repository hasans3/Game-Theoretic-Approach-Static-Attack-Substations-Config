# -*- coding: utf-8 -*-
"""
Created on Fri Mar 03 14:09:15 2017

@author: saqibhasan

This method is the contingency simulator for the entire framework and acts as a support method for static_attack_subs_support.py. 

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
# selected_outage_new: Stores the transmission lines that cause maximum load loss.
# max_load_loss: Stores the maximum load loss as a result of contingencies. 
# -----------------------------------------------------------------------------------------------------------------------------------

def DSS_Python_Interface1(filepath, comp_filename, load_file_name, start_range, contingency_range, blackout_criterion, system_name):
    
# -----------------------------------------------------------------------------------------------------------------------------------
# Setting up the com interface and importing the necessary methods
# -----------------------------------------------------------------------------------------------------------------------------------           
    import win32com.client
    import load_maptest14bus1
    import numpy as np
    from xml.dom import minidom
    import time
# -----------------------------------------------------------------------------------------------------------------------------------
# Instantiate the OpenDSS Object
# -----------------------------------------------------------------------------------------------------------------------------------        
    total_execution_time_start = time.time()
    DSSObj = win32com.client.Dispatch("OpenDSSEngine.DSS");   
# -----------------------------------------------------------------------------------------------------------------------------------
# Start the solver
# -----------------------------------------------------------------------------------------------------------------------------------            
    DSSStart = DSSObj.Start("0");
    if DSSStart:
        print("OpenDSS Engine started successfully")
    else:
        print("Unable to start the OpenDSS Engine")
# -----------------------------------------------------------------------------------------------------------------------------------
# Set up the Text, Circuit, and Solution Interfaces
# -----------------------------------------------------------------------------------------------------------------------------------            
    DSSText = DSSObj.Text;
    DSSCircuit = DSSObj.ActiveCircuit;
    DSSSolution = DSSCircuit.Solution;
# -----------------------------------------------------------------------------------------------------------------------------------
# Loading the circuit Using the Text Interface
# -----------------------------------------------------------------------------------------------------------------------------------            
    DSSText.Command = "clear";
    DSSText.Command = "Compile " + filepath; # Compiles the .dss file using the OpenDSS solver platform
    print("File compiled successfully")

# -------------------------------- Obtaining the contingencies -------------------------------
    contingencies = comp_filename;
    num_n_minus_k_contingencies = len(contingencies);

# -----------------------------------------------------------------------------------------------------------------------------------
# Method Variables Initialization
# -----------------------------------------------------------------------------------------------------------------------------------            
    LC = [];
    load_c = [];
    load_loss = [];
    final_load_loss_list = [];
    iLines = DSSCircuit.FirstPDElement();
    curr_Line_Name = [];
    Line_Names = [];
    load_Names = [];
    normal_line_curr_values = [];
    maxcurline_limit1 = [];
    curr_Line_Current = [];
    Line_Currents = [];
    Total_line_loss_counter = 0;
    blackout_counter = 0;
    max_load_loss = 0;
    selected_outage = [];
    selected_outage_new = [];
# -----------------------------------------------------------------------------------------------------------------------------------
# Obtaining current values of each line using the OpenDSS API and setting up the maximum threshold
# -----------------------------------------------------------------------------------------------------------------------------------            
    while(iLines > 0):
        line_curr_values = [];
        maxcurline_limit = [];
        curr_Line_Name = DSSCircuit.ActiveCktElement.Name;
        Line_Names.append(curr_Line_Name);
        curr_Line_Current = DSSCircuit.ActiveCktElement.CurrentsMagAng;
        LC = np.array(curr_Line_Current);
        Line_Currents.append(curr_Line_Current);
        for i in range(0,3):
            line_curr_values.append((LC[6+(2*i)]));
            maxcurline_limit.append((LC[6+(2*i)]*10/7));
        normal_line_curr_values.append(tuple(line_curr_values));
        maxcurline_limit1.append(tuple(maxcurline_limit));
        iLines = DSSCircuit.NextPDElement();
# --------------code for xml generation---------------------------- 
    root = minidom.Document();
    root_element = root.createElement('Contingencies');
    root.appendChild(root_element);
    xml_str = root.toprettyxml(indent="\t");
    data_path = system_name;
# -----------------------------------------------------------------------------------------------------------------------------------
# Simulating and Evaluating all the Contingencies 
# -----------------------------------------------------------------------------------------------------------------------------------                 
    for i in range(0, num_n_minus_k_contingencies):

# --------------code for xml generation----------------------------         
        mykcontingency = root.createElement('N-' + str(i+1) );
# -----------------------------------------------------------------         
        contingency = contingencies[i];
        size_of_contingency = len(contingency);
# -----------------------------------------------------------------------------------------------------------------------------------
# Activating Individual Contingency by removing each transmission line and loop through all the contingencies
# -----------------------------------------------------------------------------------------------------------------------------------                 
        for j in range(0, size_of_contingency):
            perct_load_loss = 0;
            initial_loss = [];
            stagecounter = 0;
            prev_stage_counter = 0;
            print "OUTAGE SELECTION NUMBER: %s" %(j+1)
            print "------------------------------------------------------------------------------------------------------"
            print "Calling Solver"
            Total_line_loss_counter = len(contingency[j]);
#            contingency[j] = ['Line.tl49','Line.tl85']
#     --------------code for xml generation----------------------------------           
            my_path = root.createElement('Path');
            my_initial_outage = root.createElement('Initial_Stage');
            my_path.appendChild(my_initial_outage);
# -----------------------------------------------------------------------------------------------------------------------------------
# Obtaining the initial outages and appending it to the list 
# -----------------------------------------------------------------------------------------------------------------------------------                             
            for k in range(0, len(contingency[j])):
                DSSCircuit.CktElements(contingency[j][k]).Open(1,0);
                DSSCircuit.CktElements(contingency[j][k]).Open(2,0);
                initial_loss.append(contingency[j][k]);

#     --------------code for xml generation----------------------------------                 
                my_outage = root.createElement('Outage');
                my_initial_outage.appendChild(my_outage);
                my_outage_text = root.createTextNode(str(contingency[j][k]));
                my_outage.appendChild(my_outage_text);
#     -----------------------------------------------------------------------                
            print "Initial outage: %s" %initial_loss
# -----------------------------------------------------------------------------------------------------------------------------------
# Solving the circuit and updating line current values after initial outages 
# -----------------------------------------------------------------------------------------------------------------------------------                 
            DSSSolution.Solve();
            iLines = DSSCircuit.FirstPDElement();
            normal_line_curr_values = [];
            while(iLines > 0):
                line_curr_values = [];
                curr_Line_Name = DSSCircuit.ActiveCktElement.Name;
                Line_Names.append(curr_Line_Name);
                curr_Line_Current = DSSCircuit.ActiveCktElement.CurrentsMagAng;
                LC = np.array(curr_Line_Current);
                Line_Currents.append(np.array(curr_Line_Current));
                for k in range(0,3):
                    line_curr_values.append((LC[6+(2*k)]));
                normal_line_curr_values.append(tuple(line_curr_values));
                iLines = DSSCircuit.NextPDElement();
            overloadExists=1;
#     --------------code for xml generation----------------------------------             
            my_cascading_outage = root.createElement('Cascading_Stage');
            final_stage_text = 'Safe';
# -----------------------------------------------------------------------------------------------------------------------------------
# Checks for overloads due to initial outages and blackout criterion satisfaction
# -----------------------------------------------------------------------------------------------------------------------------------                 
            while(overloadExists == 1):
                overloadExists = 0;
                stagecounter = stagecounter + 1;
                line_loss = [];
                load_loss = [];
                load_Names = [];
                size = len(normal_line_curr_values);
                for k in range(0,size):
# -----------------------------------------------------------------------------------------------------------------------------------
# Removing overloaded transmission lines
# -----------------------------------------------------------------------------------------------------------------------------------                 
                    if (normal_line_curr_values[k][1] >= maxcurline_limit1[k][1]):
                        DSSCircuit.CktElements(Line_Names[k]).Open(1,0);
                        DSSCircuit.CktElements(Line_Names[k]).Open(2,0);
                        line_loss.append(str(Line_Names[k]));
                        overloadExists = 1;
                        Total_line_loss_counter = Total_line_loss_counter + 1;
                line_loss_size = len(line_loss);
                if (line_loss_size != 0):
                    print "Stage {0}, Components Failed: {1} ".format(stagecounter, line_loss)
#     --------------code for xml generation-----------------------------------------                    
                    my_stage_num = root.createElement('Stage_Number');
                    my_stage_num_text = root.createTextNode(str(stagecounter));
                    my_stage_num.appendChild(my_stage_num_text);
                    for k in range(0, line_loss_size):
                        my_outage = root.createElement('Outage');
                        my_outage_text = root.createTextNode(line_loss[k]);
                        my_outage.appendChild(my_outage_text);
                        my_stage_num.appendChild(my_outage);
                    my_cascading_outage.appendChild(my_stage_num);
# -----------------------------------------------------------------------------------------------------------------------------------
# Solving the circuit and updating transmission line currents after removal of overloaded lines to check for further overloads 
# -----------------------------------------------------------------------------------------------------------------------------------                                                     
                DSSSolution.Solve();
                iLines = DSSCircuit.FirstPDElement();
                normal_line_curr_values = [];
                while(iLines > 0):
                    line_curr_values = [];
                    curr_Line_Name = DSSCircuit.ActiveCktElement.Name;
                    Line_Names.append(curr_Line_Name);
                    curr_Line_Current = DSSCircuit.ActiveCktElement.CurrentsMagAng;
                    LC = np.array(curr_Line_Current);
                    Line_Currents.append(np.array(curr_Line_Current));
                    for k in range(0,3):
                        line_curr_values.append((LC[6+(2*k)]));
                    normal_line_curr_values.append(tuple(line_curr_values));
                    iLines = DSSCircuit.NextPDElement();
# -----------------------------------------------------------------------------------------------------------------------------------
# Checking for system load loss/damage
# -----------------------------------------------------------------------------------------------------------------------------------                                                   
                iLoads = DSSCircuit.FirstPCElement();
                load_curr_values = [];
                load_Names = [];
                load_loss = [];
                while(iLoads > 0):
                    load_i_values = [];
                    load_Name = DSSCircuit.ActiveCktElement.Name;
                    load_Names.append(load_Name);
                    load_current = DSSCircuit.ActiveCktElement.CurrentsMagAng;
                    load_c = np.array(load_current);
                    for k in range(0,3):
                        load_i_values.append((load_c[2*k]));
                    load_curr_values.append(tuple(load_i_values));
                    iLoads = DSSCircuit.NextPCElement();
                for k in range(0 , len(load_curr_values)):
                    if (load_curr_values[k][1] <= 1):
                        load_loss.append(load_Names[k]);
# -----------------------------------------------------------------------------------------------------------------------------------
# Checking for the blackout criterion satisfaction 
# -----------------------------------------------------------------------------------------------------------------------------------                                    
                T_sys_load, amt_load_loss = load_maptest14bus1.load_maptest14bus(load_file_name, load_loss);
                perct_load_loss = (float(amt_load_loss)/float(T_sys_load))*100;
                if (( perct_load_loss >= blackout_criterion) and overloadExists==0):
                    prev_stage_counter = 1;
                    print '***********************************************************************'
                    print "%s percent of load has been lost" %perct_load_loss
                    print "System Blackout"
                    print "{0} MW load has been lost out of {1} MW total load".format(amt_load_loss, T_sys_load);
                    print '***********************************************************************'
#    ------------------------------------- text added for xml code -----------------------------------------------                    
                    final_stage_text = 'Blackout';
                    blackout_counter = blackout_counter + 1;
# -----------------------------------------------------------------------------------------------------------------------------------
# Checking and updating the maximum load loss causing contingencies
# -----------------------------------------------------------------------------------------------------------------------------------                                    
            if (prev_stage_counter != 1):
                print "%s percent of load has been lost" %perct_load_loss
            if (perct_load_loss > max_load_loss):
                max_load_loss = perct_load_loss;
                selected_outage = contingency[j];
#    --------------code for xml generation-----------------------------------------
            my_path.appendChild(my_cascading_outage);
            my_final_stage = root.createElement('Final_Stage');
            my_final_stage_text = root.createTextNode(final_stage_text);
            my_final_stage.appendChild(my_final_stage_text);
            my_path.appendChild(my_final_stage);
#    ------------------------------------------------------------------------------ 
            final_load_loss_list.append(perct_load_loss);
            print "Number of stages of failure = %s " %(stagecounter-1)
            print "Total number of components failed = %s " %Total_line_loss_counter
# -----------------------------------------------------------------------------------------------------------------------------------
# Resetting the system model back to nominal state
# -----------------------------------------------------------------------------------------------------------------------------------                                    
            DSSText.Command = "Compile " + filepath;
#    ---------------------------- code for xml generation -------------------------------
            mykcontingency.appendChild(my_path);
        root_element.appendChild(mykcontingency);
        xml_str = root.toprettyxml(indent="\t");
    selected_outage_new.append(selected_outage)
# -----------------------------------------------------------------------------------------------------------------------------------
# Prints the outputs on the console
# -----------------------------------------------------------------------------------------------------------------------------------                                    
    print '#######################################################################################################'
    print 'Maximum load loss causing outage: %s' %selected_outage
    print 'Maximum load loss causing outage: %s' %selected_outage_new
    print 'Maximum load loss (in percent): %s' %max_load_loss
    print '#######################################################################################################'
    print "Number of Blackout cases = %d" %blackout_counter
    total_execution_time_end = time.time() # Stops the timer
    total_execution_time = (total_execution_time_end - total_execution_time_start) # Computes the actual run time of the algorithm
#    print 'Total execution time in seconds: %s' %total_execution_time
    return (selected_outage_new, max_load_loss) 
          
#DSS_Python_Interface1("'G:\saqib\open DSS\OpenDSS_Python_Interface\ieee39bus_system\ieee39bus_system_with_1kv_base.dss'", "G:\saqib\open DSS\OpenDSS_Python_Interface\ieee39bus_system\component_data.txt", "G:\saqib\open DSS\OpenDSS_Python_Interface\ieee39bus_system\Load_data1.txt", 3, 40, 'ieee39bus_system_test_N-3.xml');
#DSS_Python_Interface1("'G:\saqib\open DSS\opendss_matlab_interface\ieee9bus_system.dss'", "G:\saqib\open DSS\OpenDSS_Python_Interface\ieee_9_bus_data\component_data_heuristics.txt", "G:\saqib\open DSS\OpenDSS_Python_Interface\ieee_9_bus_data\Load_data_with_reactive_load.txt", 0, 1, 40, 'wscc9bus_system_test_N-1.xml'); 
#DSS_Python_Interface1("'G:\saqib\ieee14bus_system.dss'", "G:\saqib\open DSS\OpenDSS_Python_Interface\component_data.txt", "G:\saqib\open DSS\OpenDSS_Python_Interface\Load_data_with_reactive_power.txt",1, 40, 'ieee14bus_system_N-1.xml');   
#DSS_Python_Interface1("'G:\saqib\open DSS\OpenDSS_Python_Interface\ieee_14_bus_data\ieee14bus_system_with_txr.dss'", "G:\saqib\open DSS\OpenDSS_Python_Interface\ieee_14_bus_data\component_data.txt", "G:\saqib\open DSS\OpenDSS_Python_Interface\Load_data_with_reactive_power.txt", 0, 1, 40, 'ieee14bus_system_N-1.xml');       
#DSS_Python_Interface1("'G:\saqib\open DSS\OpenDSS_Python_Interface\ieee_57_bus_system\ieee57bussystem1.dss'", "G:\saqib\open DSS\OpenDSS_Python_Interface\ieee_57_bus_system\component_data.txt", "G:\saqib\open DSS\OpenDSS_Python_Interface\ieee_57_bus_system\Load_data.txt", 1, 40, 'ieee57bus_system_N-1.xml');    
#DSS_Python_Interface1("'G:\saqib\open DSS\OpenDSS_Python_Interface\ieee_14_bus_data\ieee14bus_system_with_txr.dss'", "G:\saqib\open DSS\OpenDSS_Python_Interface\ieee_14_bus_data\component_data_test.txt", "G:\saqib\open DSS\OpenDSS_Python_Interface\Load_data_with_reactive_power.txt",5, 40, 'ieee14bus_system_test.xml');       
