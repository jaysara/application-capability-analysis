# Application-Capability Analysis System

This system analyzes relationships between applications and capabilities using Vertex AI for natural language processing and analysis.

## Features

- Natural language querying of application-capability relationships
- Detailed analysis of application and capability dependencies
- Interactive web interface for data exploration
- RESTful API for programmatic access
- Integration with Google Cloud Vertex AI for advanced analysis

## Prerequisites

- Python 3.9 or higher
- Google Cloud account with Vertex AI API enabled
- Google Cloud credentials (service account key or application default credentials)

## Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd ai-mcp-cursor
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install required packages:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. Set up Google Cloud credentials:
   - Option 1: Using service account key
     ```bash
     export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account-key.json"
     ```
   - Option 2: Using gcloud CLI
     ```bash
     gcloud auth application-default login
     ```

5. Create a `.env` file in the project root:
   ```
   GOOGLE_CLOUD_PROJECT=your-project-id
   GOOGLE_CLOUD_LOCATION=us-central1
   ```

## Running the Application

1. Start the server (in one terminal):
   ```bash
   source venv/bin/activate
   cd mcp_server
   python3 server.py
   ```
   The server will start on http://localhost:8000

2. Start the client (in another terminal):
   ```bash
   source venv/bin/activate
   cd mcp_client
   streamlit run app.py
   ```
   The client will be available at http://localhost:8501

## Using the System

### Natural Language Analysis

The system now uses Vertex AI to provide natural language analysis of application-capability relationships. You can ask questions like:

- "What capabilities does Application X provide?"
- "Which applications consume the same capabilities as Application Y?"
- "Tell me about the relationships between Application X and its capabilities"

The system will automatically:
1. Understand your question
2. Use appropriate data tools to gather information
3. Provide a comprehensive analysis

### API Endpoints

- `GET /`: Server status
- `POST /analyze`: Natural language analysis of relationships
- `GET /applications`: List all applications
- `GET /capabilities`: List all capabilities
- `GET /application/{application_id}`: Get application details
- `GET /capability/{capability_id}`: Get capability details

### Example API Usage

```python
import requests

# Natural language analysis
response = requests.post(
    "http://localhost:8000/analyze",
    json={"question": "What capabilities does Application X provide?"}
)
print(response.json())

# Get application details
response = requests.get("http://localhost:8000/application/APP001")
print(response.json())
```

## Data Structure

The system uses four CSV files in the `data` directory:

1. `application_catalog.csv`: Application information
2. `capability_catalog.csv`: Capability information
3. `application_consumes_capability_mapping.csv`: Application-capability consumption relationships
4. `application_provides_capability_mapping.csv`: Application-capability provision relationships

## Architecture

The system consists of three main components:

1. **Data Processor** (`utils/data_processor.py`):
   - Handles data loading and basic filtering
   - Provides methods for querying relationships

2. **Vertex AI Client** (`llm_chat/vertex_client.py`):
   - Integrates with Google Cloud Vertex AI
   - Provides natural language analysis
   - Uses DataProcessor methods as tools for detailed analysis

3. **Web Interface**:
   - FastAPI server for API endpoints
   - Streamlit client for interactive interface

## Troubleshooting

1. If you see SSL-related warnings:
   ```bash
   xcode-select --install
   pip install watchdog
   ```

2. If packages are not found, ensure you're in the virtual environment:
   ```bash
   source venv/bin/activate
   ```

3. If Vertex AI is not working:
   - Verify your Google Cloud credentials
   - Check that Vertex AI API is enabled
   - Ensure your project ID and location are correct in `.env`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request 