from dataclasses import dataclass

@dataclass
class FileWithPath:
    data: dict

    def __init__(self, file_name, file_path):
        self.data = {"file_name": file_name, "file_path": file_path}

    def to_dict(self):
        return self.data 
