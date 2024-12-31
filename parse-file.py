import os
import json
import base64

def folder_to_string(folder_path):
    """
    Serialize a folder and its contents (including images or binary files) into a string.
    """
    def serialize_folder(path):
        structure = {}
        for item in os.listdir(path):
            full_path = os.path.join(path, item)
            if os.path.isdir(full_path):
                structure[item] = serialize_folder(full_path)
            else:
                with open(full_path, 'rb') as file:  # Read in binary mode
                    file_content = file.read()
                    encoded_content = base64.b64encode(file_content).decode('utf-8')
                    structure[item] = {"type": "file", "content": encoded_content}
        return {"type": "folder", "content": structure}

    folder_structure = serialize_folder(folder_path)
    return json.dumps(folder_structure)

def string_to_folder(serialized_string, output_path):
    """
    Recreate a folder and its contents (including images or binary files) from a serialized string.
    """
    folder_structure = json.loads(serialized_string)

    def recreate_folder(structure, path):
        os.makedirs(path, exist_ok=True)
        for name, item in structure["content"].items():
            full_path = os.path.join(path, name)
            if item["type"] == "folder":
                recreate_folder(item, full_path)
            elif item["type"] == "file":
                with open(full_path, 'wb') as file:  # Write in binary mode
                    decoded_content = base64.b64decode(item["content"])
                    file.write(decoded_content)

    recreate_folder(folder_structure, output_path)

def update_html(input_folder):
    with open("./index.html", "w") as f:
        f.write(folder_to_string(input_folder))
update_html("app")