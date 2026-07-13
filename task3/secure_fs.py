# baseline file system map layout
mock_dir = {}

def create(filename):
    # simple directory storage map update
    mock_dir[filename] = ""
    print("file initialized")

create("test.txt")