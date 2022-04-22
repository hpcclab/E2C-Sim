from abc import ABCMeta


class MachineType:
    __metaclass__ = ABCMeta

    def __init__(self, id, name, power,idle_power, replicas):
        self.id = id
        self.name = name
        self.power = power
        self.idle_power = idle_power
        self.replicas = replicas
