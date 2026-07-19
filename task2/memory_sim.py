import sys

from networkx import hits
PAGE_SIZE = 4 # step 1 configuration variable[cite: 1, 2]
TOTAL_FRAMES = 3
#core helpers
def get_page_number(virtual_address):
    # simple integer division to drop the offset bytes
    """converts a raw memory address into its corresponding page number."""
    return virtual_address // PAGE_SIZE

#grid visualization formatter
def print_memory_grid(algorithm_name, current_frames, status, page_num):
    """prints a clear, human-readable grid layout of physical frames."""
    frame_display = []
    for i in range(TOTAL_FRAMES):
        if i < len(current_frames):
                    frame_display.append(f"[{current_frames[i]}]")
        else:
                    frame_display.append("[ ]")  # empty slot representation

    grid_string = " | ".join(frame_display)
    print(
                f"[{algorithm_name}] Page {page_num} -> {status.upper().ljust(5)} | Frames: {grid_string}"
     )
    
    #algorithm simulation interfaces
def run_fifo_simulation(address_stream):
    """simulates first-in-first-out page replacement logic."""
    print(f"\n--- starting fifo simulation (frames available: {TOTAL_FRAMES}) ---")
    frames = []#for tracking pages physically resident in memory
    hits=0
    faults = 0
    
    for addr in address_stream:
        page = get_page_number(addr)
        
        if page not in frames:
            faults += 1
            # checkimg if memory grid has open capacity
            if len(frames) < TOTAL_FRAMES:
                frames.append(page)
            else:
                # first in is at index 0, pop it out[cite: 1]
                frames.pop(0)
                frames.append(page)
            print_memory_grid("FIFO", frames, "fault", page)
        else:
            hits += 1
            print_memory_grid("FIFO", frames, "hit", page)
     #ratio calculations for performance metrics       
    total_ops = len(address_stream)
    hit_ratio = (hits / total_ops) * 100
    miss_ratio = (faults / total_ops) * 100

    print(f"fifo results -> hits: {hits}, faults: {faults}")
    print(
        f"performance ratios -> hit ratio: {hit_ratio:.1f}%, miss ratio: {miss_ratio:.1f}%\n"
    )
    return faults

#lru algorithm interface
def run_lru_simulation(address_stream):
    """simulates least-recently-used page replacement logic."""
    print(f"\n--- starting lru simulation (frames available: {TOTAL_FRAMES}) ---")
    frames = []
    access_history = {} # dictionary tracker to keep logical clock ticks
    hits=0
    faults = 0
    logical_time = 0 # increments on every page reference step
    
    for addr in address_stream:
        logical_time += 1
        page = get_page_number(addr)
        
        # update time rank on every hit or miss access alike
        access_history[page] = logical_time
        
        if page in frames:
            hits += 1
            print_memory_grid("LRU", frames, "hit", page)
        else:
            faults += 1
            if len(frames) < TOTAL_FRAMES:
                frames.append(page)
            else:
                # search the active grid to track down the minimum used frame slot
                oldest_page = frames[0]
                min_time = access_history[oldest_page]
                
                for f in frames:
                    if access_history[f] < min_time:
                        min_time = access_history[f]
                        oldest_page = f
                        
                # boot out the unaccessed page context link
                frames.remove(oldest_page)
                frames.append(page)
            print_memory_grid("LRU", frames, "fault", page)
      #ratio calculation integration for performance metrics      
    total_ops = len(address_stream)
    hit_ratio = (hits / total_ops) * 100
    miss_ratio = (faults / total_ops) * 100

    print(f"lru results -> hits: {hits}, faults: {faults}")
    print(
        f"performance ratios -> hit ratio: {hit_ratio:.1f}%, miss ratio: {miss_ratio:.1f}%\n"
    )
    return faults

if __name__ == "__main__":
    # quick sanity verification test loop
    addresses = [2, 3, 5, 11]
    for addr in addresses:
        print("address: " + str(addr) + " maps directly to page: " + str(get_page_number(addr)))
        
    print("\n--- running actual trace simulation ---")
    virtual_addresses = [2, 3, 5, 11, 1, 14, 7, 19]

    fifo_faults = run_fifo_simulation(virtual_addresses)
    lru_faults = run_lru_simulation(virtual_addresses)
    
    print("comparison overview ---->")
    print(f"total system page faults generated -> fifo: {fifo_faults} | lru: {lru_faults}")