from api.image_manager_interface import ImageManagerInterface
from werkzeug.datastructures import FileStorage
import os

class ImageManagerLocal(ImageManagerInterface):
    LOCATION="./files/"
    FOLDER_DEPTH = 8

    def generate_file_save_dir(self, filename) -> str:
        return os.path.join(self.LOCATION, *list(filename[:self.FOLDER_DEPTH]))

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
        # TODO: Remove relative path reference
        return "../"+os.path.join(self.generate_file_save_dir(image_name), image_name)

