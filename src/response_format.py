from pydantic import BaseModel, Field


class Location(BaseModel):
    """Location of an photo with reasoning."""
    latitude: str = Field(description="The latitude of the location")
    longitude: str = Field(description="The longitude of the location")
    reasoning: str = Field(description="Reasoning about the location of the photo")