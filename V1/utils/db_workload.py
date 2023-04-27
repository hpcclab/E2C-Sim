import random
import sys
import sqlite3 as sq
import pandas as pd
import numpy as np
from utils.utilities import *

# Develop and propagate workload table
# createWorkload(Cursor, Connection, int)
def createWorkload(cur, conn, num_wl):
    init(cur, conn)

    # Fetch from scenario table
    scenario_df = pd.read_sql_query('SELECT * FROM scenario', conn)

    # for count in range(num_wl):
    # DEBUG
    # print(f'Count: {count}')
    t_instances = {}
    # For each scenario create list of distributed instances
    row_id = 1
    for _, row in scenario_df.iterrows():
        task_id = row['task_id']
        start_time = float(row['start_time'])
        end_time = float(row['end_time'])
        num_of_tasks = int(row['num_of_tasks'])
        dist_id = row['dist_id']
        cur.execute(f"SELECT name FROM task_types WHERE task_id = '{task_id}';")
        task_name = cur.fetchall() # Returns list so must processess further
        try:
            task_name = task_name[0][0]
        except IndexError:
            print(
                f'(workload.py) Unknown task_id found in scenario table: {task_id}\n'
                'Double check scenario and task_types tables.\n'
                'Skipping for now...'
            )
            continue

        # ***
        # print(f'(workload.py) dist_id: {dist_id}')

        t_instances[(task_id, row_id, task_name)] = \
            fetchArrivals(start_time, end_time, num_of_tasks, dist_id, cur)

        row_id += 1
        # ***
        # print(f'(workload.py) t_instances: {t_instances[(task_id, scenario_id, task_name)]}')

    # Create workload local list
    workload = []
    for scenario_key in t_instances:
        task_id = scenario_key[0]
        task_name = scenario_key[2]
        for arrival_time in t_instances[scenario_key]:
            entry = (task_id, task_name, arrival_time)
            workload.append(entry)

    # Sort list by arrival_time
    workload.sort(key = lambda x: x[2])

    # Needed to sort before adding work_id
    instance_id = 1
    for i in range(len(workload)):
        entry = workload[i]
        entry = (instance_id,) + entry
        workload[i] = entry
        instance_id += 1

    # Create workload schema
    # workload_schema = f""" CREATE TABLE IF NOT EXISTS workload{count+1} (
    #     instance_id INT PRIMARY KEY,
    #     task_id INT NOT NULL,
    #     name VARCHAR(255) NOT NULL,
    #     arrival_time FLOAT NOT NULL,

    #     FOREIGN KEY (task_id) REFERENCES task_types(task_id)
    # ); """
    workload_schema = f""" CREATE TABLE IF NOT EXISTS workload (
        task_id INT NOT NULL,
        arrival_time FLOAT NOT NULL,

        FOREIGN KEY (task_id) REFERENCES task_types(task_id)
    ); """
    createSchema(cur, conn, workload_schema)

    # ***
    # for tuple in workload:
    #     for idx in tuple: print(f'{idx}: {type(idx)}')
    #     break
    # conn.close()
    # sys.exit()

    # Merge list into workload table
    insertData(cur, conn, workload, 'workload')

def get_data_sizes(data_size,stdv,num_of_tasks):
        return (np.random.normal(data_size, stdv, num_of_tasks)).tolist()

# Creates list of task instances from distribution scheme
# [int] fetchArrivals(float, float, int, int, Cursor)
def fetchArrivals(start_time, end_time, num_of_tasks, dist_id, cur):
    cur.execute(f"SELECT name FROM distribution WHERE dist_id = '{dist_id}';")
    dist_name = cur.fetchall()
    
    dist_name = dist_name[0][0]

    if dist_name == 'exponential':
        beta = (end_time - start_time) / num_of_tasks
        interarrival = np.random.exponential(
                       beta, num_of_tasks)
        distribution = start_time + np.cumsum(interarrival)        
        distribution = [round(x, 3) for x in distribution]

        return distribution
    elif dist_name == 'uniform':
        distribution = np.random.uniform(start_time, end_time,
                                         num_of_tasks)
        distribution = [round(x, 3) for x in distribution]

        return distribution
    elif dist_name == 'normal':
        mu = (start_time + end_time) / 2.0
        sigma = (end_time - start_time) / 6.0

        distribution = np.random.normal(mu, sigma, num_of_tasks)
        distribution[distribution > end_time] = end_time
        distribution[distribution < start_time] = start_time
        
        distribution = [round(x, 3) for x in distribution]

        return distribution
    elif dist_name == 'spiky':
        #hard-coded in for the time being
        no_of_spikes = 10

        # Here, tasks are considered to be arrived in spiky manner. The spikes
        # occurred at random positions but have same width.
        # The number of tasks arrive at each spike is also a random variable.
        # no_of_spikes: It is the number of spikes in the given time
        # interval [start_time, end_time]

        # Each spike width is 1% of the time interval.
        spike_width = 0.01 * (end_time - start_time)
        # Each spike begins at a random position which is drawn from a 
        # uniform distribution.
        if isinstance(no_of_spikes, int):
            spike_starts = np.random.uniform(start_time,
                                             end_time, no_of_spikes)
            distribution = []
            # remaining_tasks is the number of tasks that arrive afterward.
            remaining_tasks = num_of_tasks
            # A loop to generate spikes sequentially
            for spikes_no in range(no_of_spikes):
                # no_of_tasks_in_spike: Number of tasks arrive at each spike
                no_of_tasks_in_spike = np.random.randint(remaining_tasks + 1)
                # spike: distribution of tasks arrival time in each spike
                spike = np.random.uniform(spike_starts[spikes_no],
                                          spike_starts[spikes_no] + spike_width,
                                          no_of_tasks_in_spike)
                remaining_tasks -= no_of_tasks_in_spike
                distribution = np.concatenate((distribution, spike))
            distribution = [round(x, 3) for x in distribution]

            return distribution
        else:
            print("Invalid amount of spikes.")
            sys.exit()


def init(cur, conn):
    # Obtain list of all tables
    cur.execute("SELECT * FROM sqlite_master where type = 'table';")
    tables_raw = cur.fetchall()
    tables = []
    for table in tables_raw: tables.append(table[1])

    # Delete all previous workload tables
    for table in tables:
        if 'workload' in table:
            deleteTables(cur, conn, table)