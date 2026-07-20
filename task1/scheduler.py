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

# mutex lock for shared console print issues
shared_log = []
log_lock = threading.Lock() # standard mutex for shared console print issues
#locked resources for demonstration of deadlock scenario
lock_a = threading.Lock()
lock_b = threading.Lock()

def safe_print(msg):
    # safe zone starts here so logs don't mess up
    log_lock.acquire()
    try:
        shared_log.append(msg)
        print(msg)
    finally:
        # releasing the lock after writing safely
        log_lock.release()

# worker thread target func simulating workload execution
def run_process_slice(current, quantum):
    # spawning worker threads here to execute a slice of work
    safe_print("[RUNNING] -> PID " + str(current.pid) + " is entering execution track.")
    
    # calculate run slice durations manually
    if current.remaining_time > quantum:
        run_time = quantum
    else:
        run_time = current.remaining_time
        
    time.sleep(run_time)
    current.remaining_time -= run_time
    
    if current.remaining_time <= 0:
        current.state = "TERMINATED"
        safe_print("[FINISHED] -> PID " + str(current.pid) + " is fully done.")
    else:
        current.state = "READY"
        safe_print("[PREEMPTED] -> PID " + str(current.pid) + " put back into queue.")

#deadlock scenario demonstration function
def broken_deadlock_routine(thread_num, first_lock, second_lock):
    safe_print("[DEADLOCK-WARN] -> thread " + str(thread_num) + " checking locks.")
    first_lock.acquire()
    safe_print("[DEADLOCK-WARN] -> thread " + str(thread_num) + " holding resource 1.")
    time.sleep(0.2) # force context switch to trigger deadlock scenario cleanly
    second_lock.acquire() # system locks here permanently if unmitigated
    try:
        safe_print("secured both resources successfully.")
    finally:
        second_lock.release()
        first_lock.release()


#deadlock preventation implementation 

def handle_resources_safely(thread_num, first_lock, second_lock):
    safe_print("[DEADLOCK-TEST] -> thread " + str(thread_num) + " trying to grab locks safely.")

    # strict lexical sorting order enforcement ensures no circular wait can form[cite: 1]
    # we sort based on internal python memory ids of the lock instances
    if id(first_lock) < id(second_lock):
        lock_1 = first_lock
        lock_2 = second_lock
    else:
        lock_1 = second_lock
        lock_2 = first_lock

    # grabbing first resource in order
    lock_1.acquire()
    safe_print("[DEADLOCK-TEST] -> thread " + str(thread_num) + " got lock number 1.")
    time.sleep(0.1)  # tiny delay to prove that cross-over circular wait is completely avoided

    # grabbing second resource in order
    lock_2.acquire()
    try:
        safe_print("[DEADLOCK-TEST] -> thread " + str(thread_num) + " got both locks smoothly!")
    finally:
        # releasing both allocations properly
        lock_2.release()
        lock_1.release()


if __name__ == "__main__":
    # creating 3 explicit processes matching requirements
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
        
        # wrapping execution in a thread
        # context switching to a thread execution context block
        t = threading.Thread(target=run_process_slice, args=(current, quantum))
        t.start()
        
        # waiting for child process created previously to wind down safely
        t.join()
        
        if current.state != "TERMINATED":
            rem_queue.append(current)
            
    safe_print("\n testing out experimental deadlock simulaton")
    # this call structure will freeze up if both run actively at the same time
    # t_dead1 = threading.Thread(target=broken_deadlock_routine, args=(1, lock_a, lock_b))
    # t_dead2 = threading.Thread(target=broken_deadlock_routine, args=(2, lock_b, lock_a))
    # spin up two competing threads passing identical locks in reversed order
    thread1 = threading.Thread(target=handle_resources_safely, args=(1, lock_a, lock_b))
    thread2 = threading.Thread(target=handle_resources_safely, args=(2, lock_b, lock_a))

    thread1.start()
    thread2.start()

    # waiting for child processes created previously to wind down safely
    thread1.join()
    thread2.join()
    safe_print("deadlock test finished successfully without any issues.")