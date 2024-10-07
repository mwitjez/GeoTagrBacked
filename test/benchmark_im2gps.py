import base64
import csv
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Tuple

import haversine as hs
import numpy as np
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from PIL import Image
from tqdm import tqdm

from src.agent import Agent

@dataclass
class Coordinates:
    latitude: float
    longitude: float

    @classmethod
    def from_dict(cls, data: Dict[str, float]) -> 'Coordinates':
        return cls(
            latitude=float(data['latitude']), 
            longitude=float(data['longitude'])
        )

    def to_tuple(self) -> Tuple[float, float]:
        return (self.latitude, self.longitude)

class GeolocationEvaluator:
    def __init__(self, data_dir: Path, config_path: Path):
        self.data_dir = Path(data_dir)
        self.config = self._load_config(config_path)
        self.results_path = Path('test/im2gps_result.json')

    @staticmethod
    def _load_config(config_path: Path) -> Dict:
        return json.loads(config_path.read_text())

    def invoke_agent(self, image_path: Path) -> Dict:
        """Invoke the agent with an image and return its prediction."""
        image = Image.open(image_path)
        image_bytes = image_path.read_bytes()
        image_data = base64.b64encode(image_bytes).decode("utf-8")
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

    @staticmethod
    def calculate_distance_error(pred: Coordinates, true: Coordinates) -> float:
        """Calculate the haversine distance between predicted and true coordinates."""
        return hs.haversine(pred.to_tuple(), true.to_tuple())

    @staticmethod
    def calculate_metrics(distances: np.ndarray) -> Dict[str, float]:
        """Calculate evaluation metrics from distance errors."""
        return {
            'mean_distance_error': float(np.mean(distances)),
            'median_distance_error': float(np.median(distances)),
            'std_distance_error': float(np.std(distances)),
            'accuracy_1km': float(np.mean(distances <= 1)),
            'accuracy_25km': float(np.mean(distances <= 25)),
            'accuracy_200km': float(np.mean(distances <= 200)),
            'accuracy_750km': float(np.mean(distances <= 750)),
        }

    def load_ground_truth(self, csv_path: Path) -> Dict[str, Dict]:
        """Load ground truth coordinates from CSV file."""
        with csv_path.open() as f:
            reader = csv.DictReader(f)
            return {row.pop('img_id'): row for row in reader}

    def generate_results(self):
        """Generate and save results for all images in the dataset."""
        if not self.results_path.exists():
            self.results_path.write_text("{}")

        results = json.loads(self.results_path.read_text())

        for image_path in tqdm(self.data_dir.glob("*")):
            if image_path.name == ".DS_Store" or image_path.name in results:
                continue
            print(f"Processing {image_path.name}")
            res = self.invoke_agent(image_path)
            results[image_path.name] = res
            self.results_path.write_text(json.dumps(results))


def main():
    load_dotenv()

    # Initialize evaluator
    evaluator = GeolocationEvaluator(
        data_dir=Path("test/data/im2gps"),
        config_path=Path("src/config.json")
    )

    # Generate results
    evaluator.generate_results()

    # Load results and ground truth
    results = json.loads(evaluator.results_path.read_text())
    true_coords = evaluator.load_ground_truth(Path('test/data/scene_M_p_im2gps.csv'))

    # Calculate distances
    distances = {}
    for name, res in results.items():
        pred_coords = Coordinates.from_dict(res)
        true_coords_dict = {
            'latitude': true_coords[name]["gt_lat"],
            'longitude': true_coords[name]["gt_long"]
        }
        true_coords_obj = Coordinates.from_dict(true_coords_dict)
        dist = evaluator.calculate_distance_error(pred_coords, true_coords_obj)
        distances[name] = dist

    # Print top 10 results
    value_key_pairs = [(value, key) for key, value in distances.items()]
    top_10_pairs = sorted(value_key_pairs)[:10]

    for distance, image_name in top_10_pairs:
        print("=" * 40)
        print(f"Image: {image_name}")
        print(f"Distance Error: {distance:.2f} km")
        print(f"Prediction: {results[image_name]}")

if __name__ == "__main__":
    main()