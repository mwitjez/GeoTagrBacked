from langchain_core.tools import tool

class ImagePathContext:
    def __init__(self, path):
        self.path = path

    def __enter__(self):
        global image_path
        image_path = self.path
        return image_path

    def __exit__(self, exc_type, exc_val, exc_tb):
        global image_path
        image_path = None


class ToolsContainer:
    image = None

    @tool
    def country_prediction() -> str:
        """
        Predicts a country based on the given query.

        Returns:
            str: The predicted country
        """
        if ToolsContainer.image is None:
            raise ValueError("Image not set.")
        return "France"

