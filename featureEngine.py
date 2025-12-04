from typing import List, Dict, Any
import math


def normalizeNumeric(records, field):
    '''
    Normalize numeric field to 0-1 range using min-max scaling. Takes list of records and field name. Returns list of records with normalized field added as field_normalized.
    '''
    if not records or not field:
        return records
    
    values = [float(r.get(field, 0)) for r in records if r.get(field) is not None]
    
    if not values:
        return records
    
    min_val = min(values)
    max_val = max(values)
    range_val = max_val - min_val
    
    if range_val == 0:
        for r in records:
            r[f"{field}_normalized"] = 0.5
        return records
    
    for r in records:
        if r.get(field) is not None:
            normalized = (float(r[field]) - min_val) / range_val
            r[f"{field}_normalized"] = round(normalized, 4)
        else:
            r[f"{field}_normalized"] = None
    
    # Returns records with new normalized field added
    return records


def categorizeField(records, field, bins):
    '''
    Categorize numeric field into bins. Takes list of records, field name, and list of bin thresholds. Returns list of records with new category field added as field_category.
    '''
    if not records or not field or not bins:
        return records
    
    bins = sorted(bins)
    
    for r in records:
        value = r.get(field)
        
        if value is None:
            r[f"{field}_category"] = None
            continue
        
        try:
            value = float(value)
            category = 0
            
            for threshold in bins:
                if value >= threshold:
                    category += 1
            
            r[f"{field}_category"] = category
        except (ValueError, TypeError):
            r[f"{field}_category"] = None
    
    # Returns records with new category field added
    return records


def createRatioFeature(records, numerator_field, denominator_field, feature_name):
    '''
    Create ratio feature from two numeric fields. Takes list of records, numerator field name, denominator field name, and output feature name. Returns list of records with ratio feature added, handles division by zero.
    '''
    if not records or not numerator_field or not denominator_field or not feature_name:
        return records
    
    for r in records:
        numerator = r.get(numerator_field)
        denominator = r.get(denominator_field)
        
        if numerator is None or denominator is None:
            r[feature_name] = None
            continue
        
        try:
            num = float(numerator)
            denom = float(denominator)
            
            if denom == 0:
                r[feature_name] = None
            else:
                r[feature_name] = round(num / denom, 4)
        except (ValueError, TypeError):
            r[feature_name] = None
    
    # Returns records with new ratio feature added
    return records