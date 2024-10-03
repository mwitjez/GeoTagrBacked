import base64
import json

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage

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

    config = json.loads(open("config.json").read())
    image = open("test2.jpg", "rb").read()
    image_data = base64.b64encode(image).decode("utf-8")
    message = HumanMessage(
        content=[
            {"type": "text", "text": config["prompt"]},
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{image_data}"},
            },
        ],
    )
    agent = Agent(image=image)
    graph = agent.create_graph()
    print_stream(graph.stream({"messages": [message]}, stream_mode="values"))
