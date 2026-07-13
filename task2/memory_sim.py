PAGE_SIZE = 4 # step 1 configuration variable

def get_page_number(virtual_address):
    # simple integer division to drop the offset bytes
    return virtual_address // PAGE_SIZE

# quick sanity verification test loop
addresses = [2, 3, 5, 11]
for addr in addresses:
    print("address: " + str(addr) + " maps directly to page: " + str(get_page_number(addr)))