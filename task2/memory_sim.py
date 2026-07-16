PAGE_SIZE = 4 # step 1 configuration variable[cite: 1, 2]
TOTAL_FRAMES = 3

def get_page_number(virtual_address):
    # simple integer division to drop the offset bytes
    return virtual_address // PAGE_SIZE

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
            print("PAGE FAULT! current memory: " + str(frames))
        else:
            print("PAGE HIT! current memory: " + str(frames))
            
    print("total fifo faults recorded: " + str(faults))

if __name__ == "__main__":
    # quick sanity verification test loop
    addresses = [2, 3, 5, 11]
    for addr in addresses:
        print("address: " + str(addr) + " maps directly to page: " + str(get_page_number(addr)))
        
    print("\n--- running actual trace simulation ---")
    virtual_addresses = [2, 3, 5, 11, 1, 14, 7, 19]
    run_fifo_simulation(virtual_addresses)