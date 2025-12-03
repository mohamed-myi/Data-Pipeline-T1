import pytest
import json
import csv
import tempfile
import os
from unittest.mock import patch, MagicMock
from dataLoader import loadFromAPI, loadFromFile


def test_loadFromAPIList():
    '''
    Test loading data from API that returns list of records
    '''
    mock_data = [
        {"id": 1, "name": "record1"},
        {"id": 2, "name": "record2"}
    ]
    
    with patch('dataLoader.requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = mock_data
        mock_get.return_value = mock_response
        
        result = loadFromAPI("https://api.example.com/data")
        assert len(result) == 2
        assert result[0]["id"] == 1


def test_loadFromAPIDict():
    '''
    Test loading data from API that returns dict with results key
    '''
    mock_data = {"results": [{"id": 1, "name": "record1"}]}
    
    with patch('dataLoader.requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = mock_data
        mock_get.return_value = mock_response
        
        result = loadFromAPI("https://api.example.com/data")
        assert len(result) == 1
        assert result[0]["id"] == 1


def test_loadFromAPIError():
    '''
    Test loading from API with connection error returns empty list
    '''
    with patch('dataLoader.requests.get') as mock_get:
        mock_get.side_effect = Exception("Connection failed")
        
        result = loadFromAPI("https://api.example.com/data")
        assert result == []


def test_loadFromFileJSON():
    '''
    Test loading data from JSON file
    '''
    test_data = [
        {"id": 1, "name": "item1"},
        {"id": 2, "name": "item2"}
    ]
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(test_data, f)
        temp_file = f.name
    
    try:
        result = loadFromFile(temp_file)
        assert len(result) == 2
        assert result[0]["id"] == 1
    finally:
        os.unlink(temp_file)


def test_loadFromFileCSV():
    '''
    Test loading data from CSV file
    '''
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        writer = csv.DictWriter(f, fieldnames=['id', 'name'])
        writer.writeheader()
        writer.writerow({'id': '1', 'name': 'item1'})
        writer.writerow({'id': '2', 'name': 'item2'})
        temp_file = f.name
    
    try:
        result = loadFromFile(temp_file)
        assert len(result) == 2
        assert result[0]['id'] == '1'
    finally:
        os.unlink(temp_file)


def test_loadFromFileNotFound():
    '''
    Test loading from non-existent file returns empty list
    '''
    result = loadFromFile("/nonexistent/file.json")
    assert result == []


def test_loadFromFileUnsupported():
    '''
    Test loading from unsupported file format returns empty list
    '''
    with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as f:
        temp_file = f.name
    
    try:
        result = loadFromFile(temp_file)
        assert result == []
    finally:
        os.unlink(temp_file)