from typing import List
from pydantic import BaseModel, Field

# Describe a single permission with its ID, protection level, and description
class Permission(BaseModel):
    id: str = Field(description="The unique ID of the permission, e.g., READ_CALENDAR")
    protection_level: str = Field(description="The protection level, e.g., dangerous or normal")
    description: str = Field(description="The exact explanation of what this permission allows")

# Describe a permission group with its name and description, without listing individual permissions
class PermissionGroupSummary(BaseModel):
    group_name: str = Field(description="The name of the permission group, e.g., CALENDAR")
    description: str = Field(description="Description of what this group is responsible for as a whole")

# Combine a permission group and its associated permissions
class PermissionGroup(PermissionGroupSummary):
    permissions: List[Permission] = Field(
        description="A list of all individual permissions belonging to this group."
    )

# Collection of permission group summaries, without listing individual permissions
class PermissionGroupSummaries(BaseModel):
    groups: List[PermissionGroupSummary] = Field(
        description="A list of all available permission groups (including their names and group descriptions only)."
    )

# Collection of permission groups, including their associated permissions
class PermissionGroupCollection(BaseModel):
    groups: List[PermissionGroup] = Field(
        description="A list of all permission groups, flatly combined with their respective fine-grained sub-permissions."
    )

