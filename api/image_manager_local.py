from image_manager_interface import ImageManagerInterface
from werkzeug.datastructures import FileStorage
import os

class ImageManagerLocal(ImageManagerInterface):

    def __init__(self, file_location, folder_depth):
        self.file_save_location = file_location
        self.folder_depth = folder_depth

    def generate_file_save_dir(self, filename) -> str:
        return os.path.join(self.file_save_location, *list(filename[:self.folder_depth]))

    def save_to_storage(self, image_name: str, file: FileStorage):
        dir = self.generate_file_save_dir(image_name) 
        os.makedirs(dir)
        file_path = os.path.join(dir, image_name)
        file.save(file_path)

    def delete_from_storage(self, image_name):
        dir = self.generate_file_save_dir(image_name)
        file_path = os.path.join(dir, image_name)
        if os.path.exists(file_path):
            os.remove(file_path)

    def get_image(self, image_name):
        return os.path.join(self.generate_file_save_dir(image_name), image_name)

