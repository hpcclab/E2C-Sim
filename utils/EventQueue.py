'''
Authors: Ali Mokhtari, Chavit Denninnart
Created on Dec. 18, 2020.

In simulation mode, all events (e.g arriving a task or completing the 
task) are queued in EventQueue.In this way, the processing of a task
in real-world can be imitated. 
The EventQueue is firstly empty. By arriving the frist task, an event
which is "arriving a new task" is added to the head of queue. In the
same way, other events are added to the queue. Moreover, the queue is
always sorted based on the event's time. Heap sort technique is used
to sort the queue.

'''
import heapq



class Event:
    # An event explains different stages of processing a task, from
    # arriving to completing the task.
    #
    # event_type: The stage of processing a task like "arriving" or 
    # "completing" 
    # time: It is the time of occuring an event. For example,
    # time of arriving a task in "arriving" event.
    # event_details: a dictionary that describes the event in detail.
    
    def __init__(self, time , event_type, event_details):        
        self.time = time
        self.event_type = event_type
        self.event_details = event_details
        
    def __eq__(self, other):
        return self.time == other.time
    
    def __ne__(self, other):
        return self.time != other.time
    
    def __lt__(self,other):
        return self.time < other.time
    
    def __le__(self,other):
        return self.time <= other.time
    
    def __gt__(self,other):
        return self.time > other.time       
    
    def __ge__(self,other):
        return self.time >= other.time
    
    
class EventQueue:
    # All events are queued in EventQueue.
    #
    # event_list: It is the list of events in the queue. event_list has
    # Min-heap data struture. It can help sorting the queue based on the 
    # event.time with reseaonable time complexity.   
    
    
    event_list=[]
    # def __init__(self):
    #     self.event_list=[]
        
    def add_event(self,event):
        # Insert an event into the event_list.
        if isinstance(event, Event):
            heapq.heappush(self.event_list,event)
       
    def get_first_event(self):
        # it returns the root of event_list which is the event with 
        # smallest time.
        
        if self.event_list: # it checks that event_list is non-empty
            return heapq.heappop(self.event_list)
        else:            
            return Event(None,None,None)
    
    def remove(self,event):
        # It removes the event from the event_list. Then, the resulted
        # event_list is heapified again. 
        print(self.event_list)
        print('\n\n\n')
        self.event_list.remove(event)
        heapq.heapify(self.event_list)
        
        
def test():
    
    eq= EventQueue()  
    
    event1=Event(1,"e1",[])    
    event2=Event(5,"e2",[])
    event3=Event(2,"e3",[])
    event4=Event(3,"e4",[])
    
    eq.add_event(event1)
    eq.add_event(event2)    
    eq.add_event(event3) 
    eq.add_event(event4) 
    
    eq.remove(event4)
    eq.remove(event1)
    
    print(len(eq.event_list))
    print(eq.get_first_event().event_type)
    print(len(eq.event_list))
    print(eq.get_first_event().event_type)
    print(len(eq.event_list))
    print(eq.get_first_event().event_type)


#test()