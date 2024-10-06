from PIL import Image
from PIL.ExifTags import GPSTAGS, TAGS


class ExifDataExtractor:
    def __init__(self, image: Image):
        self.image = image

    def _get_exif_data(self):
        """Extract EXIF data from an image."""
        exif_data = {}

        info = self.image._getexif()
        if info is None:
            return exif_data

        for tag, value in info.items():
            decoded_tag = TAGS.get(tag, tag)
            exif_data[decoded_tag] = value

        return exif_data

    def _get_gps_info(self, exif_data):
        """Extract GPS info from the EXIF data."""
        gps_info = exif_data.get("GPSInfo")
        if not gps_info:
            return None
        gps_data = {}
        for tag, value in gps_info.items():
            decoded_tag = GPSTAGS.get(tag, tag)
            gps_data[decoded_tag] = value

        return gps_data

    def _convert_to_degrees(self, value):
        """Helper function to convert GPS coordinates stored as EXIF format into degrees."""
        d, m, s = value
        return d + (m / 60.0) + (s / 3600.0)

    def _extract_lat_lon(self, gps_data):
        """Extract latitude and longitude from GPS data."""
        lat = gps_data.get("GPSLatitude")
        lat_ref = gps_data.get("GPSLatitudeRef")
        lon = gps_data.get("GPSLongitude")
        lon_ref = gps_data.get("GPSLongitudeRef")

        if not lat or not lon or not lat_ref or not lon_ref:
            return None

        latitude = self._convert_to_degrees(lat)
        if lat_ref != "N":
            latitude = -latitude

        longitude = self._convert_to_degrees(lon)
        if lon_ref != "E":
            longitude = -longitude

        return latitude, longitude

    def get_image_location(self):
        """Extract the latitude and longitude from an image's EXIF metadata."""
        exif_data = self._get_exif_data()
        gps_data = self._get_gps_info(exif_data)

        if gps_data:
            return self._extract_lat_lon(gps_data)
        else:
            return None
