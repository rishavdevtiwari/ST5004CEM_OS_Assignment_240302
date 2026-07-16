#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define PAGE_SIZE 4    // step 1 configuration variable
#define TOTAL_FRAMES 3

// core helpers
// converts a raw memory address into its corresponding page number.
int get_page_number(int virtual_address) {
    // simple integer division to drop the offset bytes
    return virtual_address / PAGE_SIZE;
}

// grid visualization formatter
// prints a clear, human-readable grid layout of physical frames.
void print_memory_grid(const char *algorithm_name, int *frames, int frame_count, const char *status, int page_num) {
    char status_upper[16];
    int j = 0;
    while (status[j] != '\0' && j < 15) {
        if (status[j] >= 'a' && status[j] <= 'z') {
            status_upper[j] = status[j] - 32;
        } else {
            status_upper[j] = status[j];
        }
        j++;
    }
    status_upper[j] = '\0';

    printf("[%s] Page %d -> %-5s | Frames: ", algorithm_name, page_num, status_upper);
    for (int i = 0; i < TOTAL_FRAMES; i++) {
        if (i < frame_count) {
            printf("[%d]", frames[i]);
        } else {
            printf("[ ]"); // empty slot representation
        }
        if (i < TOTAL_FRAMES - 1) {
            printf(" | ");
        }
    }
    printf("\n");
}

// algorithm simulation interfaces
// simulates first-in-first-out page replacement logic.
int run_fifo_simulation(int *address_stream, int stream_len) {
    printf("\n--- starting fifo simulation (frames available: %d) ---\n", TOTAL_FRAMES);
    int frames[TOTAL_FRAMES]; // for tracking pages physically resident in memory
    int frame_count = 0;
    int hits = 0;
    int faults = 0;

    for (int idx = 0; idx < stream_len; idx++) {
        int addr = address_stream[idx];
        int page = get_page_number(addr);

        int found = 0;
        for (int f = 0; f < frame_count; f++) {
            if (frames[f] == page) {
                found = 1;
                break;
            }
        }

        if (!found) {
            faults++;
            // checkimg if memory grid has open capacity
            if (frame_count < TOTAL_FRAMES) {
                frames[frame_count++] = page;
            } else {
                // first in is at index 0, pop it out
                for (int f = 0; f < TOTAL_FRAMES - 1; f++) {
                    frames[f] = frames[f + 1];
                }
                frames[TOTAL_FRAMES - 1] = page;
            }
            print_memory_grid("FIFO", frames, frame_count, "fault", page);
        } else {
            hits++;
            print_memory_grid("FIFO", frames, frame_count, "hit", page);
        }
    }

    // ratio calculations for performance metrics
    double hit_ratio = ((double)hits / stream_len) * 100.0;
    double miss_ratio = ((double)faults / stream_len) * 100.0;

    printf("fifo results -> hits: %d, faults: %d\n", hits, faults);
    printf("performance ratios -> hit ratio: %.1f%%, miss ratio: %.1f%%\n\n", hit_ratio, miss_ratio);
    return faults;
}

// lru algorithm interface
// simulates least-recently-used page replacement logic.
int run_lru_simulation(int *address_stream, int stream_len) {
    printf("\n--- starting lru simulation (frames available: %d) ---\n", TOTAL_FRAMES);
    int frames[TOTAL_FRAMES];
    int access_history[1000] = {0}; // array tracker to keep logical clock ticks
    int frame_count = 0;
    int hits = 0;
    int faults = 0;
    int logical_time = 0; // increments on every page reference step

    for (int idx = 0; idx < stream_len; idx++) {
        logical_time++;
        int addr = address_stream[idx];
        int page = get_page_number(addr);

        // update time rank on every hit or miss access alike
        access_history[page] = logical_time;

        int found = 0;
        for (int f = 0; f < frame_count; f++) {
            if (frames[f] == page) {
                found = 1;
                break;
            }
        }

        if (found) {
            hits++;
            print_memory_grid("LRU", frames, frame_count, "hit", page);
        } else {
            faults++;
            if (frame_count < TOTAL_FRAMES) {
                frames[frame_count++] = page;
            } else {
                // search the active grid to track down the minimum used frame slot
                int oldest_page = frames[0];
                int min_time = access_history[oldest_page];
                int oldest_idx = 0;

                for (int f = 0; f < frame_count; f++) {
                    if (access_history[frames[f]] < min_time) {
                        min_time = access_history[frames[f]];
                        oldest_page = frames[f];
                        oldest_idx = f;
                    }
                }

                // boot out the unaccessed page context link
                for (int f = oldest_idx; f < frame_count - 1; f++) {
                    frames[f] = frames[f + 1];
                }
                frames[frame_count - 1] = page;
            }
            print_memory_grid("LRU", frames, frame_count, "fault", page);
        }
    }

    // ratio calculation integration for performance metrics
    double hit_ratio = ((double)hits / stream_len) * 100.0;
    double miss_ratio = ((double)faults / stream_len) * 100.0;

    printf("lru results -> hits: %d, faults: %d\n", hits, faults);
    printf("performance ratios -> hit ratio: %.1f%%, miss ratio: %.1f%%\n\n", hit_ratio, miss_ratio);
    return faults;
}

int main(void) {
    // quick sanity verification test loop
    int addresses[] = {2, 3, 5, 11};
    int num_addresses = sizeof(addresses) / sizeof(addresses[0]);
    for (int i = 0; i < num_addresses; i++) {
        printf("address: %d maps directly to page: %d\n", addresses[i], get_page_number(addresses[i]));
    }

    printf("\n--- running actual trace simulation ---\n");
    int virtual_addresses[] = {2, 3, 5, 11, 1, 14, 7, 19};
    int stream_len = sizeof(virtual_addresses) / sizeof(virtual_addresses[0]);

    int fifo_faults = run_fifo_simulation(virtual_addresses, stream_len);
    int lru_faults = run_lru_simulation(virtual_addresses, stream_len);

    printf("comparison overview ---->\n");
    printf("total system page faults generated -> fifo: %d | lru: %d\n", fifo_faults, lru_faults);
    return 0;
}
