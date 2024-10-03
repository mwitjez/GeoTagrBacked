from openai import OpenAI
import base64
import requests

def send_request_to_model():
    client = OpenAI(base_url="http://localhost:1234/v1", api_key="not-needed")
    path = input("Enter a local filepath to an image: ")
    base64_image = ""
    try:
        image = open(path.replace("'", ""), "rb").read()
        base64_image = base64.b64encode(image).decode("utf-8")
    except:
        print("Couldn't read the image. Make sure the path is correct and the file exists.")
        exit()

    completion = client.chat.completions.create(
    model="local-model",
    messages=[
        {
        "role": "system",
        "content": "This is a chat between a user and an assistant. The assistant is helping the user to describe an image.",
        },
        {
        "role": "user",
        "content": [
            {"type": "text", "text": "What’s in this image?"},
            {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}"
            },
            },
        ],
        }
    ],
    max_tokens=1000,
    stream=False
    )

    for chunk in completion:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)
