# GeoTagr 🌍📸 🤖

GeoTagr is an AI-powered tool that predicts the geographical location of photos using a LangChain-based agent system powered by Google's Gemini Flash 1.5 LLM.

## Overview 🎯

GeoTagr analyzes images and returns predicted coordinates along with detailed reasoning for its predictions.

## Project Structure 📁

```
.
├── src/          # Main application code and agent implementation
└── test/         # Test images and benchmarking scripts
```

## Usage 🔄

### Option 1: REST API 🌐

1. Start the API server:
   ```bash
   uvicorn app:app --reload
   ```

2. Access the API:
   - Use the Swagger UI at `/docs`
   - Send HTTP requests directly

3. Response Format:
   ```json
   {
     "latitude": float,
     "longitude": float,
     "reasoning": string
   }
   ```

### Option 2: Command Line 💻

Run the script directly with test images:
```bash
python3 src/main.py
```

## Performance 📊

Benchmark results on the Im2GPS dataset:

| Metric | Accuracy |
|--------|----------|
| Within 1km | 13.9% |
| Within 25km | 43.9% |
| Within 200km | 64.1% |
| Within 750km | 80.2% |
| Within 2500km | 92.8% |

Additional Statistics:
- Mean Distance Error: 843.23 km
- Median Distance Error: 49.06 km
