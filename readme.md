# 🌍 GeoAI 📸

GeoAI is a smart and intuitive application designed to extract the location information from your uploaded photos. It's an agent based system on Langchain and google LLM- Gemini Flash 1.5.

## Table of Contents
1. [Installation 🔧](#installation)
2. [Usage 🔄](#usage)


## Installation 🔧
To get started with GeoAI, follow these steps:

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/GeoAI.git
   ```
2. Navigate to the project directory:
   ```
   cd GeoAI
   ```
3. Install the dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage 🔄
1. Run the application:
   ```
    uvicorn app:app --reload   
   ```
2. Upload a photo via /docs or http request
3. The response is in a json format with latitude, longitude and reasoning keys.
