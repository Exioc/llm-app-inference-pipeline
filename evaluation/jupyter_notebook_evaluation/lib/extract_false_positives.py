def extract_false_positives(data):
    """
    Compares 'apk_permissions' (ground truth) with 'inferred_permissions' (prediction)
    and returns a list of dictionaries containing only the false positive permissions.
    """
    result = []
    
    for item in data:
        # Convert the lists to sets for easy comparison
        apk_set = set(item.get('apk_permissions', []))
        inferred_set = set(item.get('inferred_permissions', []))
        
        # Calculate false positives: Everything in inferred_set but not in apk_set
        fp_permissions = list(inferred_set - apk_set)
        
        # Append the result as a new dictionary to the list
        result.append({
            'fp_permissions': fp_permissions
        })
        
    return result