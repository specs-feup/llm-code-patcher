import subprocess
import os
import logging

logger = logging.getLogger(__name__)

def has_extension(file_path, target_extension):
    _, file_extension = os.path.splitext(file_path)
    return file_extension.lower() == target_extension.lower()

def remove_first_path_component(project_path):
    components = os.path.normpath(project_path).split(os.path.sep)
    
    # Remove the first component
    project_path = os.path.sep.join(components[1:])
    
    return project_path

def get_last_path_component(path):
    components = os.path.normpath(path).split(os.path.sep)
    
    # Get the last component
    last_component = components[-1]
    
    return last_component

def get_files_from_path(directory_path):
    return [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]

# Used to:
#   1. retrieve compiler errors
#   2. compile the patched code
def compile_with_clang(source_file_path, output_file="a.out"):
    compile_command = ["clang", source_file_path, "-ferror-limit=0", "-S"]

    # TODO assert at least version 15 (for errors on implicit function declarations)

    try:
        result = subprocess.run(compile_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            return True, None
        else:
            return False, result.stderr
    except FileNotFoundError:
        print("Clang is not installed")
        return None