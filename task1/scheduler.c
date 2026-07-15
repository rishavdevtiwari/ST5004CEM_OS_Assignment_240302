#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <pthread.h>
#include <stdint.h>

#ifdef _WIN32
#include <windows.h>
#define sleep_sec(x) Sleep((DWORD)((x) * 1000))
#define sleep_ms(x) Sleep((DWORD)(x))
#else
#include <unistd.h>
#define sleep_sec(x) usleep((useconds_t)((x) * 1000000))
#define sleep_ms(x) usleep((useconds_t)((x) * 1000))
#endif

// Task 1.1 simple PCB struct to track process state and remaining time
typedef struct {
    int pid;
    char name[32];
    double burst_time;
    double remaining_time;
    char state[16]; // tracking state transitions here
} ProcessPCB;

// mutex lock for shared console print issues
pthread_mutex_t log_lock = PTHREAD_MUTEX_INITIALIZER; // standard mutex for shared console print issues
// locked resources for demonstration of deadlock scenario
pthread_mutex_t lock_a = PTHREAD_MUTEX_INITIALIZER;
pthread_mutex_t lock_b = PTHREAD_MUTEX_INITIALIZER;

void safe_print(const char *msg) {
    // safe zone starts here so logs don't mess up
    pthread_mutex_lock(&log_lock);
    printf("%s\n", msg);
    fflush(stdout);
    // releasing the lock after writing safely
    pthread_mutex_unlock(&log_lock);
}

typedef struct {
    ProcessPCB *process;
    double quantum;
} ThreadArgs;

// worker thread target func simulating workload execution
void *run_process_slice(void *arg) {
    ThreadArgs *targs = (ThreadArgs *)arg;
    ProcessPCB *current = targs->process;
    double quantum = targs->quantum;
    char log_buf[256];

    // spawning worker threads here to execute a slice of work
    snprintf(log_buf, sizeof(log_buf), "[RUNNING] -> PID %d is entering execution track.", current->pid);
    safe_print(log_buf);

    // calculate run slice durations manually
    double run_time;
    if (current->remaining_time > quantum) {
        run_time = quantum;
    } else {
        run_time = current->remaining_time;
    }

    sleep_sec(run_time);
    current->remaining_time -= run_time;

    if (current->remaining_time <= 0.001) {
        current->remaining_time = 0;
        strcpy(current->state, "TERMINATED");
        snprintf(log_buf, sizeof(log_buf), "[FINISHED] -> PID %d is fully done.", current->pid);
        safe_print(log_buf);
    } else {
        strcpy(current->state, "READY");
        snprintf(log_buf, sizeof(log_buf), "[PREEMPTED] -> PID %d put back into queue.", current->pid);
        safe_print(log_buf);
    }

    return NULL;
}

typedef struct {
    int thread_num;
    pthread_mutex_t *first_lock;
    pthread_mutex_t *second_lock;
} DeadlockArgs;

// deadlock scenario demonstration function
void *broken_deadlock_routine(void *arg) {
    DeadlockArgs *dargs = (DeadlockArgs *)arg;
    char log_buf[256];

    snprintf(log_buf, sizeof(log_buf), "[DEADLOCK-WARN] -> thread %d checking locks.", dargs->thread_num);
    safe_print(log_buf);

    pthread_mutex_lock(dargs->first_lock);
    snprintf(log_buf, sizeof(log_buf), "[DEADLOCK-WARN] -> thread %d holding resource 1.", dargs->thread_num);
    safe_print(log_buf);

    sleep_ms(200); // force context switch to trigger deadlock scenario cleanly

    pthread_mutex_lock(dargs->second_lock); // system locks here permanently if unmitigated
    safe_print("secured both resources successfully.");

    pthread_mutex_unlock(dargs->second_lock);
    pthread_mutex_unlock(dargs->first_lock);
    return NULL;
}

// deadlock preventation implementation
void *handle_resources_safely(void *arg) {
    DeadlockArgs *dargs = (DeadlockArgs *)arg;
    char log_buf[256];

    snprintf(log_buf, sizeof(log_buf), "[DEADLOCK-TEST] -> thread %d trying to grab locks safely.", dargs->thread_num);
    safe_print(log_buf);

    // strict lexical sorting order enforcement ensures no circular wait can form
    // we sort based on memory addresses of the mutex lock instances
    pthread_mutex_t *lock_1;
    pthread_mutex_t *lock_2;

    if ((uintptr_t)dargs->first_lock < (uintptr_t)dargs->second_lock) {
        lock_1 = dargs->first_lock;
        lock_2 = dargs->second_lock;
    } else {
        lock_1 = dargs->second_lock;
        lock_2 = dargs->first_lock;
    }

    // grabbing first resource in order
    pthread_mutex_lock(lock_1);
    snprintf(log_buf, sizeof(log_buf), "[DEADLOCK-TEST] -> thread %d got lock number 1.", dargs->thread_num);
    safe_print(log_buf);

    sleep_ms(100); // tiny delay to prove that cross-over circular wait is completely avoided

    // grabbing second resource in order
    pthread_mutex_lock(lock_2);
    snprintf(log_buf, sizeof(log_buf), "[DEADLOCK-TEST] -> thread %d got both locks smoothly!", dargs->thread_num);
    safe_print(log_buf);

    // releasing both allocations properly
    pthread_mutex_unlock(lock_2);
    pthread_mutex_unlock(lock_1);

    return NULL;
}

int main(void) {
    // creating 3 explicit processes matching requirements
    ProcessPCB my_tasks[3] = {
        {101, "Task-A", 0.9, 0.9, "READY"},
        {102, "Task-B", 0.3, 0.3, "READY"},
        {103, "Task-C", 1.1, 1.1, "READY"}
    };

    double quantum = 0.4;
    ProcessPCB *rem_queue[100];
    int queue_size = 3;
    for (int i = 0; i < 3; i++) {
        rem_queue[i] = &my_tasks[i];
    }

    // scheduling loop keeps spinning until all work items are cleared
    while (queue_size > 0) {
        // pulling the next process from our queue
        ProcessPCB *current = rem_queue[0];
        for (int i = 0; i < queue_size - 1; i++) {
            rem_queue[i] = rem_queue[i + 1];
        }
        queue_size--;

        // wrapping execution in a thread
        // context switching to a thread execution context block
        pthread_t worker_thread;
        ThreadArgs targs = {current, quantum};

        pthread_create(&worker_thread, NULL, run_process_slice, &targs);

        // waiting for child process created previously to wind down safely
        pthread_join(worker_thread, NULL);

        if (strcmp(current->state, "TERMINATED") != 0) {
            rem_queue[queue_size++] = current;
        }
    }

    safe_print("\n testing out experimental deadlock simulaton");

    // spin up two competing threads passing identical locks in reversed order
    pthread_t thread1, thread2;
    DeadlockArgs dargs1 = {1, &lock_a, &lock_b};
    DeadlockArgs dargs2 = {2, &lock_b, &lock_a};

    pthread_create(&thread1, NULL, handle_resources_safely, &dargs1);
    pthread_create(&thread2, NULL, handle_resources_safely, &dargs2);

    // waiting for child processes created previously to wind down safely
    pthread_join(thread1, NULL);
    pthread_join(thread2, NULL);

    safe_print("deadlock test finished successfully without any issues.");
    return 0;
}
