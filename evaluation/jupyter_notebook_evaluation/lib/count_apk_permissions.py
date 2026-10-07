from collections import Counter

def count_apk_permissions(data_list: list) -> dict:
    """
    Counts the occurrences of all 'apk_permissions' across the provided list of dictionaries.
    Returns a single dictionary where the key is the permission name and the value is the count.
    """
    # Flatten all permission lists into a single stream
    all_permissions = [
        perm 
        for item in data_list 
        for perm in item.get("apk_permissions", [])
    ]
    
    # Count the occurrences of each permission
    counts = Counter(all_permissions)
    
    # Convert directly to a dictionary, keeping the frequency sorting
    return dict(counts.most_common())