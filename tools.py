from langchain_core.tools import tool
from langchain_community.tools import WikipediaQueryRun


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

    @tool
    def duck_duck_go_search(query: str) -> str:
        """
        Searches DuckDuckGo for the given query.

        Args:
            query (str): The query to search for.

        Returns:
            str: The results of the search.
        """
        return "DuckDuckGo: " + query

    @tool
    def reverse_image_search() -> str:
        """Finds similar images to the given image.

        Returns:
            dict: The results of the search.
        """
        return {}

    @tool
    def wikimapia_search(query: str) -> str:
        """
        Searches Wikimapia for the given query.

        Args:
            query (str): The query to search for.

        Returns:
            str: The results of the search.
        """
        return "Wikimapia: " + query

    @tool
    def exif_metadata_extraction() -> str:
        """
        Returns the EXIF metadata of the image.

        Returns:
            dict: The EXIF metadata.
        """
        return {}