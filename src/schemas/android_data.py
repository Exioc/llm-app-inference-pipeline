from typing import List
from pydantic import BaseModel, Field

class Permission(BaseModel):
    id: str = Field(description="The unique ID of the permission, e.g., READ_CALENDAR")
    protection_level: str = Field(description="The protection level, e.g., dangerous or normal")
    description: str = Field(description="The exact explanation of what this permission allows")

#PermissionGroupInfo
class PermissionGroupSummary(BaseModel):
    group_name: str = Field(description="The name of the permission group, e.g., CALENDAR")
    description: str = Field(description="Description of what this group is responsible for as a whole")

#PermissionGroup
class PermissionGroup(PermissionGroupSummary):
    permissions: List[Permission] = Field(
        description="A list of all individual permissions belonging to this group."
    )

#PermissionGroupCatalog
class PermissionGroupSummaries(BaseModel):
    groups: List[PermissionGroupSummary] = Field(
        description="A list of all available permission groups (including their names and group descriptions only)."
    )

class PermissionGroupCollection(BaseModel):
    groups: List[PermissionGroup] = Field(
        description="A list of all permission groups, flatly combined with their respective fine-grained sub-permissions."
    )

