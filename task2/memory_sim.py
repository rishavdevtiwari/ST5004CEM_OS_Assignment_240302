PAGE_SIZE = 4 # step 1 configuration variable[cite: 1, 2]
TOTAL_FRAMES = 3

def get_page_number(virtual_address):
    # simple integer division to drop the offset bytes
    return virtual_address // PAGE_SIZE

#grid visualization formatter
def print_memory_grid(algorithm_name, current_frames, status, page_num):
    """prints a clear, human-readable grid layout of physical frames."""
    display = []
    for i in range(TOTAL_FRAMES):
        if i < len(current_frames):
            display.append("[" + str(current_frames[i]) + "]")
        else:
            display.append("[ ]") # empty slot representation
    print("[" + algorithm_name + "] Page " + str(page_num) + " -> " + status.upper().ljust(5) + " | Frames: " + " | ".join(display))

def run_fifo_simulation(address_stream):
    print("--- starting fifo simulation ---")
    frames = []
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
            print_memory_grid("FIFO", frames, "hit", page)
            
    print("total fifo faults recorded: " + str(faults))

if __name__ == "__main__":
    # quick sanity verification test loop
    addresses = [2, 3, 5, 11]
    for addr in addresses:
        print("address: " + str(addr) + " maps directly to page: " + str(get_page_number(addr)))
        
    print("\n--- running actual trace simulation ---")
    virtual_addresses = [2, 3, 5, 11, 1, 14, 7, 19]
    run_fifo_simulation(virtual_addresses)