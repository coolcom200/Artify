from api.image_manager.image_manager_interface import ImageManagerInterface
from api.image_manager.image_manager_local import ImageManagerLocal


def get_image_manager(app) -> ImageManagerInterface:
    return ImageManagerLocal(app.config["FILE_SAVE_LOCATION"], app.config["FOLDER_DEPTH"])
