import os
from google.cloud import aiplatform
from dotenv import load_dotenv
from utils.data_processor import DataProcessor

class VertexClient:
    def __init__(self):
        load_dotenv()
        # Initialize Vertex AI
        project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
        location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
        
        if not project_id:
            raise ValueError("GOOGLE_CLOUD_PROJECT not found in environment variables")
        
        try:
            aiplatform.init(project=project_id, location=location)
            # Get the default text model
            self.model = aiplatform.TextGenerationModel.from_pretrained("text-bison@002")
            # Initialize DataProcessor
            self.data_processor = DataProcessor()
        except Exception as e:
            raise ValueError(f"Error initializing Vertex AI model: {str(e)}")
    
    def _get_tools_description(self) -> str:
        """Get description of available tools"""
        return """
        Available Tools:
        1. get_application_details(application_id): Get details for a specific application
        2. get_capability_details(capability_id): Get details for a specific capability
        3. get_consumed_capabilities(application_id): Get all capabilities consumed by an application
        4. get_provided_capabilities(application_id): Get all capabilities provided by an application
        5. get_consuming_applications(capability_id): Get all applications that consume a specific capability
        6. get_providing_applications(capability_id): Get all applications that provide a specific capability
        
        To use these tools, you can call them with appropriate parameters. For example:
        - To get details of application 'APP001': get_application_details('APP001')
        - To get capabilities consumed by 'APP001': get_consumed_capabilities('APP001')
        """
    
    def _execute_tool(self, tool_name: str, params: dict) -> str:
        """Execute a tool based on its name and parameters"""
        try:
            if tool_name == "get_application_details":
                return str(self.data_processor.get_application_details(params['application_id'], self.app_catalog))
            elif tool_name == "get_capability_details":
                return str(self.data_processor.get_capability_details(params['capability_id'], self.cap_catalog))
            elif tool_name == "get_consumed_capabilities":
                return str(self.data_processor.get_consumed_capabilities(params['application_id'], self.consumes_mapping))
            elif tool_name == "get_provided_capabilities":
                return str(self.data_processor.get_provided_capabilities(params['application_id'], self.provides_mapping))
            elif tool_name == "get_consuming_applications":
                return str(self.data_processor.get_consuming_applications(params['capability_id'], self.consumes_mapping))
            elif tool_name == "get_providing_applications":
                return str(self.data_processor.get_providing_applications(params['capability_id'], self.provides_mapping))
            else:
                return f"Unknown tool: {tool_name}"
        except Exception as e:
            return f"Error executing tool {tool_name}: {str(e)}"
        
    async def get_response(self, prompt: str, context: str = None) -> str:
        """
        Get a response from Vertex AI model
        
        Args:
            prompt (str): The user's question or prompt
            context (str, optional): Additional context for the model
            
        Returns:
            str: The model's response
        """
        try:
            # Load data if not already loaded
            if not hasattr(self, 'app_catalog'):
                self.app_catalog, self.cap_catalog, self.consumes_mapping, self.provides_mapping = self.data_processor.load_data()
            
            # Add tools description to the context
            tools_description = self._get_tools_description()
            full_context = f"{tools_description}\n\n{context}" if context else tools_description
            
            # Create the full prompt
            full_prompt = f"""
            Context: {full_context}
            
            Question: {prompt}
            
            Instructions:
            1. Analyze the question and determine if you need to use any tools
            2. If you need to use tools, specify the tool name and parameters
            3. I will execute the tool and provide you with the results
            4. Use the results to provide a comprehensive answer
            
            Your response should be in this format:
            TOOL: <tool_name> <parameters>
            or
            ANSWER: <your analysis>
            """
            
            response = self.model.predict(full_prompt)
            return response.text
        except Exception as e:
            return f"Error getting response from Vertex AI: {str(e)}"
    
    async def analyze_application_capability(self, 
                                          application_data: dict,
                                          capability_data: dict,
                                          consumes_mapping: dict,
                                          provides_mapping: dict,
                                          question: str) -> str:
        """
        Analyze application-capability relationships using Vertex AI
        
        Args:
            application_data (dict): Application catalog data
            capability_data (dict): Capability catalog data
            consumes_mapping (dict): Application consumes capability mapping
            provides_mapping (dict): Application provides capability mapping
            question (str): User's question about the data
            
        Returns:
            str: Analysis result from Vertex AI
        """
        # Store the data for tool execution
        self.app_catalog = application_data
        self.cap_catalog = capability_data
        self.consumes_mapping = consumes_mapping
        self.provides_mapping = provides_mapping
        
        context = f"""
        Application Catalog: {application_data}
        Capability Catalog: {capability_data}
        Consumes Mapping: {consumes_mapping}
        Provides Mapping: {provides_mapping}
        
        Please analyze this data and answer the following question:
        """
        
        response = await self.get_response(question, context)
        
        # Check if the response is a tool call
        if response.startswith("TOOL:"):
            # Parse the tool call
            tool_parts = response[5:].strip().split()
            tool_name = tool_parts[0]
            params = {}
            
            # Parse parameters (assuming format: param_name=value)
            for part in tool_parts[1:]:
                if '=' in part:
                    key, value = part.split('=')
                    params[key] = value.strip("'\"")
            
            # Execute the tool
            tool_result = self._execute_tool(tool_name, params)
            
            # Get a new response with the tool result
            return await self.get_response(
                f"Tool {tool_name} returned: {tool_result}\n\nPlease provide a comprehensive answer to the original question: {question}",
                context
            )
        
        return response 