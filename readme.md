# GeoTagr 🌍 📸 🤖

GeoTagr is an AI-powered tool that predicts the geographical location of photos using a LangChain-based agent system powered by Google's Gemini Flash 1.5 LLM.

## Overview 🎯

GeoTagr analyzes images and returns predicted coordinates along with detailed reasoning for its predictions. You can test it [HERE](https://huggingface.co/spaces/mwitjez/GeoTagr)

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
   git clone https://github.com/mwitjez/GeoTagrBacked.git
   cd GeoTagrBacked
   ```

2. Set up environment variables:
   ```bash
   # Copy the template
   cp .env_template .env
   
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
   uvicorn api:app --reload --port 8000
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
     "latitude": str,
     "longitude": str,
     "reasoning": str,
   }
   ```

### Option 2: Command Line 💻

1. Run with a single image specified in main.py:
   ```bash
   python src/main.py
   ```

### Option 3: Streamlit 🎈

1. Run using Streamlit interface:
   ```bash
   streamlit run app.py
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
