"""
Author: Ali Mokhtari (ali.mokhtaary@gmail.com)
Created on Nov., 15, 2021


"""

from utils.base_task import TaskStatus
from utils.base_scheduler import BaseScheduler
import utils.config as config
from utils.queue import Queue
import time


class FCFS(BaseScheduler):


    def __init__(self, total_no_of_tasks):
        super(FCFS, self).__init__()
        self.name = 'FCFS'
        self.total_no_of_tasks = total_no_of_tasks
        self.prev_assignment_idx = -1
        self.sleep_time = 0.1



    def choose(self, index=0):

        task = self.batch_queue.get(index)
        self.unmapped_task.append(task)

        if config.gui==1:
            self.decision.emit({'type':'choose',
                                'time':config.time.gct(),
                                'where':'simulator: choose',
                                'data': {'task':task,
                                        'bq_indx': index,
                                        },
                                        })
            time.sleep(self.sleep_time)

        if config.settings['verbosity']:
            s =f'\n{task.id} selected --> BQ = '
            bq = [t.id for t in self.batch_queue.list]
            s += f'{bq}'
            s += f'\nexecutime: {task.execution_time}'
            s += f'\testimeated_time{task.estimated_time}'

            config.log.write(s)

        return task


    def defer(self, task):
        if config.time.gct() > task.deadline:
            self.drop(task)
            return 1

        if config.gui==1:
                self.decision.emit({'type':'defer',
                                'time':config.time.gct(),
                                'where':'simulator: defer',
                                'data': {'task':task,
                                        },
                                        })
                time.sleep(self.sleep_time)
        task.status =  TaskStatus.DEFERRED
        task.no_of_deferring += 1
        self.batch_queue.put(task)

        self.stats['deferred'].append(task)
        if config.settings['verbosity']:
            s = '\n[ Task({:}),  _________ ]: Deferred       @time({:3.3f})'.format(
            task.id, config.time.gct())
            config.log.write(s)



    def drop(self, task):
        task.status = TaskStatus.CANCELLED
        task.drop_time = config.time.gct()
        self.stats['dropped'].append(task)
        if config.gui==1:
            self.decision.emit({'type':'cancelled',
                                'time':config.time.gct(),
                                'where':'simulator: drop',
                                'data': {'task':task,
                                        },
                                        })
            time.sleep(self.sleep_time)
        if config.settings['verbosity']:
            s = '\n[ Task({:}),  _________ ]: Cancelled      @time({:3.3f})'.format(
                task.id, config.time.gct()       )
            config.log.write(s)


    def map(self, machine):
        task = self.unmapped_task.pop()
        assignment,_ = machine.admit(task)
        if assignment != 'notEmpty':
            if config.gui==1:
                self.decision.emit({'type':'map',
                                'time':config.time.gct(),
                                'where':'scheduler: map',
                                'data': {'task':task,
                                         'assigned_machine':machine,
                                        },
                                        })
                time.sleep(self.sleep_time)
            task.assigned_machine = machine
            self.stats['mapped'].append(task)
            s = f"\ntask:{task.id}  assigned to:{task.assigned_machine.type.name}  delta:{task.deadline}"
            config.log.write(s)
        else:
            self.unmapped_task.append(task)


    def first_available_machine(self):

        for machine in config.machines:

            if not machine.is_working():
                return machine

        min_qlen = float('inf')
        min_qlen_machine = None
        for machine in config.machines:

            if (not machine.queue.full()) and machine.queue.qsize() < min_qlen:
                min_qlen = machine.queue.qsize()
                min_qlen_machine = machine

        return min_qlen_machine




    def schedule(self):


        if config.settings['verbosity']:
            s = f'\n Current State @{config.time.gct()}'
            s = '\nBQ = '
            bq = [t.id for t in self.batch_queue.list]
            s += f'{bq}'
            s += '\n\nMACHINES ==>>>'
            for m in config.machines:
                s += f'\n\tMachine {m.type.name} :'
                if m.running_task:
                    r = [m.running_task[0].id]
                else:
                    r = []
                mq = [t.id for t in m.queue.list]
                r.append(mq)
                s +=f'\t{r}'
            config.log.write(s)

        if self.batch_queue.empty():
            return None

        machine_index = (self.prev_assignment_idx+1) % config.no_of_machines
        print(50*'*')
        print(config.machines)
        print(m.type.name for m in config.machines)
        machine = config.machines[machine_index]
        self.prev_assignment_idx = machine_index
        #available_machine = self.first_available_machine()
        available_machine = machine
        if available_machine != None:
            self.choose()
            self.map(available_machine)
            return available_machine



