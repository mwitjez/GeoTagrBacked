import base64
import json
from PIL import Image
from io import BytesIO

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage

from agent import Agent


def print_stream(stream):
    for s in stream:
        message = s["messages"][-1]
        if isinstance(message, tuple):
            print(message)
        else:
            message.pretty_print()


if __name__ == "__main__":
    load_dotenv()

    config = json.loads(open("src/config.json").read())
    ##Ograniczy kontekst wejściowy- zmieni rozmiar zdjecia!!!
    image_path = "test/data/im2gps/97344248_30a4521091_32_77325609@N00.jpg"
    image = Image.open(image_path)
    image = image.resize((1024, 1024)).convert('RGB')
    byte_io = BytesIO()
    image.save(byte_io, format='JPEG')
    image_data = base64.b64encode(byte_io.getvalue()).decode("utf-8")
    system = SystemMessage(config["system_message"])
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
    print_stream(graph.stream({"messages": [system, message], "recursion_limit": 1}, stream_mode="values"))
