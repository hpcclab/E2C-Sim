# E2C-Sim
## Introduction
This project simualtes the heterogeneous Edge-to-Cloud (E2C) environment and this document focuses on the E2C installation. You can find more extensive documentation and tutorial of this project at: https://hpcclab.github.io/E2C-Sim-docs/#/.
Also, you can refer to [E2C YouTube channel to watch its tutorial videos](https://youtube.com/playlist?list=PL7jhdCPVrCHh49PvIglDEY2Xs4v2ivrsw&si=S3m-nZetf96BBmks). 
## How to Install and Execute the Project
Below, you can find the steps to execute the program:
1. Download Anaconda from ``` https://www.anaconda.com/products/distribution ``` and install it based on the instruction in Anaconda Webpage (https://docs.anaconda.com/anaconda/install/). Once the installation is done successfully, make sure to restart your terminal.
2. Clone the repository:
```git clone https://github.com/hpcclab/E2C-Sim.git ```
3. Run the following command to create a new environment via conda and name it simulator. For this purpose, open terminal (or Anaconda Prompt for Winodws user) and type the below command: 
   ```
    conda create --name simulator python=3.9
    ```
    Note that the python version in simulator environment is 3.9.
    
4. Activate the environment in Anaconda prompt
   ```
   conda activate simulator
   ```
5. Install the latest version of pip in simulator environment as follows:
   ```
   conda install -c anaconda pip
   ```
6. Navigate to ```E2C-Sim/V1/
7. Then, you can use requirements.txt file to install required dependencies via pip:
   ```
      pip install -r requirements.txt

    ```
8. Within the ``` V1 ``` directory, you can run ``` main.py ``` directly with a default configuration:
   ```
   python main.py
   ```
 
10. To change the config of the machines and task types, open ```config.json``` and add new task types in the same format present and increase or decrease the amount of each machine present as well as add new machine types etc also in the format present. Once the desired changes have been made, save the changed files and run python main.py to see the results in the window.window 
