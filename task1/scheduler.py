import sys
import threading
import time

# Task 1.1 simple PCB class to track process state and remaining time
class ProcessPCB:
    def __init__(self, pid, name, burst_time):
        self.pid = pid
        self.name = name
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.state = "READY" # tracking state transitions here

if __name__ == "__main__":
    # creating 3 explicit processes matching requirements[cite: 1, 2]
    my_tasks = [
        ProcessPCB(101, "Task-A", 0.9),
        ProcessPCB(102, "Task-B", 0.3),
        ProcessPCB(103, "Task-C", 1.1)
    ]
    
    quantum = 0.4
    rem_queue = list(my_tasks) # making a copy to iterate over loop mechanics
    
    # scheduling loop keeps spinning until all work items are cleared
    while len(rem_queue) > 0:
        # pulling the next process from our queue
        current = rem_queue.pop(0)
        
        print("[RUNNING] -> PID " + str(current.pid) + " is entering execution track.")
        
        # calculate run slice durations manually
        if current.remaining_time > quantum:
            run_time = quantum
        else:
            run_time = current.remaining_time
            
        time.sleep(run_time)
        current.remaining_time -= run_time
        
        if current.remaining_time <= 0:
            current.state = "TERMINATED"
            print("[FINISHED] -> PID " + str(current.pid) + " is fully done.")
        else:
            current.state = "READY"
            print("[PREEMPTED] -> PID " + str(current.pid) + " put back into queue.")
            rem_queue.append(current)