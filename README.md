## Game-Theoretic-Approach for Static Attack Scenario

This folder contains the respective methods and supporting files needed for identifying static attack strategies.

## Background: 
Static attacks are those attacks that takes place simultaneously. Here, we consider a power system model representing a cyber-physical
energy system. This system consists of both physical and cyber components. Physical components represent transmission lines, loads, generators, 
transformers, buses, etc. However, cyber components represents the protection assemblies such as distance relay, over-current relay and circuit breakers.
A power system consists of a large number of substations. Each substation consists of several protection assemblies. These protection assemblies can be remotely 
monitored and controlled using the remote terminal units located in every substations. If an attacker gain access to a substation 
then he can manipulate these protection assemblies to disconnect transmission lines from the power system network and cause system damage.
However, considering the scale of the power system network it is impossible to exhaustively identify the substations and protection assemblies to attack
in order to maximize system damage. Hence, we use our game-theoretic approach to model this as an optimization problem and use our "static_attack_subs_v2_test.py"
method to obtain a efficient and resonable solution. 

Note: For more details about the problem, system model, etc., please refer to the paper titled "Vulnerability Analysis of Power Systems Based on Cyber-Attack and Defense Models". 
The document will be available on Vanderbilt Universities, Institute for software integrated systems under "Publications".

## How to run the main method `static_attack_subs_v2_test.py`?
  
To run the attack method, the following steps are needed:
1. `Install the OpenDSS` on the Windows machine as OpenDSS is not mac compatible.
2. `Download and save` the system models from the "System Models" folder to the local drive. 
3. `Install` Python 2.7.
4. `Install` Spyder, PyCharm or any other Python IDE.
5. `Open` the `static_attack_subs_v2_test.py` method and set the paths for the `filepath, comp_filename, load_file_name` as per the 
directory where the downloaded files are stored from the "System Models" folder. 

`filepath` is the path where `.dss` file is stored on the local drive.

`comp_filename` is the local drive path where `component_data_subs.txt` file is stored.

`load_file_name` is the path for the `load_data.txt` file stored on the local drive. For certain models the file name can be `load_data1.txt` or `load_data_testing1.txt`, etc.

6. Run `static_attack_subs_v2_test.py`.

## Supporting Methods 
1. `cascade_algorithm_reduced_outages.py`
2. `cascade_algorithm.py`
3. `load_maptest14bus1.py`
4. `maptest_new_outage_list.py`
5. `maptest_testing_subs.py`
6. `maptest_testing.py`
7. `static_attack_subs_support.py`
8. `trimmed_list.py`

## Dependencies
more-itertools 

pywin32

pypiwin32

numpy

To install dependencies: `pip install <dependencyname>`; ex: `pip install numpy`.
