import pandas as pd
from typing import Dict, List, Tuple

class DataProcessor:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        
    def load_data(self) -> Tuple[Dict, Dict, Dict, Dict]:
        """
        Load all CSV files and return their data as dictionaries
        
        Returns:
            Tuple containing:
            - Application catalog data
            - Capability catalog data
            - Consumes mapping data
            - Provides mapping data
        """
        try:
            # Load application catalog
            app_catalog = pd.read_csv(f"{self.data_dir}/application_catalog.csv")
            app_catalog_dict = app_catalog.to_dict('records')
            
            # Load capability catalog
            cap_catalog = pd.read_csv(f"{self.data_dir}/capability_catalog.csv")
            cap_catalog_dict = cap_catalog.to_dict('records')
            
            # Load consumes mapping
            consumes_mapping = pd.read_csv(f"{self.data_dir}/application_consumes_capability_mapping.csv")
            consumes_dict = consumes_mapping.to_dict('records')
            
            # Load provides mapping
            provides_mapping = pd.read_csv(f"{self.data_dir}/application_provides_capability_mapping.csv")
            provides_dict = provides_mapping.to_dict('records')
            
            return app_catalog_dict, cap_catalog_dict, consumes_dict, provides_dict
            
        except Exception as e:
            raise Exception(f"Error loading data: {str(e)}")
    
    def get_application_details(self, application_id: str, app_catalog: List[Dict]) -> Dict:
        """Get details for a specific application"""
        for app in app_catalog:
            if app['application_id'] == application_id:
                return app
        return {}
    
    def get_capability_details(self, capability_id: str, cap_catalog: List[Dict]) -> Dict:
        """Get details for a specific capability"""
        for cap in cap_catalog:
            if cap['capability_id'] == capability_id:
                return cap
        return {}
    
    def get_consumed_capabilities(self, application_id: str, consumes_mapping: List[Dict]) -> List[Dict]:
        """Get all capabilities consumed by an application"""
        return [mapping for mapping in consumes_mapping if mapping['application_id'] == application_id]
    
    def get_provided_capabilities(self, application_id: str, provides_mapping: List[Dict]) -> List[Dict]:
        """Get all capabilities provided by an application"""
        return [mapping for mapping in provides_mapping if mapping['application_id'] == application_id]
    
    def get_consuming_applications(self, capability_id: str, consumes_mapping: List[Dict]) -> List[Dict]:
        """Get all applications that consume a specific capability"""
        return [mapping for mapping in consumes_mapping if mapping['capability_id'] == capability_id]
    
    def get_providing_applications(self, capability_id: str, provides_mapping: List[Dict]) -> List[Dict]:
        """Get all applications that provide a specific capability"""
        return [mapping for mapping in provides_mapping if mapping['capability_id'] == capability_id] 