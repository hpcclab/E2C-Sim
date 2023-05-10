import os
import sqlite3 as sq
from random import uniform
import pandas as pd
from utils.utilities import *

CURR_PATH = os.getcwd()
MACHINE_PATH = CURR_PATH + '/Data/Default/machineTypes.csv'
TASK_PATH = CURR_PATH + '/utils/taskTypes.csv'
EET_PATH = CURR_PATH + '/Data/Default/eet.csv'
DIST_PATH = CURR_PATH + '/utils/distribution.csv'
MIN_EX = 0.01
MAX_EX = 1.0



def initTables(cur, conn):
    # Remove all tables just b/c
    # --------------------------------------------------------------
    cur.execute("SELECT * FROM sqlite_master where type = 'table';")
    tables_raw = cur.fetchall()
    tables = []
    for table in tables_raw: tables.append(table[1])
    deleteTables(cur, conn, tables)

    # Create schemas
    # --------------------------------------------------------------
    # Machine Types
    # Pre-defined table of machine types and their characteristics.
    machine_types = """ CREATE TABLE IF NOT EXISTS machine_types (
        machine_id INT PRIMARY KEY,
        machine_name VARCHAR(255) NOT NULL,
        no_of_replicas INT NOT NULL,
        idle_power FLOAT NOT NULL,
        max_power FLOAT NOT NULL,
        num_of_cores INT NOT NULL,
        cpu_clock FLOAT NOT NULL,
        memory FLOAT NOT NULL
    ); """

    #workload for old e2c
    workload = """ CREATE TABLE IF NOT EXISTS workload(
        task_type INT,
        arrival_time FLOAT
    );"""

    # Task Types
    # Pre-defined table of task types and their characteristics.
    task_types = """ CREATE TABLE IF NOT EXISTS task_types (
        task_id INT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        detail VARCHAR(255) NOT NULL,
        urgency FLOAT NOT NULL
    ); """

    # Expected Execution Time
    # Derived from task_types & machine_types.
    # Each entry contained expected execution time of task type on given
    # machine type.
    # eet = """ CREATE TABLE IF NOT EXISTS eet (
    #     task_id INT NOT NULL,
    #     machine_id INT NOT NULL,
    #     expected_ex_time FLOAT NOT NULL,

    #     FOREIGN KEY (task_id) REFERENCES task_types(task_id),
    #     FOREIGN KEY (machine_id) REFERENCES machine_types(machine_id)
    # ); """
    eet = """ CREATE TABLE IF NOT EXISTS eet (
        '' VARCHAR(255) NOT NULL,
        m1 FLOAT NOT NULL,
        m2 FLOAT NOT NULL,
        m3 FLOAT NOT NULL
    ); """

    # Scenario
    # Characterization of distribution of tasks.
    scenario = """ CREATE TABLE IF NOT EXISTS scenario (
        task_id INT NOT NULL,
        start_time FLOAT NOT NULL,
        end_time FLOAT NOT NULL,
        num_of_tasks INT NOT NULL,
        dist_id INT NOT NULL,
        FOREIGN KEY (task_id) REFERENCES task_types(task_id),
        FOREIGN KEY (dist_id) REFERENCES distribution(dist_id)
    ); """

    # Distribution
    # Possible distribution schemes for task scenarios.
    distribution = """ CREATE TABLE IF NOT EXISTS distribution (
        dist_id INT PRIMARY KEY,
        name VARCHAR(255) NOT NULL
    ); """

    schemas = [
        machine_types,
        task_types,
        eet,
        scenario,
        distribution,
        workload   
    ]

    # Set up schemas
    createSchema(cur, conn, schemas)

    # Fill each table from default files
    # --------------------------------------------------------------
    # --- machine_types ---
    # machine_data = fromCSV(MACHINE_PATH)
    # insertData(cur, conn, machine_data, 'machine_types')

    # --- task_types ---
    task_data = fromCSV(TASK_PATH)
    insertData(cur, conn, task_data, 'task_types')

    # --- distribution ---
    dist_data = fromCSV(DIST_PATH)
    insertData(cur, conn, dist_data, 'distribution')

    # --- eet ---
    # This table is derived from task_types and machine_types
    task_type_df = pd.read_sql_query(f'SELECT * FROM task_types', conn)
    machine_type_df = pd.read_sql_query(f'SELECT * FROM machine_types', conn)

    # Cartesian product of task_types and machine_types
    # (only using attributes we need)
    eet_list_buff = [
        (tt, mt) \
        for tt, _, _, _ in task_type_df.values.tolist() \
        for mt, _, _, _, _, _, _, _ in machine_type_df.values.tolist()
    ]

    # Insert randomized eet value for each tuple
    eet_list = []
    for entry in eet_list_buff:
        rnd = round(uniform(MIN_EX, MAX_EX), 2)
        eet_list.append(entry + (rnd, ))

    # Insert data to the eet table
    # insertData(cur, conn, eet_list, 'eet')