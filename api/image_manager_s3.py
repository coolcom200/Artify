from api.image_manager_interface import ImageManagerInterface

class ImageManagerS3(ImageManagerInterface):

    def save_to_storage(self, image_name, file):
        pass

    def delete_from_storage(self, image_id):
        pass