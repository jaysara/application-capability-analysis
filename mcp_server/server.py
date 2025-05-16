from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.data_processor import DataProcessor
from llm_chat.gemini_client import GeminiClient

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
data_processor = DataProcessor()
gemini_client = GeminiClient()

class Query(BaseModel):
    question: str

@app.get("/")
async def root():
    return {"message": "Application-Capability Analysis Server"}

@app.post("/analyze")
async def analyze_data(query: Query):
    try:
        # Load all data
        app_catalog, cap_catalog, consumes_mapping, provides_mapping = data_processor.load_data()
        
        # Get analysis from Gemini
        response = await gemini_client.analyze_application_capability(
            application_data=app_catalog,
            capability_data=cap_catalog,
            consumes_mapping=consumes_mapping,
            provides_mapping=provides_mapping,
            question=query.question
        )
        
        return {"response": response}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/applications")
async def get_applications():
    try:
        app_catalog, _, _, _ = data_processor.load_data()
        return {"applications": app_catalog}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/capabilities")
async def get_capabilities():
    try:
        _, cap_catalog, _, _ = data_processor.load_data()
        return {"capabilities": cap_catalog}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/application/{application_id}")
async def get_application_details(application_id: str):
    try:
        app_catalog, cap_catalog, consumes_mapping, provides_mapping = data_processor.load_data()
        
        app_details = data_processor.get_application_details(application_id, app_catalog)
        if not app_details:
            raise HTTPException(status_code=404, detail="Application not found")
            
        consumed_caps = data_processor.get_consumed_capabilities(application_id, consumes_mapping)
        provided_caps = data_processor.get_provided_capabilities(application_id, provides_mapping)
        
        return {
            "application": app_details,
            "consumed_capabilities": consumed_caps,
            "provided_capabilities": provided_caps
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/capability/{capability_id}")
async def get_capability_details(capability_id: str):
    try:
        app_catalog, cap_catalog, consumes_mapping, provides_mapping = data_processor.load_data()
        
        cap_details = data_processor.get_capability_details(capability_id, cap_catalog)
        if not cap_details:
            raise HTTPException(status_code=404, detail="Capability not found")
            
        consuming_apps = data_processor.get_consuming_applications(capability_id, consumes_mapping)
        providing_apps = data_processor.get_providing_applications(capability_id, provides_mapping)
        
        return {
            "capability": cap_details,
            "consuming_applications": consuming_apps,
            "providing_applications": providing_apps
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 