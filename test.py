import sched
import time
  
  
# instance is created
scheduler = sched.scheduler(time.time, time.sleep)
  
# function to print time and
# name of the event
def print_event():
    print('EVENT:')
  
# printing starting time
print ('START:', time.time())
  
# first event with delay 
# of 1 second
e1 = scheduler.enter(1, 1, print_event)
  
  
# second event with delay 
# of 2 seconds
e2 = scheduler.enter(2, 1, print_event)
  
# removing 1st event from 
# the event queue
#scheduler.cancel(e1)
  
# executing the events
scheduler.run()