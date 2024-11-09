import streamlit as st
import pandas as pd
from PIL import Image
from io import BytesIO
import base64
import json
import os
from langchain_core.messages import HumanMessage, SystemMessage
from src.agent import Agent
from dotenv import load_dotenv


load_dotenv()


class GeolocationImageAnalyzer:
    def __init__(self):
        self.config = self._load_config()

    def _load_config(self):
        with open("src/config.json", "r") as f:
            return json.load(f)

    def resize_image(self, img, max_size=1024):
        scale = max_size / max(img.size) if max(img.size) > max_size else 1
        resized = img.resize(
            [int(d * scale) for d in img.size], Image.Resampling.LANCZOS
        ).convert("RGB")
        return resized

    def process_image(self, image):
        image = self.resize_image(image)
        byte_io = BytesIO()
        image.save(byte_io, format="JPEG")
        image_data = base64.b64encode(byte_io.getvalue()).decode("utf-8")

        system = SystemMessage(self.config["system_message"])
        message = HumanMessage(
            content=[
                {"type": "text", "text": ""},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{image_data}"},
                },
            ],
        )
        agent = Agent(image=image)
        graph = agent.create_graph()
        res = graph.invoke(
            {"messages": [system, message], "recursion_limit": 5}, stream_mode="values"
        )
        return json.loads(res["messages"][-1].content)


analyzer = GeolocationImageAnalyzer()


API_URL = os.getenv("API_URL")

st.title("🗺️ GeoTagr 📍")

st.markdown("""Upload a photo, and the app will pinpoint it on the map.""")

col1, col2 = st.columns([4, 1])

with col1:
    uploaded_file = st.file_uploader("Upload a Photo", type=["jpg", "jpeg", "png"])

with col2:
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Photo", width=100)

if uploaded_file is not None:
    response = analyzer.process_image(image)

    if response:
        latitude = float(response.get("latitude"))
        longitude = float(response.get("longitude"))

        if latitude is not None and longitude is not None:
            map_data = pd.DataFrame({"lat": [latitude], "lon": [longitude]})
            st.header("Location: ")
            st.write("Latitude: ", latitude)
            st.write("Longitude: ", longitude)
            st.markdown("**Reasoning:** " + response.get("reasoning"))
            st.map(map_data, zoom=5)
        else:
            st.error("Could not retrieve coordinates from the image.")
    else:
        st.error(f"Error processing image: {response.status_code} - {response.text}")
