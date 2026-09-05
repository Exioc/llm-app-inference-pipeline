# LABEL_TO_PERMISSIONS
from typing import Dict, List
from pydantic import BaseModel, Field, model_validator

class AppPermission(BaseModel):
    name: str = Field(...,description="The technical Android permission name, e.g. 'android.permission.ACCESS_WIFI_STATE'")
    label: str = Field(...,description="The human-readable permission label, e.g. 'view Wi-Fi connections'")

# Defines a model to represent the processed permissions mapping in the pipeline state.
class ProcessedPermissions(BaseModel):
    # Key = category (e.g., "Identity"), Value = list of AppPermission objects
    permissions_map: Dict[str, List[AppPermission]] = Field(default_factory=dict)


# Defines a model matching the structure of AndroGuard's "label_permission_mapping" file.
class PermissionElement(BaseModel):
    description: str
    description_ptr: str
    label: str
    label_ptr: str
    name: str
    permission_group: str = Field(..., alias="permissionGroup")
    protection_level: str = Field(..., alias="protectionLevel")

# Model that automatically transforms permissions dictionary keys from permission names to labels for easier mapping.
class AndroidPermissionsModel(BaseModel):
    permissions: Dict[str, PermissionElement]

    @model_validator(mode="before")
    @classmethod
    def transform_keys_to_labels(cls, data: dict) -> dict:
        # if permissions key is not present or is not a dictionary, return the data as is
        if "permissions" not in data or not isinstance(data["permissions"], dict):
            return data

        transformed_permissions = {}
        
        # Change the key to label to make mapping easier.
        for old_key, perm_body in data["permissions"].items():
            # Get the label from the permission body. If it's empty, fallback to the original permission name.
            new_key = perm_body.get("label") or perm_body.get("name") or old_key
            
            # Save the permission body under the new key (label)
            transformed_permissions[new_key] = perm_body

        # Replace the original permissions dict with the transformed one
        data["permissions"] = transformed_permissions
        return data

    class Config:
        populate_by_name = True