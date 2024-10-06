from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.tools.base import StructuredTool
from langchain_core.tools import InjectedToolArg, tool
from typing_extensions import Annotated
from PIL import Image
from exif_data_extractor import ExifDataExtractor
from langchain_community.tools import DuckDuckGoSearchRun
import requests
import os


class ToolsContainer:

    def __init__(self, image: Image = None):
        self.image = image
        self.predicted_country = None

    def get_tools(self):
        return [tool(self.geocode), tool(self.wikipedia_search), tool(self.duckduckgo_search)]

    def country_prediction(self) -> str:
        """
        Predicts a country based on the given query.

        Returns:
            str: The predicted country
            image: Image passed to country prediction model
        """
        print(self.image)
        self.predicted_country = "Poland"
        return "Poland"

    def geocode(self, query: str):
        """
        Geocodes the given query. Returns the latitude and longitude of the query.

        Args:
        query (str): Specific search string for the geocoding, MUST include COUNTRY and CITY. Address is optional but recommend. E.g. "CITY, COUNTRY", "CITY, COUNTRY, ADDRESS"

        Returns:
            dict: The latitude and longitude of the query
        """
        access_token = os.getenv("MAPBOX_API_KEY")
        url = "https://api.mapbox.com/search/geocode/v6/forward"
        params = {
            "q": query,
            "access_token": access_token
        }

        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            coordinates = data["features"][0]["geometry"]["coordinates"]
            result = {"latitude": coordinates[1], "longitude": coordinates[0]}
        else:
            result = {"error": response.status_code}
        return result

    def wikipedia_search(self, query: str) -> str:
        """
        Searches Wikipedia for the given query.

        Args:
            query (str): The query to search for.

        Returns:
            str: The results of the search.
        """
        wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
        result = wikipedia.run(query)
        return result

    def duckduckgo_search(self, query: str) -> str:
        """
        Searches the web for the given query. Best matches could be acquired with description of a buildings, landmarks or landscape.

        Args:
            query (str): The query to search for.

        Returns:
            str: The results of the search.
        """
        search = DuckDuckGoSearchRun()
        result = search.invoke(query)
        return result


    # def exif_metadata_extraction(self) -> str:
    #     """
    #     Returns the location from the EXIF metadata of the image.

    #     Returns:
    #         dict: location or message if no location is found
    #     """
    #     extractor = ExifDataExtractor(image=self.image)
    #     location = extractor.get_image_location()
    #     if location:
    #         return {"Latitude": location[0], "Longitude": location[1]}
    #     else:
    #         return {"error": "No location found"}
