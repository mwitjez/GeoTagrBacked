from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
from io import BytesIO
import base64
import json
from langchain_core.messages import HumanMessage, SystemMessage
from src.agent import Agent

app = FastAPI()

# Allow CORS if needed
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GeolocationImageAnalyzer:
    def __init__(self, config):
        self.config = config

    def resize_image(self, img, max_size=1024):
        scale = max_size / max(img.size) if max(img.size) > max_size else 1
        resized = img.resize([int(d * scale) for d in img.size], Image.Resampling.LANCZOS).convert('RGB')
        return resized

    def process_image(self, image):
        image = self.resize_image(image)
        byte_io = BytesIO()
        image.save(byte_io, format='JPEG')
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
            {"messages": [system, message], "recursion_limit": 5}, 
            stream_mode="values"
        )
        return json.loads(res["messages"][-1].content)

analyzer = GeolocationImageAnalyzer(config={"system_message": "Your system message here"})

@app.post("/process-image")
async def process_image(file: UploadFile = File(...)):
    image = Image.open(BytesIO(await file.read()))
    result = analyzer.process_image(image)
    return JSONResponse(content=result)
