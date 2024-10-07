from pydantic import BaseModel, Field


class Location(BaseModel):
    """Location of an photo with reasoning."""
    address: str = Field(description="The address of the location (Street, City, Country)")
    latitude: str = Field(description="The latitude of the location")
    longitude: str = Field(description="The longitude of the location")
    reasoning: str = Field(description="Reasoning about the location of the photo")