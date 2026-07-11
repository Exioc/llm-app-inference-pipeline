from typing import Dict, List
from pydantic import BaseModel, Field, model_validator

class AppPermission(BaseModel):
    name: str = Field(..., description="Der technische Android-Name, z.B. 'android.permission.ACCESS_WIFI_STATE'")
    label: str = Field(..., description="Das lesbare Label, z.B. 'view Wi-Fi connections'")

class ProcessedPermissions(BaseModel):
    # Das ist deine Struktur aus Option 1:
    # Key = Kategorie (z.B. "Identity"), Value = Liste von AppPermission-Objekten
    permissions_map: Dict[str, List[AppPermission]] = Field(default_factory=dict)

class PermissionElement(BaseModel):
    description: str
    description_ptr: str
    label: str
    label_ptr: str
    name: str
    permission_group: str = Field(..., alias="permissionGroup")
    protection_level: str = Field(..., alias="protectionLevel")

class AndroidPermissionsModel(BaseModel):
    permissions: Dict[str, PermissionElement]

    @model_validator(mode="before")
    @classmethod
    def transform_keys_to_labels(cls, data: dict) -> dict:
        # Falls "permissions" nicht im Input ist, machen wir nichts
        if "permissions" not in data or not isinstance(data["permissions"], dict):
            return data

        transformed_permissions = {}
        
        for old_key, perm_body in data["permissions"].items():
            # Wir holen das Label. Wenn das Label im JSON leer ist (""), 
            # nehmen wir als Fallback den echten Namen der Permission.
            new_key = perm_body.get("label") or perm_body.get("name") or old_key
            
            # Falls im JSON das Feld "name" fehlt, fügen wir es zur Sicherheit hinzu,
            # da dein PermissionElement-Modell es als Pflichtfeld verlangt.
            if "name" not in perm_body:
                perm_body["name"] = old_key
                
            transformed_permissions[new_key] = perm_body

        # Wir ersetzen das alte Permissions-Dict mit unserem neuen, umgebauten Dict
        data["permissions"] = transformed_permissions
        return data

    class Config:
        populate_by_name = True