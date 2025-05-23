import os
import google.generativeai as genai
from dotenv import load_dotenv

class GeminiClient:
    def __init__(self):
        load_dotenv()
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        
        genai.configure(api_key=api_key)
        # List available models
        try:
            models = [m for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            if not models:
                raise ValueError("No suitable models found")
            # Use the first available model that supports generateContent
            self.model = genai.GenerativeModel(models[0].name)
        except Exception as e:
            raise ValueError(f"Error initializing Gemini model: {str(e)}")
        
    async def get_response(self, prompt: str, context: str = None) -> str:
        """
        Get a response from Gemini model
        
        Args:
            prompt (str): The user's question or prompt
            context (str, optional): Additional context for the model
            
        Returns:
            str: The model's response
        """
        try:
            full_prompt = f"{context}\n\n{prompt}" if context else prompt
            response = await self.model.generate_content_async(full_prompt)
            return response.text
        except Exception as e:
            return f"Error getting response from Gemini: {str(e)}"
    
    async def analyze_application_capability(self, 
                                          application_data: dict,
                                          capability_data: dict,
                                          consumes_mapping: dict,
                                          provides_mapping: dict,
                                          question: str) -> str:
        """
        Analyze application-capability relationships using Gemini
        
        Args:
            application_data (dict): Application catalog data
            capability_data (dict): Capability catalog data
            consumes_mapping (dict): Application consumes capability mapping
            provides_mapping (dict): Application provides capability mapping
            question (str): User's question about the data
            
        Returns:
            str: Analysis result from Gemini
        """
        context = f"""
        Application Catalog: {application_data}
        Capability Catalog: {capability_data}
        Consumes Mapping: {consumes_mapping}
        Provides Mapping: {provides_mapping}
        
        Please analyze this data and answer the following question:
        """
        
        return await self.get_response(question, context) 