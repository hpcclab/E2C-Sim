# E2C-Sim
## Introduction
This project simualtes the heterogeneous Edge-to-Cloud (E2C) environment. 
## How to Install and Execute the Project
Below, you can find the steps to execute the program:
1. Download Anaconda from ``` https://www.anaconda.com/products/distribution ``` and install it based on the instruction in Anaconda Webpage (https://docs.anaconda.com/anaconda/install/). Once the installation is done successfully, make sure to restart your terminal.
2. Clone the repository:
```git clone https://github.com/hpcclab/E2C-Sim.git ```
3. In this step, you create a new conda environment and name it ```simulator```. For this purpose, open terminal (or Anaconda Prompt for Winodws user) and type the below command:
   ```
    conda create --name simulator python=3.9
    ```
   Note that the comaptible python version with E2C is python3.9. 
4. Activate the environment in Anaconda prompt
   ```
   conda activate simulator
   ```
5. Install the latest version of pip in simulator environment as follows:
```
conda install -c anaconda pip
```
6. Then, you can use requirements.txt file to install required dependencies via pip:
```
pip install -r requirements.txt
```
7. Navigate to the E2C-Sim/V1 directory. Then, run the main.py within the V1 directory in simulator environemnt:
```
python main.py
```
8. You can directly access the simulation environment from **config.json** file. Task types and machines are initially defined in that JSON file. Considering the JSON format, you can easily modify, add, or delete machines or task types. Once the desired changes have been made, save the changed files and run python main.py to see the results in the window.
