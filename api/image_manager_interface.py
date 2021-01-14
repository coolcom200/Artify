from abc import ABC, abstractmethod
from uuid import uuid4 as generate_uuid
from werkzeug.datastructures import FileStorage

class ImageManagerInterface(ABC):

    def is_allowed_file_type(self, file: FileStorage):
       pass 

    def save_image(self, file: FileStorage) -> str:
        safe_filename = str(generate_uuid())
        self.save_to_storage(safe_filename, file)
        return safe_filename

    @abstractmethod
    def save_to_storage(self, image_name, file: FileStorage) -> str:
        pass

    @abstractmethod
    def delete_from_storage(self, image_name):
        pass

    @abstractmethod
    def get_image(self, image_name) -> str:
        pass

    