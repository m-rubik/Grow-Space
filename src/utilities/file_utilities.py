"""
Contains all utilities relevant to file operations.
"""


import os


def generate_unique_filename(name, filetype):
    """
    Generates a unique filename by appending a number, if required, to the name that is passed in.
    @param name: Name for which to create unique filename
    @param filetype: Extension to add to the end of the unique filename
    """
    
    extension = "."+filetype
    file_name = "logs/"+name+extension
    if os.path.exists(file_name):
        expand = 1
        while True:
            expand += 1
            new_file_name = file_name.split(".")[0] + "_" + str(expand) + extension
            if not os.path.exists(new_file_name):
                return new_file_name
    return file_name
