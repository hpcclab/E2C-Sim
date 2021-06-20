# smartsight
## Introduction
This project includes the energy-efficient scheduler on the edge-tier of the SmartSight project 
## How to Install and Execute the Project
Below, you can find the steps to execute the program:
1. Clone the repository:
```git clone https://github.com/hpcclab/smartsight.git ```
2. Within the ``` simulater_v1 ``` directory, open the ``` utils ``` folder.
3. Once there, you can run ``` main.py ``` directly with a default configuration.
4. To change the Config of the machines and task types, open ``` config.json ``` and add new task types in the same format present and increase or decrease the amount of each machine present as well as add new machine types etc also in the format present.
5. To change the arrival times and amount of incoming tasks, open ``` ArrivalTimes.txt ``` and once there, you can add or remove tasks in the same format already present.
6. Inside of ``` main.py ```, the scheduling algorithm can also be changed. To do so, open ``` main.py ``` and on line 120, change the algorithm the scheduler is based on and run.
7. To change to 2 phase scheduling, open ``` main.py ``` and once there, uncomment the section thats titled "Code for phase 2 Scheduling" which starts at line 66 and ends on line 118. After its uncommented, you must comment out the code for one phase scheduling which starts at line 120 and ends on line 182
8. To then change the algorithms for 2 phase scheduling, inside of ``` main.py ```, change the algorithm that the scheduler1 and scheduler2 variables are set to 
9. Once the desired changes have been made, save the files changed and run ``` main.py ``` to see the results in the window
