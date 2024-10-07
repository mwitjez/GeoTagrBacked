import base64
import json
from PIL import Image

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
    image_path = "test/test_images/test6.jpg"
    image = Image.open(image_path)
    image_bytes = open(image_path, "rb").read()
    image_data = base64.b64encode(image_bytes).decode("utf-8")
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
    print_stream(graph.stream({"messages": [system, message], "recursion_limit": 5}, stream_mode="values"))
