# E2C-Sim
## Introduction
This project simualtes the heterogeneous Edge-to-Cloud (E2C) environment. 
## How to Install and Execute the Project
Below, you can find the steps to execute the program:
1. Download Anaconda from ``` https://www.anaconda.com/products/distribution ``` and install it based on the instruction in Anaconda Webpage (https://docs.anaconda.com/anaconda/install/).
2. Clone the repository:
```git clone https://github.com/hpcclab/E2C-Sim.git ```
3. Go to the ```E2C-Sim/V1``` directory and run the following command to install required packages (Linux users may need to run `conda env export --no-builds > environment.yml` prior to this command)
   ```
    conda env create -f environment.yml
    ```
4. Activate the environment in Anaconda prompt
   ```
   conda activate simulator
   ```
4. Within the ``` V1 ``` directory, you can run ``` main_gui.py ``` directly with a default configuration.
5. To change the Config of the machines and task types, open ``` config.json ``` and add new task types in the same format present and increase or decrease the amount of each machine present as well as add new machine types etc also in the format present.
6. Once the desired changes have been made, save the files changed and run ``` main_gui.py ``` to see the results in the window 
