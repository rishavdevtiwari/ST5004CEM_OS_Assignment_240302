# ST5004CEM Operating Systems and Security Coursework

Welcome to the ST5004CEM Operating Systems and Security assignment repository. This repository contains complete, functional implementations in the **C language** for Tasks 1 through 4.

---

## Repository Overview

This project implements core operating system and security concepts:

- **task1/ (`scheduler.c`)**: Demonstrates process creation, Round-Robin CPU scheduling simulation, POSIX thread management (`pthread`), and deadlock prevention using memory-address sorting.
- **task2/ (`memory_sim.c`)**: Simulates virtual memory paging, address translation (`virtual_address / PAGE_SIZE`), and compares **FIFO** and **LRU** page replacement algorithms with hit/miss performance ratios.
- **task3/ (`secure_fs.c`)**: Implements a secure file system with SHA-256 user password authentication, byte-level XOR stream cipher encryption at rest, POSIX-like RWX access control rules (`owner:group:others`), and timestamped action tracking in `audit.log`.
- **task4/ (`server.c` & `client.c`)**: A multi-threaded TCP socket client-server application demonstrating Inter-Process Communication (IPC) over port `9090`, JSON packet envelopes, and authentication handshake token checks.

---

## How to Compile & Run (C Programs)

### Prerequisites
- A standard C compiler (`gcc` or `clang`) with POSIX threads (`-pthread`) support.

### Compilation Commands

1. **Task 1 (Scheduler & Threading)**:
   ```bash
   gcc -Wall -Wextra task1/scheduler.c -o task1/scheduler -pthread
   ./task1/scheduler
   ```

2. **Task 2 (Memory Management Simulator)**:
   ```bash
   gcc -Wall -Wextra task2/memory_sim.c -o task2/memory_sim
   ./task2/memory_sim
   ```

3. **Task 3 (Secure File System)**:
   ```bash
   gcc -Wall -Wextra task3/secure_fs.c -o task3/secure_fs
   ./task3/secure_fs
   ```

4. **Task 4 (Socket IPC Server & Client)**:
   - Start Server (Terminal 1):
     ```bash
     gcc -Wall -Wextra task4/server.c -o task4/server -pthread
     ./task4/server
     ```
   - Run Client (Terminal 2):
     ```bash
     gcc -Wall -Wextra task4/client.c -o task4/client
     ./task4/client
     ```

---

## Note on Python Files
> **Note**: All initial Python reference implementation files (`.py`) have been excluded from observation in the `main` branch and transferred to the `dummypython` branch for initial workflow reference. The `main` branch contains strictly the final C language deliverables.
