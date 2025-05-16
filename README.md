# Application-Capability Analysis System

This system analyzes the relationships between applications and capabilities using CSV data files and Gemini Flash 2.x for natural language processing.

## Project Structure

- `mcp_client/` - Streamlit-based client application
- `mcp_server/` - FastAPI-based server for data processing
- `llm_chat/` - Gemini Flash 2.x integration
- `data/` - Directory for CSV files
- `utils/` - Utility functions for data processing

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
Create a `.env` file with:
```
GOOGLE_API_KEY=your_gemini_api_key
```

3. Place your CSV files in the `data/` directory:
- application_catalog.csv
- capability_catalog.csv
- application_consumes_capability_mapping.csv
- application_provides_capability_mapping.csv

## Running the Application

1. Start the server (in one terminal):
```bash
python mcp_server/server.py
```

2. Start the client (in another terminal):
```bash
streamlit run mcp_client/app.py
```

The application will open in your web browser with three main sections:
- Natural Language Query
- Application Analysis
- Capability Analysis

## Sample Prompts

### 1. Application Analysis Questions
- "Which applications consume the most capabilities?"
- "List all cloud-based applications and their capabilities"
- "What are all the capabilities consumed by the Customer Portal?"
- "Which applications are managed by John Smith?"
- "Show me all applications that consume the User Authentication capability"

### 2. Capability Analysis Questions
- "What capabilities are provided by cloud-based applications?"
- "List all capabilities in the Identity Management context"
- "Which capabilities are most commonly consumed across applications?"
- "Show me all capabilities that are consumed by more than 2 applications"
- "What are the capabilities provided by the Payment Gateway?"

### 3. Relationship Analysis Questions
- "Find all applications that both provide and consume capabilities"
- "Which applications have dependencies on the Data Storage capability?"
- "Show me the relationship between Order Management and its consumed capabilities"
- "What is the dependency chain for the Customer Portal?"
- "Which capabilities are provided by on-premise applications?"

### 4. Platform and Type Analysis
- "Compare the capabilities of cloud vs on-premise applications"
- "What types of applications consume the most capabilities?"
- "List all microservices and their provided capabilities"
- "Show me the distribution of capabilities across different application types"
- "Which legacy applications consume cloud-based capabilities?"

### 5. Team and Ownership Questions
- "Who are the system architects for applications that provide authentication capabilities?"
- "List all applications managed by each delivery lead"
- "Show me the service owners for applications that consume payment processing"
- "Which team members are responsible for the most critical capabilities?"
- "What capabilities are managed by each service owner?"

### 6. Business Context Questions
- "What are all the capabilities related to Supply Chain?"
- "Show me the relationships between Financial Services capabilities"
- "List all capabilities that support Business Intelligence"
- "What are the dependencies between Order Processing and other capabilities?"
- "How do the Identity Management capabilities interact with other systems?"

## Features

- Analyze relationships between applications and capabilities
- Natural language querying of the dataset
- Visualization of application-capability relationships
- Detailed analysis of application and capability attributes
- Team and ownership analysis
- Platform and type-based analysis
- Business context analysis 