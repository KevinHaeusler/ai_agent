import os
from google.genai import types
from config import MAX_CHARS


def get_file_content(working_directory, file_path):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        file_abs = os.path.abspath(os.path.join(working_dir_abs, file_path))

        if os.path.commonpath([working_dir_abs, file_abs]) != working_dir_abs:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(file_abs):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(file_abs, "r", encoding="utf-8", errors="replace") as f:
            data = f.read(MAX_CHARS + 1)

        truncated = len(data) > MAX_CHARS
        content = data[:MAX_CHARS]

        if truncated:
            return (
                content
                + f'\n[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            )
        return content

    except Exception as e:
        return f"Error: {e}"


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Lists the content of the specified file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "working_directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to read files from, relative to the working directory.",
            ),
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to read.",
            ),
        },
    ),
)
