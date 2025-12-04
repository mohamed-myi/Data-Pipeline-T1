from typing import List, Dict, Any


def checkRequired(record, required_fields):
    '''
    Check if record contains all required fields. Returns True if all required fields present, False otherwise.
    '''
    if not record:
        return False
    
    for field in required_fields:
        if field not in record or record[field] is None or str(record[field]).strip() == '':
            return False
    
    return True


def cleanRecord(record, schema):
    '''
    Clean and validate single record against schema. Takes record dict and schema dict with field types. Returns cleaned record dict or None if validation fails.
    '''
    if not record or not isinstance(record, dict):
        return None
    
    cleaned = {}
    
    for field, field_type in schema.items():
        value = record.get(field)
        
        if value is None or str(value).strip() == '':
            cleaned[field] = None
            continue
        
        try:
            if field_type == 'string':
                cleaned[field] = str(value).strip()
            
            elif field_type == 'integer':
                cleaned[field] = int(value)
            
            elif field_type == 'float':
                cleaned[field] = float(value)
            
            elif field_type == 'boolean':
                if isinstance(value, bool):
                    cleaned[field] = value
                else:
                    str_val = str(value).lower()
                    cleaned[field] = str_val in ['true', '1', 'yes', 'on']
            
            else:
                cleaned[field] = value
        
        except (ValueError, TypeError):
            return None
    
    # Returns cleaned record if all fields processed successfully
    return cleaned


def cleanData(records, schema, required_fields=None):
    '''
    Clean and validate list of records against schema. Takes list of record dicts, schema dict, optional required fields list. Returns list of valid cleaned records.
    '''
    if not records or not schema:
        return []
    
    if not isinstance(records, list):
        records = [records]
    
    cleaned_records = []
    skipped_count = 0
    
    for record in records:
        if required_fields and not checkRequired(record, required_fields):
            skipped_count += 1
            continue
        
        cleaned = cleanRecord(record, schema)
        
        if cleaned is not None:
            cleaned_records.append(cleaned)
        else:
            skipped_count += 1
    
    if skipped_count > 0:
        print(f"Skipped {skipped_count} invalid records during cleaning")
    
    # Returns list of successfully cleaned and validated records
    return cleaned_records


def removeDuplicates(records, key_fields):
    '''
    Remove duplicate records based on key fields. Takes list of records and list of field names to check for duplicates. Returns list with duplicates removed, keeping first occurrence.
    '''
    if not records or not key_fields:
        return records
    
    seen = set()
    unique_records = []
    
    for record in records:
        key_tuple = tuple(record.get(field) for field in key_fields)
        
        if key_tuple not in seen:
            seen.add(key_tuple)
            unique_records.append(record)
    
    duplicates_removed = len(records) - len(unique_records)
    if duplicates_removed > 0:
        print(f"Removed {duplicates_removed} duplicate records")
    
    # Returns deduplicated list of records
    return unique_records