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

def resize_image(img, max_size=1024):
    scale = max_size / max(img.size) if max(img.size) > max_size else 1
    resized = img.resize([int(d * scale) for d in img.size], Image.Resampling.LANCZOS).convert('RGB')
    return resized


if __name__ == "__main__":
    load_dotenv()

    config = json.loads(open("src/config.json").read())
    image_path = "test/test_images/test.jpg"
    image = Image.open(image_path)
    image = resize_image(image)
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
