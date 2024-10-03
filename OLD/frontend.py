import time
import streamlit as st

from io import StringIO

class StreamlitView():
    def __init__(self) -> None:
        self._init_header_view()
        self._init_file_view()

    def _init_header_view(self):
        st.title("GeoAI")
        st.text("Upload a photo and get its location")

    def _init_file_view(self):
        st.header("Upload photo")
        uploaded_file = st.file_uploader("Choose a file", type="png")
        if uploaded_file is not None:
            with st.spinner('Wait for it...'):
                time.sleep(5)
                st.success('Done!')