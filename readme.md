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

### Prerequisites ⚙️

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/geotagr.git
   cd geotagr
   ```

2. Set up environment variables:
   ```bash
   # Copy the template
   cp .env-template .env
   
   # Edit .env with your credentials
   nano .env
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Option 1: REST API 🌐

1. Start the API server:
   ```bash
   uvicorn app:app --reload --port 8000
   ```

2. Access the API:
   - Interactive Documentation: Visit `http://localhost:8000/docs`
   - Direct API endpoint: `http://localhost:8000/process-image`

3. Make a prediction:
   ```bash
   curl -X POST "http://localhost:8000/process-image" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@/path/to/your/image.jpg"
   ```

4. Response Format:
   ```json
   {
     "latitude": float,      // Predicted latitude coordinate
     "longitude": float,     // Predicted longitude coordinate
     "reasoning": string,    // AI's explanation for the prediction
   }
   ```

### Option 2: Command Line 💻

1. Run with a single image specified in main.py:
   ```bash
   python src/main.py
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
