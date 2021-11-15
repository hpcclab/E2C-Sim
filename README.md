# smartsight
## Introduction
This project includes the energy-efficient scheduler on the edge-tier of the SmartSight project 
## How to Install and Execute the Project
Below, you can find the steps to execute the program:
1. Clone the repository:
```git clone https://github.com/hpcclab/smartsight.git ```
2. Within the ``` V1.0 ``` directory, open the ``` utils ``` folder.
3. Once there, you can run ``` main.py ``` directly with a default configuration.
4. To change the Config of the machines and task types, open ``` config.json ``` and add new task types in the same format present and increase or decrease the amount of each machine present as well as add new machine types etc also in the format present.
5. To change the arrival times and amount of incoming tasks, open ``` ./Episodes/oversubscription-2/medium-variance/ArrivalTime-<#>.txt ``` and once there, you can add or remove tasks in the same format already present.
6. Once the desired changes have been made, save the files changed and run ``` main.py ``` to see the results in the window
