import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        file_abs = os.path.abspath(os.path.join(working_dir_abs, file_path))
        filename, file_extension = os.path.splitext(file_path)

        if os.path.commonpath([working_dir_abs, file_abs]) != working_dir_abs:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(file_abs):
            return f'Error: File "{file_path}" not found.'

        if file_extension != ".py":
            return f'Error: "{file_path}" is not a Python file.'

        commands = ["python3"]
        commands.append(file_path)
        commands += args
        execution = subprocess.run(
            args=commands, cwd=working_directory, capture_output=True, text=True
        )

        if execution.stderr or execution.stdout:
            return (
                f"STDOUT: {execution.stdout} STDERR: {execution.stderr} Process exited with code {execution.returncode}"
                if execution.returncode != 0
                else f"STDOUT: {execution.stdout} STDERR: {execution.stderr}"
            )

    except Exception as e:
        return f"Error: executing Python file: {e}"



schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a specified python file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "working_directory": types.Schema(
                type=types.Type.STRING,
                description="The working directory.",
            ),
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to run.",
            ),
            "args": types.Schema(
                type=types.Type.STRING,
                description="The additional arguments to run.",
            ),
        },
    ),
)
