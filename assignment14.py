import sys
import gc

class Node:
    def __init__(self, name):
        self.name = name
        self.link = None

    def __del__(self):
        print(f"{self.name} is being destroyed")


# Disable automatic garbage collection
gc.disable()

# Create objects
A = Node("A")
B = Node("B")

# Create cyclic reference
A.link = B
B.link = A

# Check reference counts
print("Reference count of A:", sys.getrefcount(A))
print("Reference count of B:", sys.getrefcount(B))

# Store object IDs
A_id = id(A)
B_id = id(B)

# Delete variable references
del A
del B

print("\nAfter deleting A and B variables:")

# Check if objects still exist
for obj in gc.get_objects():
    if id(obj) == A_id or id(obj) == B_id:
        print("Found unreachable object still in memory:", obj.name)

# Force garbage collection
print("\nRunning Garbage Collector...")
collected = gc.collect()

print("Unreachable objects collected:", collected)
