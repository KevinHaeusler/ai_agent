import os

def get_files_info(working_directory, directory="."):
    working_dir_abs =  os.path.abspath(working_directory) 
    target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
    valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
    if not valid_target_dir:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(target_dir):
        return f'Error: "{directory}" is not a directory'
    files = os.listdir(target_dir)
    file_info_lines = []
    try:
        for file in files:
            filepath = os.path.join(target_dir, file)
            file_info_lines.append(f"- {file}: file_size={os.path.getsize(filepath)} bytes, is_dir={os.path.isdir(filepath)}")
        return "\n".join(file_info_lines)
  
    except Exception as e:
        return  f"Error: {e}"