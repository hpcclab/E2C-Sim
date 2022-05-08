# smartsight
## Introduction
This project includes the energy-efficient scheduler on the edge-tier of the SmartSight project 
## How to Install and Execute the Project
Below, you can find the steps to execute the program:
1. Clone the repository:
```git clone https://github.com/hpcclab/E2C-Sim.git ```
2. Run this command in ```V1.0``` directory to install required packages
   ```
    pip install -r requirements.txt
    ```
3. Within the ``` V1.0 ``` directory, open the ``` utils ``` folder.
4. Once there, you can run ``` main.py ``` directly with a default configuration.
5. To change the Config of the machines and task types, open ``` config.json ``` and add new task types in the same format present and increase or decrease the amount of each machine present as well as add new machine types etc also in the format present.
6. To change the arrival times and amount of incoming tasks, open ``` ./Episodes/oversubscription-2/medium-variance/ArrivalTime-<#>.txt ``` and once there, you can add or remove tasks in the same format already present.
7. Once the desired changes have been made, save the files changed and run ``` main.py ``` to see the results in the window
## How to Run the GUI
1. Go to ``` config.json ```, under Settings, set ```"gui":1```
2. Run ``` python main.py```
3. In the GUI, press **Start** to begin the simulation.
4. Once the simuation starts, you will see little squares animating in the GUI. Each of these squares represents a task.
5. Slide the slider to increase or decrease the speed.
6. Press **Pause** to pause and **Resume** to resume
7. End the simulation by pressing **End**. Ending the simulation will generate results for the simulation.
8. **Restart** button will close the GUI and reopen it.
9. **Machine Summary** will generate a table that contains all the machine statistics
10. **Full log** will display a window with scrollable box that contains full log that runs the simulator. You can filter the logs by **event type** with the drop down box or **task id** with the search bar. 
11. The **Details** buttons beside each machine will display the statistic of individual machine and all the finished tasks. 