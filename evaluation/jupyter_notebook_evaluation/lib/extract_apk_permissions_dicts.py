def extract_apk_permissions_dicts(data_list: list, outer_key: str = "set_collection_data") -> list:
    """
    Extracts 'apk_permissions' from nested dictionaries and 
    returns them as a list of dictionaries.
    """
    extracted_permissions = []
    
    for item in data_list:
        # Safely check if the outer dictionary exists
        if outer_key in item:
            inner_dict = item[outer_key]
            
            # Check if the target key exists in the inner dictionary
            if "apk_permissions" in inner_dict:
                
                # Create a new dict with just the apk_permissions and append it
                extracted_permissions.append({
                    "apk_permissions": inner_dict["apk_permissions"]
                })
                
    return extracted_permissions