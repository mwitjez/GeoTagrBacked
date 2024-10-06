import base64
import json
import os
import time
from tqdm import tqdm
import numpy as np
import haversine as hs
import csv
from PIL import Image
from typing import List, Tuple, Dict


from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from agent import Agent


def invoke_agent(image_path):
    config = json.loads(open("/Users/mateuszwitka-jezewski/Documents/Projekty/GeoAI/src/config.json").read())
    image = Image.open(f"test/data/im2gps/{image_path}")
    image_bytes = open(f"test/data/im2gps/{image_path}", "rb").read()
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

    res = graph.invoke({"messages": [system, message], "recursion_limit": 5}, stream_mode="values")
    return json.loads(res["messages"][-1].content)


def calculate_metrics(results):
    """
    Calculate evaluation metrics
    """
    distances = np.array(results)

    metrics = {
        'mean_distance_error': float(np.average(distances)),
        'median_distance_error': float(np.median(distances)),
        'std_distance_error': float(np.std(distances)),
        'accuracy_1km': float(np.mean(distances <= 1)),
        'accuracy_25km': float(np.mean(distances <= 25)),
        'accuracy_200km': float(np.mean(distances <= 200)),
        'accuracy_750km': float(np.mean(distances <= 750)),
    }
    
    return metrics

def calculate_distance_error(pred_coords: Tuple[float, float], 
                           true_coords: Tuple[float, float]) -> float:
    """
    Calculate the haversine distance between predicted and true coordinates
    """
    return hs.haversine(pred_coords, true_coords)

def generate_res_file():
    load_dotenv()
    json_file_path = 'result.json'

    if not os.path.exists(json_file_path):
        with open(json_file_path, 'w') as file:
            json.dump({}, file)

    with open(json_file_path, 'r') as file:
        results = json.load(file)

    for image in tqdm(os.listdir("test/data/im2gps")):
        if image not in results and ".DS_Store" not in image:
            try:
                print(image)
                res = invoke_agent(image)
                results[image] = res
                with open(json_file_path, 'w') as file:
                    json.dump(results, file)
            except Exception:
                print("ERROR- retrying")
                time.sleep(30)
                res = invoke_agent(image)
                results[image] = res
                with open(json_file_path, 'w') as file:
                    json.dump(results, file)

def get_labels_dict() -> Dict:
        csv_file_path = '/Users/mateuszwitka-jezewski/Documents/Projekty/GeoAI/test/data/scene_M_p_im2gps.csv'
        parsed_data = {}
        with open(csv_file_path, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                img_id = row.pop('img_id')
                parsed_data[img_id] = row 
        return parsed_data


if __name__ == "__main__":
    json_file_path = 'result.json'
    with open(json_file_path, 'r') as file:
        results = json.load(file)
        
    true_coords = get_labels_dict()

    distances = {}
    for name, res in results.items():
        pred_lat = float(res["latitude"])
        pred_long = float(res["longitude"])
        true_lat = float(true_coords.get(name)["gt_lat"])
        true_long = float(true_coords.get(name)["gt_long"])
        dist = calculate_distance_error((pred_lat, pred_long), (true_lat, true_long))
        distances[name] = dist

    import heapq

    value_key_pairs = [(value, key) for key, value in distances.items()]
    top_10_pairs = heapq.nsmallest(10, value_key_pairs)
    top_10_keys = [key for _, key in top_10_pairs]
    for key in top_10_keys:
        print("########################")
        print(key)
        print(distances[key])
        print(results[key])