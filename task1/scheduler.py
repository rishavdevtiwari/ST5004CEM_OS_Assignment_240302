import sys
import threading
import time

# --- TASK 1.1: MOCK PCB STATE ---
# standard python variables for now instead of full objects
p1_rem = 0.9
p2_rem = 0.3
p3_rem = 1.1


def simple_worker(name, run_time):
    # spawning worker threads here to execute a slice of work
    print("[RUNNING] -> " + name + " started execution.")
    time.sleep(run_time)  # testing sleep for CPU simulation
    print("[FINISHED] -> " + name + " is done.")


if __name__ == "__main__":
    # creating 3 explicit processes matching requirements
    t1 = threading.Thread(target=simple_worker, args=("Task-A", p1_rem))
    t2 = threading.Thread(target=simple_worker, args=("Task-B", p2_rem))
    t3 = threading.Thread(target=simple_worker, args=("Task-C", p3_rem))

    t1.start()
    t2.start()
    t3.start()

    # waiting for child processes created previously to wind down safely
    t1.join()
    t2.join()
    t3.join()
    print("day 1 script finished.")