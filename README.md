# ST5004CEM Operating Systems and Security Coursework

This repository contains the complete implementation for Tasks 1 through 4 of the ST5004CEM Operating Systems and Security assignment. Both **Python** and **C** implementations are provided with full functional equivalence.

---

## Project Structure

```text
ST5004CEM_OS_Assignment/
├── Makefile                 # C build script for all tasks
├── README.md                # Compilation and execution guide
├── documentation_guide.md   # Comprehensive assignment report guide
├── guidelines.md            # Coursework prompt and learning outcomes
├── users.txt                # User credentials database (auto-generated)
├── audit.log                # Security audit log (auto-generated)
├── task1/
│   ├── scheduler.py         # Task 1 Python implementation
│   └── scheduler.c          # Task 1 C implementation
├── task2/
│   ├── memory_sim.py        # Task 2 Python implementation
│   └── memory_sim.c         # Task 2 C implementation
├── task3/
│   ├── secure_fs.py         # Task 3 Python implementation
│   └── secure_fs.c          # Task 3 C implementation
└── task4/
    ├── server.py            # Task 4 Python socket server
    ├── client.py            # Task 4 Python socket client
    ├── server.c            # Task 4 C socket server
    └── client.c            # Task 4 C socket client
```

---

## Prerequisites & Compilation (C Language)

### Prerequisites
- **GCC / Clang Compiler** (supports C99/C11 and POSIX threads `-pthread`)
- **Make** (optional, for easy building)

### Compiling all C tasks using Makefile
```bash
make all
```

### Manual Compilation Commands

#### Task 1: Process Management & Threading
```bash
gcc -Wall -Wextra task1/scheduler.c -o task1/scheduler -pthread
```

#### Task 2: Memory Management Simulator
```bash
gcc -Wall -Wextra task2/memory_sim.c -o task2/memory_sim
```

#### Task 3: Secure File System
```bash
gcc -Wall -Wextra task3/secure_fs.c -o task3/secure_fs
```

#### Task 4: Socket IPC Server & Client
**Linux / WSL:**
```bash
gcc -Wall -Wextra task4/server.c -o task4/server -pthread
gcc -Wall -Wextra task4/client.c -o task4/client
```

**Windows (MinGW):**
```bash
gcc -Wall -Wextra task4/server.c -o task4/server.exe -pthread -lws2_32
gcc -Wall -Wextra task4/client.c -o task4/client.exe -lws2_32
```

---

## Execution Instructions

### C Implementation Execution

#### Task 1: Scheduler Simulation
```bash
./task1/scheduler
```

#### Task 2: Memory Simulator
```bash
./task2/memory_sim
```

#### Task 3: Secure File System
```bash
./task3/secure_fs
```

#### Task 4: Client-Server Socket IPC
1. Start the server in terminal 1:
   ```bash
   ./task4/server
   ```
2. Execute the client in terminal 2:
   ```bash
   ./task4/client
   ```

---

## Execution Instructions (Python Version)

### Task 1
```bash
python task1/scheduler.py
```

### Task 2
```bash
python task2/memory_sim.py
```

### Task 3
```bash
python task3/secure_fs.py
```

### Task 4
1. Terminal 1 (Server): `python task4/server.py`
2. Terminal 2 (Client): `python task4/client.py`
