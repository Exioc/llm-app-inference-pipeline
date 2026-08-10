from typing import Set, Any
from pydantic import BaseModel, Field, model_validator

class PermissionCatalog(BaseModel):
    permissions: Set[str] = Field(default_factory=set)

    @model_validator(mode="before")
    @classmethod
    def extract_permission_ids_to_set(cls, data: Any) -> Any:
        if isinstance(data, list):
            perm_ids = set()
            for group in data:
                for perm in group.get("permissions", []):
                    perm_id = perm.get("id")
                    if perm_id:
                        perm_ids.add(perm_id)
            return {"permissions": perm_ids}
        return data