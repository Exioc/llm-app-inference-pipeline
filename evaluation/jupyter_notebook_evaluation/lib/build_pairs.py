def build_pairs(runs: list, key_a: str, key_b: str) -> list:
    """
    Extracts two specific keys from the nested 'set_collection_data' 
    and returns them as a list of dictionaries.
    """
    extracted_pairs = []
    
    for run in runs:
        # Extract the inner dictionary into a variable for better readability
        nested_data = run['set_collection_data']
        
        # Check if both requested keys exist in this specific run
        if key_a in nested_data and key_b in nested_data:
            
            # Create a new dictionary containing just these two values
            pair_dict = {
                key_a: nested_data[key_a],
                key_b: nested_data[key_b]
            }
            
            # Append it to the final result list
            extracted_pairs.append(pair_dict)
            
    return extracted_pairs