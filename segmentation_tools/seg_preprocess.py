from io_tools.file_management import add_0000_in_suffix, add_whole_in_suffix, copy_folder, delete_folder
import os

def preprocess_images(input_folder, output_folder):
    if len(os.listdir(output_folder)) != 0:
        delete_folder(output_folder)
    copy_folder(input_folder, output_folder)
    add_whole_in_suffix(output_folder)
    add_0000_in_suffix(output_folder)