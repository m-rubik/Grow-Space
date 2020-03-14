import os


def generate_unique_filename(name, filetype):
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
