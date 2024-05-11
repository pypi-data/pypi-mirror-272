import ctypes
import os


module_dir = os.path.dirname(__file__)

# Load the shared library
lib = ctypes.CDLL(os.path.join(module_dir, 'a.so'))

# Define the argument and return types of the function
lib.add.argtypes = [ctypes.c_int, ctypes.c_int]
lib.add.restype = ctypes.c_int

def add(a, b):
    print("Current Working Directory:", os.getcwd())
    # Call the C++ function
    return lib.add(a, b)

# if __name__ == '__main__':
#     # Test the function
print(add(3, 5))  # Output should be 8

