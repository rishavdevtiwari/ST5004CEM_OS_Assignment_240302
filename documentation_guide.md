# Operating Systems and Security (ST5004CEM) - Documentation & Verification Guide

This document provides a comprehensive guide for documenting and verifying all four practical tasks in the ST5004CEM assignment repository, covering both **Python** and **C** implementations.

---

## Workspace Readiness & Verification Summary

All four tasks have been thoroughly developed, verified for 100% execution success, and provided in both Python and C language implementations with complete functional parity.

| Task | Module / Component | Python Source Files | C Source Files | Status | Execution Readiness | Required Report Word Count |
| :--- | :--- | :--- | :--- | :---: | :---: | :---: |
| **Task 1** | Process Management & Threading | `task1/scheduler.py` | `task1/scheduler.c` | ✅ Ready | Verified Clean Run | 500 – 750 words |
| **Task 2** | Memory Management Simulation | `task2/memory_sim.py` | `task2/memory_sim.c` | ✅ Ready | Verified Clean Run | 500 – 750 words |
| **Task 3** | File System & Security | `task3/secure_fs.py` | `task3/secure_fs.c` | ✅ Ready | Verified Clean Run | 500 – 750 words |
| **Task 4** | Network Programming & IPC | `task4/server.py`, `task4/client.py` | `task4/server.c`, `task4/client.c` | ✅ Ready | Verified Clean Run | 500 words |

---

## Detailed Task Guides

### Task 1: Process Management and Threading

#### 1. How to Run
- **Python**:
  ```bash
  python task1/scheduler.py
  ```
- **C**:
  ```bash
  gcc -Wall -Wextra task1/scheduler.c -o task1/scheduler -pthread
  ./task1/scheduler
  ```

#### 2. What to Expect Upon Execution
- **Round-Robin Scheduling**:
  - The application initializes 3 process control blocks (`ProcessPCB`):
    - PID 101 (`Task-A`, burst time: 0.9s)
    - PID 102 (`Task-B`, burst time: 0.3s)
    - PID 103 (`Task-C`, burst time: 1.1s)
  - Time quantum is set to `0.4s`.
  - Terminal logs indicate thread spawning, process execution slice, preemption state updates (`[PREEMPTED]`), and termination state transitions (`[FINISHED]`).
- **Deadlock Prevention Demonstration**:
  - Launches threads attempting to acquire two locks (`lock_a` and `lock_b`) in reverse orders.
  - Demonstrates strict resource ordering via pointer address comparison (`uintptr_t` in C / `id()` in Python), ensuring circular wait condition is eliminated.
  - Output displays `deadlock test finished successfully without any issues.`

#### 3. What to Include in Documentation / Report (500–750 words)
- **Design Decisions**:
  - Explain the Process Control Block (PCB) structure and state machine (`READY`, `RUNNING`, `PREEMPTED`, `TERMINATED`).
  - Discuss multi-threading using POSIX threads (`pthread_t` in C) and why mutexes (`pthread_mutex_t` / `threading.Lock()`) are required for shared console logging (`safe_print`).
- **Scheduling Logic Analysis**:
  - Describe the Round-Robin algorithm, time quantum selection trade-offs (context-switching overhead vs. responsiveness), and fairness guarantees.
- **Concurrency & Deadlock Prevention**:
  - Detail the four necessary Coffman conditions for deadlock (Mutual Exclusion, Hold and Wait, No Preemption, Circular Wait).
  - Explain how memory-based lock ordering breaks the **Circular Wait** condition to prevent deadlock.
- **Evidence & Deliverables**:
  - Include full console output log screenshots showing preemption sequences and successful deadlock test completion.

---

### Task 2: Memory Management Simulation

#### 1. How to Run
- **Python**:
  ```bash
  python task2/memory_sim.py
  ```
- **C**:
  ```bash
  gcc -Wall -Wextra task2/memory_sim.c -o task2/memory_sim
  ./task2/memory_sim
  ```

#### 2. What to Expect Upon Execution
- **Address Translation Output**:
  - Shows virtual address to page number translation (e.g., Address `11` with Page Size `4` maps to Page `2`).
- **Step-by-Step Memory Grid Logs**:
  - Visual grid output showing frame residency after each reference for **FIFO** (First-In, First-Out) and **LRU** (Least Recently Used).
  - Terminal prints page reference status (`FAULT` vs `HIT`) alongside physical frame contents (e.g., `[FIFO] Page 3 -> FAULT | Frames: [1] | [2] | [3]`).
- **Performance Ratios & Comparison**:
  - Calculates total hits, total page faults, **Hit Ratio (%)**, and **Miss/Fault Ratio (%)**.
  - Displays summary comparison (FIFO vs LRU fault metrics).

#### 3. What to Include in Documentation / Report (500–750 words)
- **Virtual Memory Architecture**:
  - Define paging, page size calculation (`page_number = virtual_address / PAGE_SIZE`), offsets, and frame allocation.
- **Algorithm Comparison & Performance Analysis**:
  - Explain the mechanics of **FIFO** (queue structure) vs. **LRU** (logical clock / access history tracking).
  - Analyze the hit/miss ratio metrics produced by the test sequence.
  - Discuss Belady's Anomaly (for FIFO) and temporal locality of reference (for LRU).
- **Evidence & Deliverables**:
  - Screenshots of step-by-step frame state logs.
  - Comparative metrics summary table.

---

### Task 3: File System Operations and Security

#### 1. How to Run
- **Python**:
  ```bash
  python task3/secure_fs.py
  ```
- **C**:
  ```bash
  gcc -Wall -Wextra task3/secure_fs.c -o task3/secure_fs
  ./task3/secure_fs
  ```

#### 2. What to Expect Upon Execution
- **User Authentication**:
  - Prompts for credentials (Username: `admin`, Password: `admin123`).
  - Validates password against SHA-256 hash stored in `users.txt`. Displays `Welcome back, admin!`.
- **File Operations & XOR Cipher Encryption**:
  - Creates files (`confidential.txt`, `public.txt`).
  - Encrypts file payload using XOR stream cipher before storage and decrypts upon read.
- **POSIX Permission & Access Control Evaluation**:
  - Tests reading with `admin` context (succeeds).
  - Swaps context to `guest_user` and tests access on `confidential.txt` (`Access Denied: You do not have read permissions`) vs `public.txt` (succeeds based on `rw:r:r` other-permissions).
- **Audit Logging**:
  - Automatically appends timestamped entries for `LOGIN`, `CREATE`, `WRITE`, `READ`, and `DELETE` operations into `audit.log`.

#### 3. What to Include in Documentation / Report (500–750 words)
- **Security Architecture & Design**:
  - Explain the authentication workflow (SHA-256 password hashing to prevent plaintext exposure).
  - Describe POSIX permission tri-string format (`owner:group:others`) and access matrix checking (`check_permission`).
  - Detail data confidentiality via stream cipher XOR encryption at rest.
- **Audit Trail & Accountability**:
  - Discuss the role of audit logs (`audit.log`) in security monitoring, non-repudiation, and breach investigation.
- **Security Analysis & Vulnerability Discussion**:
  - Critically evaluate limitations: symmetric key management risks, XOR cipher key repetition risks, in-memory plaintexts, lack of salt in SHA-256 password storage.
  - Propose mitigations (PBKDF2/bcrypt, AES-GCM encryption, salted hashing).
- **Evidence & Deliverables**:
  - User guide for terminal authentication and file operations.
  - Sample screenshot of terminal run and contents of generated `audit.log`.

---

### Task 4: Network Programming and Inter-Process Communication (IPC)

#### 1. How to Run
- **Python**:
  - Terminal 1 (Server): `python task4/server.py`
  - Terminal 2 (Client): `python task4/client.py`
- **C**:
  - Terminal 1 (Server): `./task4/server`
  - Terminal 2 (Client): `./task4/client`

#### 2. What to Expect Upon Execution
- **Server Console Output**:
  - Displays `[SERVER] -> listening actively on tcp://127.0.0.1:9090`.
  - Logs client connection addresses and incoming raw JSON payloads.
  - Logs verified command processing (`PING`, `UPPERCASE`).
- **Client Console Output**:
  - Transmits JSON payload with valid auth token (`super_secret_ipc_token`).
  - Decodes responses from server (`PONG`, uppercase data string).
  - Performs security boundary test with an invalid token (`wrong_hacker_token`).
  - Receives and displays security rejection: `{"status": "error", "message": "invalid security handshake token"}`.

#### 3. What to Include in Documentation / Report (~500 words)
- **Network Protocol Specification**:
  - Document the Application-Layer IPC protocol structure formatted in JSON:
    - Envelope fields: `token` (authentication passkey), `command` (action verb), `data` (payload string).
- **Concurrency & Socket Architecture**:
  - Detail TCP socket connection lifecycle (`bind`, `listen`, `accept`, `recv`, `send`, `close`).
  - Explain multi-threaded server architecture handling concurrent clients without blocking the main socket listener.
- **Security & Error Handling Analysis**:
  - Explain authentication token validation, JSON schema validation, and socket resource cleanup (`finally` blocks / teardowns).
- **Evidence & Deliverables**:
  - Protocol specification diagram or JSON schema listing.
  - Screenshots of side-by-side terminal windows (Server and Client execution).

---

## Submission Checklist & Formatting Guidelines

- **Report Word Count**: Total ~2,000 words (approx. 500–750 words per task section).
- **Format**: PDF document for report submission, named according to guidelines (`NAME_studentID.pdf`).
- **Archive**: Source code files (`task1/`, `task2/`, `task3/`, `task4/`, `users.txt`, `Makefile`, `README.md`) packaged into a single ZIP archive.
- **References**: Include IEEE / Harvard citations for operating system concepts (e.g., Silberschatz OS concepts, POSIX permissions, Round-Robin scheduling, paging algorithms).
