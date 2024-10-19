import http.client
import json
import urllib.parse
from collections import Counter

from langchain_community.tools import DuckDuckGoSearchRun, WikipediaQueryRun
from langchain_community.utilities import (
    DuckDuckGoSearchAPIWrapper,
    WikipediaAPIWrapper,
)
from langchain_core.tools import tool
from PIL import Image
from ratelimit import limits, sleep_and_retry


class ToolsContainer:
    def __init__(self, image: Image = None):
        self.image = image
        self.tool_usage_counter = Counter()
        self.tool_usage_restrictions = {
            "country_prediction": 1,
            "search_for_place": 2,
            "wikipedia_search": 2,
            "duckduckgo_search": 2,
            "geocode": 1,
        }

    def get_tools(self):
        base = [self.wikipedia_search, self.duckduckgo_search, self.geocode]
        tools_with_call_restrictions = [
            tool(func)
            for func in base
            if self.tool_usage_counter[func.__name__]
            < self.tool_usage_restrictions[func.__name__]
        ]
        return tools_with_call_restrictions

    @sleep_and_retry
    @limits(calls=1, period=1)
    def geocode(self, query: str):
        """
        Geocodes the given query. Returns the latitude and longitude of the query.

        Args:
        query (str): Specific search string for the geocoding. Can searches for places by name or address. The query should include COUNTRY and CITY. Address is optional but recommend. E.g. "CITY, COUNTRY", " ADDRESS, CITY"

        Returns:
            dict: The latitude and longitude of the query
        """
        conn = http.client.HTTPSConnection("nominatim.openstreetmap.org")
        params = urllib.parse.urlencode(
            {"q": query, "format": "json", "addressdetails": 1, "limit": 1}
        )

        headers = {"User-Agent": "geoai app"}

        conn.request("GET", f"/search?{params}", headers=headers)
        response = conn.getresponse()
        if response.status == 200:
            data = response.read().decode("utf-8")
            data = json.loads(data)
            if len(data) == 0:
                result = {"message": "No results found. Maybe try a different query?"}
                return result
            result = {"latitude": data[0]["lat"], "longitude": data[0]["lon"]}
            self.tool_usage_counter["search_for_place"] += 1
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
        self.tool_usage_counter["wikipedia_search"] += 1
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
        wrapper = DuckDuckGoSearchAPIWrapper(max_results=2)
        search = DuckDuckGoSearchRun(api_wrapper=wrapper)
        result = search.invoke(query)
        self.tool_usage_counter["duckduckgo_search"] += 1
        return result
