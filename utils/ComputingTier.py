# -*- coding: utf-8 -*-
"""
Created on Wed Jan 27 12:14:57 2021

@author: Ali
"""


class ComputingUnit:
    
        
    def __init__(self, id,initial_energy, power_limit,network_bandwidth):
                
        self.id = int(id)
        self.machines = []
        self.total_power = 0.0
        self.power_limit = float(power_limit)
        self.initial_energy = float(initial_energy)
        self.network_bandwidth = float(network_bandwidth)
        self.available_energy = float(initial_energy)
        
    
    def add_machine(self, machine):
        
        added_power = float(machine.spec_detail['dynamic_power'])
        
        if ( self.total_power + added_power ) < float(self.power_limit):
            
            print('\t\t Added Machine => id: '+str(machine.machine_id)+
                  ' Type: '+ machine.machine_type )            
            self.machines.append(machine)
            self.total_power += added_power
            
        else:
            # Later it should raise an error
            print("\t\t !!! The machine "+  str(machine.machine_id) +
                  'with the' +machine.machine_type+'type cannot be added' +
                  'to the computing unit' + self.id +
                  ' because power is exceeded the power limit')
    
    def remove_machine(self, machine):
        print('\n machine '+str(machine.machine_id)+
              ' with the '+machine.machine_type+' type is removed from '+
                  'computing unit '+self.id)
        self.machines.remove(machine)
        self.total_power -= float(machine.spec_detail['dynamic_power'])
        
    def deduct_energy(self, energy):
        self.available_energy -= energy


class ComputingTier:
    
    def __init__(self, name):
        self.name = str(name)
        self.computing_units = []
        self.initial_energy = 0.0
        self.available_energy = 0.0
        
    def add_computing_unit(self, computing_unit):
        self.computing_units.append(computing_unit)
        self.available_energy += computing_unit.available_energy
        self.initial_energy += computing_unit.initial_energy
    
    def remove_computing_unit(self, computing_unit):
        self.computing_units.remove(computing_unit)
        self.available_energy -= computing_unit.available_energy
        self.initial_energy -= computing_unit.initial_energy
        
    
            
    
    
        
        


