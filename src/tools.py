import os

import requests
from ratelimit import limits, sleep_and_retry
from langchain_community.tools import DuckDuckGoSearchRun, WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_core.tools import tool
from PIL import Image
import http.client
import urllib.parse
import json


class ToolsContainer:

    def __init__(self, image: Image = None):
        self.image = image
        self.predicted_country = None

    def get_tools(self):
        return [tool(self.search_for_place), tool(self.wikipedia_search)]

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

    @sleep_and_retry
    @limits(calls=1, period=1)
    def search_for_place(self, query: str):
        """
        Searches open street maps for given query
        Args:

        query (str): query to search for, can be a place name

        Returns:
            dict: The result containing places with addresses
        """
        conn = http.client.HTTPSConnection("nominatim.openstreetmap.org")
        params = urllib.parse.urlencode({
            'q': query,
            'format': 'json',
            'addressdetails': 1,
            'limit': 1
        })

        headers = {
            'User-Agent': "geoai app"
        }

        conn.request("GET", f"/search?{params}", headers=headers)
        response = conn.getresponse()
        if response.status == 200:
            data = response.read().decode('utf-8')
            data = json.loads(data)
            result = data[0].get("address")
        else:
            result = {"error": response.status_code}
        return result

    @sleep_and_retry
    @limits(calls=1000, period=60)
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

    @sleep_and_retry
    @limits(calls=500, period=2400)
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

    @sleep_and_retry
    @limits(calls=10, period=60)
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
