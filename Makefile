# Makefile for ST5004CEM Operating Systems & Security C Implementations

CC = gcc
CFLAGS = -Wall -Wextra -O2
LDFLAGS = -pthread

ifeq ($(OS),Windows_NT)
    SOCKET_LIBS = -lws2_32
    EXE = .exe
else
    SOCKET_LIBS =
    EXE =
endif

TARGETS = task1/scheduler$(EXE) task2/memory_sim$(EXE) task3/secure_fs$(EXE) task4/server$(EXE) task4/client$(EXE)

all: $(TARGETS)

task1/scheduler$(EXE): task1/scheduler.c
	$(CC) $(CFLAGS) $< -o $@ $(LDFLAGS)

task2/memory_sim$(EXE): task2/memory_sim.c
	$(CC) $(CFLAGS) $< -o $@

task3/secure_fs$(EXE): task3/secure_fs.c
	$(CC) $(CFLAGS) $< -o $@

task4/server$(EXE): task4/server.c
	$(CC) $(CFLAGS) $< -o $@ $(LDFLAGS) $(SOCKET_LIBS)

task4/client$(EXE): task4/client.c
	$(CC) $(CFLAGS) $< -o $@ $(SOCKET_LIBS)

clean:
	rm -f task1/scheduler$(EXE) task2/memory_sim$(EXE) task3/secure_fs$(EXE) task4/server$(EXE) task4/client$(EXE) audit.log users.txt

.PHONY: all clean
