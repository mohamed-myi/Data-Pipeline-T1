import requests
import json
import csv
from typing import List, Dict, Any


def loadFromAPI(endpoint, params=None):
    '''
    Fetch data from API endpoint with optional query parameters. Returns list of dictionaries representing JSON response data.
    '''
    try:
        response = requests.get(endpoint, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        # Handle both dict and list responses
        if isinstance(data, list):
            # Returns list of records from API
            return data
        elif isinstance(data, dict):
            # Try to extract items from common response structures
            if "results" in data:
                return data["results"]
            elif "data" in data:
                return data["data"]
            elif "items" in data:
                return data["items"]
            else:
                # Returns wrapped response as single item
                return [data]
        
        return []
    except requests.exceptions.RequestException as e:
        print(f"Error loading from API {endpoint}: {e}")
        return []


def loadFromFile(file_path):
    '''
    Load data from CSV or JSON file. Returns list of dictionaries representing file records.
    '''
    try:
        if file_path.endswith('.json'):
            with open(file_path, 'r') as f:
                data = json.load(f)
                
                if isinstance(data, list):
                    # Returns list of records from JSON file
                    return data
                else:
                    # Returns wrapped response as single item
                    return [data]
        
        elif file_path.endswith('.csv'):
            records = []
            with open(file_path, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    records.append(row)
            
            # Returns list of records from CSV file
            return records
        
        else:
            print(f"Unsupported file format: {file_path}")
            return []
    
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return []
    except Exception as e:
        print(f"Error loading from file {file_path}: {e}")
        return []