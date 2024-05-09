
import os

def read_file(file_name):
    root_dir = os.path.dirname(os.path.abspath(__file__))  # Get the absolute path to the directory of this file
    data_path = os.path.join(root_dir, '..', 'data', file_name)
    
    with open(data_path, 'r') as file:
        content = file.read()
    
    return content
